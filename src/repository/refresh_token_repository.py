from abc import ABC, abstractmethod

from src.repository.repository import Repository


class RefreshTokenRepository(Repository):
    @abstractmethod
    async def disabled_not_expired_old_tokens_by_user(self, user_id: int) -> None: ...
