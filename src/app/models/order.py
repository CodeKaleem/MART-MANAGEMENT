from sqlmodel import SQLModel, Field
from typing import Optional

class Order(SQLModel, table=True):
    order_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    inventory_id: int = Field(foreign_key="inventory.inventory_id")
    quantity: int
    order_date: str