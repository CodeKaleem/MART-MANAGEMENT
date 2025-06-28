from pydantic import BaseModel

class NotificationCreate(BaseModel):
    user_id: int
    message: str
    status: str

class NotificationRead(BaseModel):
    notification_id: int
    user_id: int
    message: str
    status: str