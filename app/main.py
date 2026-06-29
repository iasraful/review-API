from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from app import models

from app.database import engine, Base, SessionLocal, get_db
from sqlalchemy.orm import session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float 

@app.post("/items/")
async def create_item(item: Item):
    return item

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users/")
def read_users(db:session = Depends(get_db)):
    return {'status' : 'Successfully Connected to the Database! & Created tables'}