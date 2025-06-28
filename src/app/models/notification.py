from sqlmodel import SQLModel, Field
from typing import Optional

class Notification(SQLModel, table=True):
    notification_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    message: str
    status: str