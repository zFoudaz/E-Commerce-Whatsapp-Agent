import requests
from Agent.config import settings
from typing import List, Optional

url = settings.BACKEND_URL

def list_categories() -> List[dict]:
    """A tool used to get all the categories in the store
       Args: None
       Returns:
        List[dict] [{
                    "id": int,
                    "name": str,
                    "description":str
                    }]
    """
    response = requests.get(f"{url}/categories/")
    return response.json()

def search_products(keyword:Optional[str]=None, category_id:Optional[int] = None, in_stock_only:Optional[bool]=None) -> List[dict]:
    """
    A tool used to search for products in the store
    
    Args:
        keyword : str = keyword to search with
        category_id : int = id of a specific category
        in_stock_only : bool = search for in stock only products or no
    Returns:
        List[dict] [{
                    "id": int,
                    "name": str,
                    "description":str
                    }]
    """
    params = {
        "search":keyword,
        "category_id":category_id,
        "in_stock_only":in_stock_only
    }
    response = requests.get(f"{url}/products/", params=params)
    return response.json()

def get_product_details(product_id: int) -> dict:
    """
        A tool used to get details for products in the store
        
        Args:
            product_id : int = id of a specific product
        Returns:
            dict {
                "id": int,
                "name": str,
                "description": str,
                "price": float,
                "stock": int,
                "category_id": int
                }
        """
    response = requests.get(f"{url}/products/{product_id}/")
    return response.json()

def get_customer_cart(customer_name:str) -> dict:
    """
    A tool used to get the cart for a specific customer
    
    Args:
        customer_name : str = name of the customer
    Returns:
        dict {
            "customer_name": str,
            "items": [
                {
                    "id": int,
                    "customer_name": str,
                    "product_id": int,
                    "product_name": str,
                    "unit_price": float,
                    "quantity": int,
                    "subtotal": float
                }
            ],
            "total_items": int,
            "total_price": float
        }
    """
    params = {
        "customer_name":customer_name
    }
    response = requests.get(f"{url}/cart/{customer_name}", params=params)
    return response.json()

def add_item_to_cart(customer_name:str, product_id:int, quantity:int) -> dict:
    """
    A tool used to add an item to a customer's cart
    
    Args:
        customer_name : str = name of the customer
        product_id : int = id of the product to add
        quantity : int = quantity of the product to add
    Returns:
        dict {
            "id": int,
            "customer_name": str,
            "product_id": int,
            "product_name": str,
            "unit_price": float,
            "quantity": int,
            "subtotal": float
        }
    """
    data = {
        "customer_name":customer_name,
        "product_id":product_id,
        "quantity":quantity,
    }
    response = requests.post(f"{url}/cart/items",json=data)
    return response.json()

def remove_item_from_cart(item_id: int) -> dict:
    """
    A tool used to remove an item from a customer's cart
    NOTE: item_id is not the product_id its unique for each item in the cart
    
    Args:
        item_id : int = unique id of the item in the cart
    Returns:
        dict {
            "message": str
        }
    """
    response = requests.delete(
        f"{url}/cart/items/{item_id}"
    )
    return response.json()

def clear_customer_cart(customer_name:str) -> dict:
    """
    A tool used to clear all items from a customer's cart
    
    Args:
        customer_name : str = name of the customer
    Returns:
        dict {
            "message": str
        }
    """
    response = requests.delete(
        f"{url}/cart/{customer_name}"
    )
    return response.json()

def checkout_cart(customer_name:str, customer_phone:str) -> dict:
    """
    A tool used to checkout a customer's cart and create an order
    
    Args:
        customer_name : str = name of the customer
        customer_phone : str = phone number of the customer
    Returns:
        dict {
            "id": int,
            "customer_name": str,
            "customer_phone": str,
            "total_price": float,
            "status": str,
            "items": [
                {
                    "id": int,
                    "product_id": int,
                    "product_name": str,
                    "unit_price": float,
                    "quantity": int,
                    "subtotal": float
                }
            ]
        }
    """
    data = {
        "customer_name":customer_name,
        "customer_phone":customer_phone
    }
    response = requests.post(f"{url}/orders/checkout",json=data)
    return response.json()

def track_order(order_id:int) -> dict:
    """
    A tool used to track the status of an order
    
    Args:
        order_id : int = id of the order to track
    Returns:
        dict {
            "id": int,
            "customer_name": str,
            "customer_phone": str,
            "total_price": float,
            "status": str,
            "items": [
                {
                    "id": int,
                    "product_id": int,
                    "product_name": str,
                    "unit_price": float,
                    "quantity": int,
                    "subtotal": float
                }
            ]
        }
    """
    response = requests.get(f"{url}/orders/{order_id}")
    return response.json()

def cancel_order(order_id:int) -> dict:
    """
    A tool used to cancel an order
    
    Args:
        order_id : int = id of the order to cancel
    Returns:
        dict {
            "id": int,
            "customer_name": str,
            "customer_phone": str,
            "total_price": float,
            "status": str,
            "items": [
                {
                    "id": int,
                    "product_id": int,
                    "product_name": str,
                    "unit_price": float,
                    "quantity": int,
                    "subtotal": float
                }
            ]
        }
    """
    response = requests.put(f"{url}/orders/{order_id}/cancel")
    return response.json()

def list_orders() -> List[dict]:
    """
    A tool used to get all orders in the store
    
    Args: None
    Returns:
        List[dict] [{
            "id": int,
            "customer_name": str,
            "customer_phone": str,
            "total_price": float,
            "status": str,
            "items": [
                {
                    "id": int,
                    "product_id": int,
                    "product_name": str,
                    "unit_price": float,
                    "quantity": int,
                    "subtotal": float
                }
            ]
        }]
    """
    response = requests.get(f"{url}/orders/")
    return response.json()

tools = [
    list_categories,
    search_products,
    get_product_details,
    get_customer_cart,
    add_item_to_cart,
    remove_item_from_cart,
    clear_customer_cart,
    checkout_cart,
    track_order,
    cancel_order,
    list_orders
]
# if __name__ == '__main__':
    # print(list_categories())
    # print(search_products(keyword='laptop'))
    # print(search_products(category_id=2, in_stock_only=True))
    # print(get_product_details(1))
    # print(get_customer_cart("1"))
    # print(add_item_to_cart("1",4,1))
    # print(remove_item_from_cart(1))
    # print(get_customer_cart("1"))
    # print(cancel_order(1))
    # print(list_orders())