from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Mapped, mapped_column


class DateTimeModelMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), onupdate=datetime.now())
