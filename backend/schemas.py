from pydantic import BaseModel
from typing import Optional, List


# --- Category Schemas ---
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# --- Product Schemas ---
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: int

    class Config:
        from_attributes = True


# --- Cart Schemas ---
class CartItemAdd(BaseModel):
    customer_name: str
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemResponse(BaseModel):
    id: int
    customer_name: str
    product_id: int
    product_name: str
    unit_price: float
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True


class CartSummaryResponse(BaseModel):
    customer_name: str
    items: List[CartItemResponse]
    total_items: int
    total_price: float


# --- Order Schemas ---
class CheckoutRequest(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    unit_price: float
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    customer_phone: Optional[str] = None
    total_price: float
    status: str
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str
