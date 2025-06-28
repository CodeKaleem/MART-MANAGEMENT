from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from src.app.models.inventory import Inventory
from src.app.schemas.inventory import InventoryCreate, InventoryRead

from src.app.models.order import Order
from src.app.schemas.order import OrderCreate, OrderRead

from src.app.models.notification import Notification
from src.app.schemas.notification import NotificationCreate, NotificationRead

from src.app.models.user import User
from src.app.schemas.user import UserCreate, UserRead

from src.app.database.connectivity import async_session, engine

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/")
def root():
    return {"message": "Mart Management System is running!"}

@app.post("/inventory", response_model=InventoryRead, status_code=201)
async def create_inventory(item: InventoryCreate):
    async with async_session() as session:
        try:
            db_item = Inventory(**item.dict())
            session.add(db_item)
            await session.commit()
            await session.refresh(db_item)
            return db_item
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Inventory creation failed: Integrity error.")

@app.get("/inventory", response_model=list[InventoryRead])
async def read_inventory():
    async with async_session() as session:
        result = await session.execute(select(Inventory))
        inventory_items = result.scalars().all()
        if not inventory_items:
            raise HTTPException(status_code=404, detail="No inventory items found.")
        return inventory_items

@app.get("/inventory/{inventory_id}", response_model=InventoryRead)
async def get_inventory_by_id(inventory_id: int):
    async with async_session() as session:
        db_item = await session.get(Inventory, inventory_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Inventory item not found.")
        return db_item

@app.post("/order", response_model=OrderRead, status_code=201)
async def create_order(order: OrderCreate):
    async with async_session() as session:
        try:
            # Ensure user and inventory exist
            user = await session.get(User, order.user_id)
            inventory = await session.get(Inventory, order.inventory_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")
            if not inventory:
                raise HTTPException(status_code=404, detail="Inventory item not found.")
            if inventory.quantity < order.quantity:
                raise HTTPException(status_code=400, detail="Insufficient inventory quantity.")
            # Create order and update inventory
            db_order = Order(**order.dict())
            inventory.quantity -= order.quantity
            session.add(db_order)
            await session.commit()
            await session.refresh(db_order)
            return db_order
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Order creation failed: Integrity error.")

@app.get("/order", response_model=list[OrderRead])
async def read_orders():
    async with async_session() as session:
        result = await session.execute(select(Order))
        orders = result.scalars().all()
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found.")
        return orders

@app.get("/order/{order_id}", response_model=OrderRead)
async def get_order_by_id(order_id: int):
    async with async_session() as session:
        db_order = await session.get(Order, order_id)
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found.")
        return db_order

@app.post("/notification", response_model=NotificationRead, status_code=201)
async def create_notification(notification: NotificationCreate):
    async with async_session() as session:
        try:
            # Ensure user exists
            user = await session.get(User, notification.user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")
            db_notification = Notification(**notification.dict())
            session.add(db_notification)
            await session.commit()
            await session.refresh(db_notification)
            return db_notification
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Notification creation failed: Integrity error.")

@app.get("/notification", response_model=list[NotificationRead])
async def read_notifications():
    async with async_session() as session:
        result = await session.execute(select(Notification))
        notifications = result.scalars().all()
        if not notifications:
            raise HTTPException(status_code=404, detail="No notifications found.")
        return notifications

@app.get("/notification/{notification_id}", response_model=NotificationRead)
async def get_notification_by_id(notification_id: int):
    async with async_session() as session:
        db_notification = await session.get(Notification, notification_id)
        if not db_notification:
            raise HTTPException(status_code=404, detail="Notification not found.")
        return db_notification

@app.post("/user", response_model=UserRead, status_code=201)
async def create_user(user: UserCreate):
    async with async_session() as session:
        try:
            db_user = User(**user.dict())
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return db_user
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail="User creation failed: Integrity error.")

@app.get("/user", response_model=list[UserRead])
async def read_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        if not users:
            raise HTTPException(status_code=404, detail="No users found.")
        return users

@app.get("/user/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int):
    async with async_session() as session:
        db_user = await session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found.")
        return db_user

@app.put("/user/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserCreate):
    async with async_session() as session:
        db_user = await session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found.")
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

@app.delete("/user/{user_id}", status_code=204)
async def delete_user(user_id: int):
    async with async_session() as session:
        db_user = await session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found.")
        await session.delete(db_user)
        await session.commit()
        return {'message': 'user deleted!'}