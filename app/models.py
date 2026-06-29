import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # [cite: 17]
    email = Column(String, unique=True, index=True, nullable=False) # [cite: 18]
    created_at = Column(DateTime, default=datetime.datetime.utcnow) # [cite: 19]

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False) # [cite: 23]
    description = Column(Text) # [cite: 24]
    image_url = Column(String, nullable=True) # [cite: 25]
    created_at = Column(DateTime, default=datetime.datetime.utcnow) # [cite: 26]
    
    # Establish relationship to reviews
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False) # [cite: 31]
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # [cite: 32]
    rating = Column(Integer, nullable=False) # [cite: 33]
    comment = Column(Text, nullable=True) # [cite: 34]
    created_at = Column(DateTime, default=datetime.datetime.utcnow) # [cite: 35]

    product = relationship("Product", back_populates="reviews")
    user = relationship("User")