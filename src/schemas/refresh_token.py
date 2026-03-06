from datetime import datetime

from pydantic import BaseModel


class RefreshTokenModelBase(BaseModel):
    token: str
    is_expired: bool
    expires_at: datetime
    user_id: int

class RefreshTokenModelCreate(RefreshTokenModelBase): ...

class RefreshTokenModelUpdate(BaseModel):
    token: str | None = None
    is_expired: bool | None = None
    expires_at: datetime | None = None
    user_id: int | None = None

class RefreshTokenModelRead(RefreshTokenModelBase):
    created_at: datetime
    updated_at: datetime