from pydantic import BaseModel

class InventoryCreate(BaseModel):
    name: str
    category: str
    quantity: int
    threshold: int

class InventoryRead(BaseModel):
    inventory_id: int
    name: str
    category: str
    quantity: int
    threshold: int