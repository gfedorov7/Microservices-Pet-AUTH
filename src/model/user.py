from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

from src.model.base import Base
from src.util.mixin.datetime_model_mixin import DateTimeModelMixin
from src.model.refresh_token import RefreshToken

if TYPE_CHECKING:
    from src.model.refresh_token import RefreshToken


class User(DateTimeModelMixin, Base):
    login: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[bytes]

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )
