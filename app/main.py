from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

import app.models as models, app.schema as schemas
from app.database import engine, get_db

# Automatically creates tables in your local PostgreSQL on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Review Platform API")

# Setup CORS so your Next.js frontend can communicate with it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- USER ENDPOINTS (Helper to seed users for test) ---
@app.post("/api/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- PRODUCT ENDPOINTS ---

# 1. GET ALL PRODUCTS [cite: 38, 39]
@app.get("/api/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    # Group and aggregate directly from DB for faster loading
    results = db.query(
        models.Product,
        func.coalesce(func.avg(models.Review.rating), 0).label("avg_rating"),
        func.count(models.Review.id).label("count")
    ).outerjoin(models.Review).group_by(models.Product.id).all()
    
    output = []
    for product, avg_rating, count in results:
        prod_data = schemas.ProductResponse.from_orm(product)
        prod_data.average_rating = round(float(avg_rating), 1)
        prod_data.review_count = count
        output.append(prod_data)
        
    return output

# 2. GET PRODUCT DETAILS WITH REVIEWS [cite: 49, 50]
@app.get("/api/products/{id}", response_model=schemas.ProductDetailResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    # Aggregate ratings
    stats = db.query(
        func.coalesce(func.avg(models.Review.rating), 0).label("avg_rating"),
        func.count(models.Review.id).label("review_count")
    ).filter(models.Review.product_id == id).first()
    
    prod_data = schemas.ProductDetailResponse.from_orm(product)
    if stats:
        prod_data.average_rating = round(float(stats.avg_rating), 1) if stats.avg_rating else 0.0
        prod_data.review_count = stats.review_count
    else:
        prod_data.average_rating = 0.0
        prod_data.review_count = 0
    return prod_data

# Helper to create products via API easily
@app.post("/api/products", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_prod = models.Product(**product.dict())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod


# --- REVIEW ENDPOINTS ---

# 1. CREATE REVIEW [cite: 65, 66]
@app.post("/api/reviews", response_model=schemas.ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    # Verify product and user exist first to prevent foreign key crashes
    if not db.query(models.Product).filter(models.Product.id == review.product_id).first():
        raise HTTPException(status_code=400, detail="Product does not exist")
    if not db.query(models.User).filter(models.User.id == review.user_id).first():
        raise HTTPException(status_code=400, detail="User does not exist")
        
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# 2. UPDATE REVIEW [cite: 74, 75]
@app.put("/api/reviews/{id}", response_model=schemas.ReviewResponse)
def update_review(id: int, review_update: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    db_review = db.query(models.Review).filter(models.Review.id == id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
        
    update_data = review_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_review, key, value)
        
    db.commit()
    db.refresh(db_review)
    return db_review

# 3. DELETE REVIEW [cite: 76, 77]
@app.delete("/api/reviews/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(id: int, db: Session = Depends(get_db)):
    db_review = db.query(models.Review).filter(models.Review.id == id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(db_review)
    db.commit()
    return None