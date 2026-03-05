from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.base_repository import BaseRepository
from src.util.type.model import ModelType


class UserRepositoryImpl(BaseRepository):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        super().__init__(session, model)

    async def get_by_login(self, login: str) -> ModelType | None:
        stmt = select(self.model).where(self.model.login == login)
        return await self._get_one_or_none_by_stmt(stmt)
    