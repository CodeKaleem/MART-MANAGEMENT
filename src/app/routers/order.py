from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.models.order import Order
from src.app.schemas.order import OrderCreate, OrderRead
from src.app.database.connectivity import async_session

router = APIRouter()

@router.post("/", response_model=OrderRead, status_code=201)
async def create_order(order: OrderCreate):
    async with async_session() as session:
        db_order = Order(**order.dict())
        session.add(db_order)
        await session.commit()
        await session.refresh(db_order)
        return db_order

@router.get("/", response_model=list[OrderRead])
async def read_orders():
    async with async_session() as session:
        result = await session.execute(select(Order))
        return result.scalars().all()
