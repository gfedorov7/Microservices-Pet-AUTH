from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    login: str

class UserCreate(UserBase):
    password: str | bytes

class UserUpdate(BaseModel):
    login: str | None = None
    password: str | bytes | None = None

class UserRead(BaseModel):
    created_at: datetime
    updated_at: datetime
