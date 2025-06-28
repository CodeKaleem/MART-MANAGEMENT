from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.models.notification import Notification
from src.app.schemas.notification import NotificationCreate, NotificationRead
from src.app.database.connectivity import async_session

router = APIRouter()

@router.post("/", response_model=NotificationRead, status_code=201)
async def create_notification(notification: NotificationCreate):
    async with async_session() as session:
        db_notification = Notification(**notification.dict())
        session.add(db_notification)
        await session.commit()
        await session.refresh(db_notification)
        return db_notification

@router.get("/", response_model=list[NotificationRead])
async def read_notifications():
    async with async_session() as session:
        result = await session.execute(select(Notification))
        return result.scalars().all()
