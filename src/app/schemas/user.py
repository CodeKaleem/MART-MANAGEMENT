from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserRead(BaseModel):
    user_id: int
    name: str
    email: str
    role: str
    