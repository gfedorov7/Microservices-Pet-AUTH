from abc import ABC, abstractmethod

from src.model.refresh_token import RefreshToken
from src.repository.repository import Repository


class RefreshTokenRepository(Repository):
    @abstractmethod
    async def disabled_not_expired_old_tokens_by_user(self, user_id: int, rt: str = None) -> None: ...

    @abstractmethod
    async def get_by_refresh_token(self, rt: str) -> RefreshToken: ...