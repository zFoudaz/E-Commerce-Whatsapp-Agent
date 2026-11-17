from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List


router=APIRouter(prefix='/orders')

@router.post("/checkout", response_model=schemas.OrderResponse, status_code=201, tags=["Orders"])
def checkout_cart(checkout_data: schemas.CheckoutRequest, db: Session = Depends(get_db)):
    # 1. Fetch customer's cart items
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.customer_name == checkout_data.customer_name
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty. Add items to cart before checkout.")

    # 2. Check stock for every product in the cart
    for item in cart_items:
        if item.product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot checkout: '{item.product.name}' has only {item.product.stock} items left in stock."
            )

    # 3. Create the Order
    total_price = 0.0
    for item in cart_items:
        total_price += item.product.price * item.quantity

    new_order = models.Order(
        customer_name=checkout_data.customer_name,
        customer_phone=checkout_data.customer_phone,
        total_price=round(total_price, 2),
        status="pending"
    )
    db.add(new_order)
    db.flush()  # Generate order.id before creating order items

    # 4. Create OrderItems & deduct stock
    order_items_responses = []
    for item in cart_items:
        # Deduct stock permanently
        item.product.stock -= item.quantity

        subtotal = round(item.product.price * item.quantity, 2)
        order_item = models.OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            product_name=item.product.name,
            unit_price=item.product.price,
            quantity=item.quantity
        )
        db.add(order_item)
        db.flush()

        order_items_responses.routerend({
            "id": order_item.id,
            "product_id": order_item.product_id,
            "product_name": order_item.product_name,
            "unit_price": order_item.unit_price,
            "quantity": order_item.quantity,
            "subtotal": subtotal
        })

    # 5. Clear the customer's cart
    db.query(models.CartItem).filter(
        models.CartItem.customer_name == checkout_data.customer_name
    ).delete()

    db.commit()
    db.refresh(new_order)

    return {
        "id": new_order.id,
        "customer_name": new_order.customer_name,
        "customer_phone": new_order.customer_phone,
        "total_price": new_order.total_price,
        "status": new_order.status,
        "items": order_items_responses
    }


@router.get("/", response_model=List[schemas.OrderResponse], tags=["Orders"])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    results = []
    for order in orders:
        items_data = [
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product_name,
                "unit_price": item.unit_price,
                "quantity": item.quantity,
                "subtotal": round(item.unit_price * item.quantity, 2)
            }
            for item in order.items
        ]
        results.routerend({
            "id": order.id,
            "customer_name": order.customer_name,
            "customer_phone": order.customer_phone,
            "total_price": order.total_price,
            "status": order.status,
            "items": items_data
        })
    return results


@router.get("/{order_id}", response_model=schemas.OrderResponse, tags=["Orders"])
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items_data = [
        {
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product_name,
            "unit_price": item.unit_price,
            "quantity": item.quantity,
            "subtotal": round(item.unit_price * item.quantity, 2)
        } for item in order.items
    ]
    
    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "total_price": order.total_price,
        "status": order.status,
        "items": items_data
    }


@router.put("/{order_id}/cancel", response_model=schemas.OrderResponse, tags=["Orders"])
def cancel_order_direct(order_id: int, db: Session = Depends(get_db)):
    return update_order_status(order_id, schemas.OrderStatusUpdate(status="cancelled"), db)


@router.patch("/{order_id}/status", response_model=schemas.OrderResponse, tags=["Orders"])
def update_order_status(order_id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    old_status = order.status
    new_status = status_update.status.lower()

    # If cancelling an active order, restore stock back to products!
    if new_status == "cancelled" and old_status != "cancelled":
        for item in order.items:
            product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
            if product:
                product.stock += item.quantity

    order.status = new_status
    db.commit()
    db.refresh(order)

    items_data = [
        {
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product_name,
            "unit_price": item.unit_price,
            "quantity": item.quantity,
            "subtotal": round(item.unit_price * item.quantity, 2)
        }
        for item in order.items
    ]
    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "total_price": order.total_price,
        "status": order.status,
        "items": items_data
    }
