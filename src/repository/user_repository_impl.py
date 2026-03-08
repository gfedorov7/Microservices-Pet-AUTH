from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.user import User
from src.repository.base_repository import BaseRepository


class UserRepositoryImpl(BaseRepository):
    def __init__(self, session: AsyncSession, model: Type[User]):
        super().__init__(session, model)

    async def get_by_login(self, login: str) -> User | None:
        stmt = select(self.model).where(self.model.login == login)
        return await self._get_one_or_none_by_stmt(stmt)
    