from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    inventory_id: int
    quantity: int
    order_date: str  

class OrderRead(BaseModel):
    order_id: int
    user_id: int
    inventory_id: int
    quantity: int
    order_date: str