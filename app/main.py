from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models as models
from app.database import engine
from app.routers import users, products, reviews

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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Review Platform API!"}

# Include modular routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(reviews.router)