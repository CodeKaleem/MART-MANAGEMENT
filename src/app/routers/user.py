from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
# from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.models.user import User
from src.app.schemas.user import UserCreate, UserRead
from src.app.database.connectivity import async_session
from src.app.utils.auth import require_admin

router = APIRouter()

@router.post("/signup", response_model=UserRead, status_code=201)
async def signup(user: UserCreate):
    async with async_session() as session:
        existing_user = await session.execute(select(User).where(User.email == user.email))
        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = User(**user.dict())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

@router.post("/login")
async def login(email: str, password: str):
    async with async_session() as session:
        user = await session.execute(select(User).where(User.email == email, User.password == password))
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"user_id": user.user_id, "role": user.role, "name": user.name}


@router.get("/", response_model=list[UserRead])
async def read_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    async with async_session() as session:
        db_user = await session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found.")
        await session.delete(db_user)
        await session.commit()
        return {'message': 'user deleted!'}
