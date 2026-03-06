from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.base_repository import BaseRepository
from src.util.type.model import ModelType


class RefreshTokenRepository(BaseRepository):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        super().__init__(session, model)