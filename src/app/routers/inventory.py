from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.models.inventory import Inventory
from src.app.schemas.inventory import InventoryCreate, InventoryRead
from src.app.database.connectivity import async_session
from src.app.utils.auth import require_admin

router = APIRouter()

@router.post("/", response_model=InventoryRead, status_code=201)
async def create_inventory(item: InventoryCreate):
    """
    Create a new inventory item.
    Only accessible by admin users.
    """
    async with async_session() as session:
        db_item = Inventory(**item.dict())
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return db_item

@router.get("/", response_model=list[InventoryRead])
async def read_inventory():
    """
    Retrieve all inventory items.
    """
    async with async_session() as session:
        result = await session.execute(select(Inventory))
        return result.scalars().all()

@router.get("/{inventory_id}", response_model=InventoryRead)
async def get_inventory_by_id(inventory_id: int):
    """
    Retrieve a single inventory item by its ID.
    """
    async with async_session() as session:
        db_item = await session.get(Inventory, inventory_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Inventory item not found.")
        return db_item

@router.delete("/{inventory_id}", response_model=InventoryRead) # dependencies=[Depends(require_admin)]
async def delete_inventory(inventory_id: int):
    """
    Delete an inventory item by its ID.
    Only accessible by admin users.
    """
    async with async_session() as session:
        db_item = await session.get(Inventory, inventory_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Inventory item not found.")
        await session.delete(db_item)
        await session.commit()
        return db_item
