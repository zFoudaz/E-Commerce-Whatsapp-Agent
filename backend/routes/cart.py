from fastapi import APIRouter, Depends, HTTPException
import schemas, models
from database import get_db
from sqlalchemy.orm import Session


router=APIRouter(prefix='/cart')

@router.post("/items", response_model=schemas.CartItemResponse, status_code=201, tags=["Cart"])
def add_item_to_cart(item: schemas.CartItemAdd, db: Session = Depends(get_db)):
    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < item.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough stock available. Current stock: {product.stock}"
        )

    # Check if item is already in the customer's cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.customer_name == item.customer_name,
        models.CartItem.product_id == item.product_id
    ).first()

    if existing_item:
        new_quantity = existing_item.quantity + item.quantity
        if product.stock < new_quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot add more. Total in cart ({new_quantity}) exceeds stock ({product.stock})"
            )
        existing_item.quantity = new_quantity
        cart_entry = existing_item
    else:
        cart_entry = models.CartItem(
            customer_name=item.customer_name,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_entry)

    db.commit()
    db.refresh(cart_entry)

    subtotal = round(product.price * cart_entry.quantity, 2)
    return {
        "id": cart_entry.id,
        "customer_name": cart_entry.customer_name,
        "product_id": cart_entry.product_id,
        "product_name": product.name,
        "unit_price": product.price,
        "quantity": cart_entry.quantity,
        "subtotal": subtotal
    }


@router.get("/{customer_name}", response_model=schemas.CartSummaryResponse, tags=["Cart"])
def get_customer_cart(customer_name: str, db: Session = Depends(get_db)):
    cart_items = db.query(models.CartItem).filter(models.CartItem.customer_name == customer_name).all()

    items_data = []
    total_price = 0.0
    total_items = 0

    for item in cart_items:
        subtotal = round(item.product.price * item.quantity, 2)
        total_price += subtotal
        total_items += item.quantity
        items_data.routerend({
            "id": item.id,
            "customer_name": item.customer_name,
            "product_id": item.product_id,
            "product_name": item.product.name,
            "unit_price": item.product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "customer_name": customer_name,
        "items": items_data,
        "total_items": total_items,
        "total_price": round(total_price, 2)
    }


@router.put("/items/{item_id}", response_model=schemas.CartItemResponse, tags=["Cart"])
def update_cart_item_quantity(item_id: int, updated: schemas.CartItemUpdate, db: Session = Depends(get_db)):
    cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if updated.quantity <= 0:
        # If quantity <= 0, remove the item
        db.delete(cart_item)
        db.commit()
        raise HTTPException(status_code=200, detail="Item removed from cart because quantity was 0")

    if cart_item.product.stock < updated.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Requested quantity exceeds available stock ({cart_item.product.stock})"
        )

    cart_item.quantity = updated.quantity
    db.commit()
    db.refresh(cart_item)

    subtotal = round(cart_item.product.price * cart_item.quantity, 2)
    return {
        "id": cart_item.id,
        "customer_name": cart_item.customer_name,
        "product_id": cart_item.product_id,
        "product_name": cart_item.product.name,
        "unit_price": cart_item.product.price,
        "quantity": cart_item.quantity,
        "subtotal": subtotal
    }


@router.delete("/items/{item_id}", tags=["Cart"])
def remove_item_from_cart(item_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}


@router.delete("/{customer_name}", tags=["Cart"])
@router.delete("/clear/{customer_name}", tags=["Cart"])
def clear_customer_cart(customer_name: str, db: Session = Depends(get_db)):
    db.query(models.CartItem).filter(models.CartItem.customer_name == customer_name).delete()
    db.commit()
    return {"message": f"Cart for {customer_name} cleared successfully"}

