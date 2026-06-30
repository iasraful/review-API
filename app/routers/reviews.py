from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.models as models
import app.schema as schemas
from app.database import get_db

router = APIRouter(
    prefix="/api/reviews",
    tags=["reviews"]
)

# 1. CREATE REVIEW
@router.post("", response_model=schemas.ReviewResponse, status_code=status.HTTP_201_CREATED)
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

# 2. UPDATE REVIEW
@router.put("/{id}", response_model=schemas.ReviewResponse)
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

# 3. DELETE REVIEW
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(id: int, db: Session = Depends(get_db)):
    db_review = db.query(models.Review).filter(models.Review.id == id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(db_review)
    db.commit()
    return None
