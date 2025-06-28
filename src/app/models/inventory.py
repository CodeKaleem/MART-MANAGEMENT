from sqlmodel import SQLModel, Field
from typing import Optional

class Inventory(SQLModel, table=True):
    inventory_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    quantity: int
    threshold: int