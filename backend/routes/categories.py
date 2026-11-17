from fastapi import APIRouter, Depends, HTTPException
import schemas, models
from database import get_db
from sqlalchemy.orm import Session
from typing import List


router=APIRouter(prefix='/categories')

@router.post("/", response_model=schemas.CategoryResponse, status_code=201, tags=["Categories"])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    new_category = models.Category(name=category.name, description=category.description)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=List[schemas.CategoryResponse], tags=["Categories"])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


@router.get("/{category_id}", response_model=schemas.CategoryResponse, tags=["Categories"])
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{category_id}", tags=["Categories"])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"message": f"Category {category_id} deleted successfully"}
