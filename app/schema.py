from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- REVIEW SCHEMAS ---
class ReviewBase(BaseModel):
    product_id: int 
    user_id: int 
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    comment: str 

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    comment: str
    created_at: datetime
    user: Optional[UserResponse] = None # Nested user to easily display the name on frontend [cite: 61]

    class Config:
        from_attributes = True

# --- PRODUCT SCHEMAS ---
class ProductBase(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    average_rating: float = 0.0
    review_count: int = 0
    
    class Config:
        from_attributes = True

class ProductDetailResponse(ProductResponse):
    reviews: List[ReviewResponse] = []