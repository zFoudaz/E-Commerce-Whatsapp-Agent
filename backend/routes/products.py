from fastapi import APIRouter, Depends, HTTPException, Query
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional


router=APIRouter(prefix='/products')

@router.post("/", response_model=schemas.ProductResponse, status_code=201, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # Verify that the category exists
    category = db.query(models.Category).filter(models.Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/", response_model=List[schemas.ProductResponse], tags=["Products"])
def get_products(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    search: Optional[str] = Query(None, description="Search products by name"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    in_stock_only: bool = Query(False, description="Filter only in-stock products"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)

    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)
    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    if in_stock_only:
        query = query.filter(models.Product.stock > 0)

    return query.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=schemas.ProductResponse, tags=["Products"])
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=schemas.ProductResponse, tags=["Products"])
def update_product(product_id: int, updated: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if updated.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == updated.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        product.category_id = updated.category_id

    if updated.name is not None:
        product.name = updated.name
    if updated.description is not None:
        product.description = updated.description
    if updated.price is not None:
        product.price = updated.price
    if updated.stock is not None:
        product.stock = updated.stock

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": f"Product {product_id} deleted successfully"}
