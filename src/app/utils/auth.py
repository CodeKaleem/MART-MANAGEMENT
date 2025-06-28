from fastapi import Depends, HTTPException
from src.app.models.user import User
from src.app.database.connectivity import async_session
from sqlmodel.ext.asyncio.session import AsyncSession

async def get_current_user(user_id: int, session: AsyncSession = Depends(async_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")