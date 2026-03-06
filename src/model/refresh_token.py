from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.model.base import Base
from src.util.mixin.datetime_model_mixin import DateTimeModelMixin

if TYPE_CHECKING:
    from src.model.user import User


class RefreshToken(DateTimeModelMixin, Base):
    token: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_expired: Mapped[bool] = mapped_column(default=False)
    expired_at: Mapped[datetime] = mapped_column(default=None)

    user_id: Mapped[int] = mapped_column(unique=True, index=True, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")
