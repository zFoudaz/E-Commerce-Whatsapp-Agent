from fastapi import FastAPI
from routes import cart, categories, orders, products
import models
from database import engine

# Create all database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce Backend API",
    description="A complete and clean e-commerce backend with Categories, Products, Cart, and Orders (No Auth).",
    version="1.0.0"
)
app.include_router(cart.router)
app.include_router(categories.router)
app.include_router(orders.router)
app.include_router(products.router)