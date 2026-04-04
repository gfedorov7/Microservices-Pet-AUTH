from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, update, select

from src.model.refresh_token import RefreshToken
from src.repository.base_repository import BaseRepository
from src.repository.refresh_token_repository import RefreshTokenRepository


class RefreshTokenRepositoryImpl(BaseRepository):
    def __init__(self, session: AsyncSession, model: Type[RefreshToken]):
        super().__init__(session, model)

    async def disabled_not_expired_old_tokens_by_user(self, user_id: int, rt: str = None) -> None:
        if rt is None:
            stmt = (
                update(self.model)
                .where(
                    self.model.user_id == user_id,
                    self.model.is_expired == False
                )
                .values(is_expired=True)
            )
        else:
            stmt = (
                update(self.model)
                .where(
                    self.model.user_id == user_id,
                    self.model.is_expired == False,
                    self.model.token == rt
                )
                .values(is_expired=True)
            )

        await self.session.execute(stmt)
        await self.session.commit()

    async def get_by_refresh_token(self, rt: str):
        stmt = select(self.model).where(self.model.token == rt)
        return await self._get_one_or_none_by_stmt(stmt)
