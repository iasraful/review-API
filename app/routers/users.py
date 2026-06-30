from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import app.models as models
import app.schema as schemas
from app.database import get_db

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.post("", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
