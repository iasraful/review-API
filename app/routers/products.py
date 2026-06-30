from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import app.models as models
import app.schema as schemas
from app.database import get_db

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

# 1. GET ALL PRODUCTS (with search and rating filter)
@router.get("", response_model=List[schemas.ProductResponse])
def get_products(search: Optional[str] = None, min_rating: Optional[float] = None, db: Session = Depends(get_db)):
    # Start basic query
    query = db.query(
        models.Product,
        func.coalesce(func.avg(models.Review.rating), 0).label("avg_rating"),
        func.count(models.Review.id).label("count")
    ).outerjoin(models.Review)
    
    # Search filter (matches title case-insensitively)
    if search:
        query = query.filter(models.Product.title.ilike(f"%{search}%"))
        
    query = query.group_by(models.Product.id)
    
    # Rating filter
    if min_rating:
        query = query.having(func.coalesce(func.avg(models.Review.rating), 0) >= min_rating)
        
    results = query.all()
    
    output = []
    for product, avg_rating, count in results:
        prod_data = schemas.ProductResponse.from_orm(product)
        prod_data.average_rating = round(float(avg_rating), 1)
        prod_data.review_count = count
        output.append(prod_data)
        
    return output

# 2. GET PRODUCT DETAILS WITH REVIEWS
@router.get("/{id}", response_model=schemas.ProductDetailResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    stats = db.query(
        func.coalesce(func.avg(models.Review.rating), 0).label("avg_rating"),
        func.count(models.Review.id).label("review_count")
    ).filter(models.Review.product_id == id).first()
    
    prod_data = schemas.ProductDetailResponse.from_orm(product)
    prod_data.average_rating = round(float(stats.avg_rating), 1) if stats and stats.avg_rating else 0.0
    prod_data.review_count = stats.review_count if stats else 0
    return prod_data

# Helper to create products via API easily
@router.post("", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_prod = models.Product(**product.dict())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

# Helper to delete products via API
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return None
