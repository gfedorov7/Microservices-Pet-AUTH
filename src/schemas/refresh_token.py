from datetime import datetime

from pydantic import BaseModel


class RefreshTokenModelBase(BaseModel):
    token: str
    is_expired: bool = False
    expired_at: datetime
    user_id: int

class RefreshTokenModelCreate(RefreshTokenModelBase): ...

class RefreshTokenModelUpdate(BaseModel):
    token: str | None = None
    is_expired: bool | None = None
    expired_at: datetime | None = None
    user_id: int | None = None

class RefreshTokenModelRead(RefreshTokenModelBase):
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }