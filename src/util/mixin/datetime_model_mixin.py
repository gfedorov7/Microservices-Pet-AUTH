from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Mapped, mapped_column


moscow_tz = ZoneInfo("Europe/Moscow")

def now_msk_naive() -> datetime:
    return datetime.now(moscow_tz).replace(tzinfo=None)

class DateTimeModelMixin:
    created_at: Mapped[datetime] = mapped_column(default=now_msk_naive)

    updated_at: Mapped[datetime] = mapped_column(default=now_msk_naive, onupdate=now_msk_naive)
