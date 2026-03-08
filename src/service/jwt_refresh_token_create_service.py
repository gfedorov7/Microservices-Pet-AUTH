from typing import Dict, Any

from src.repository.refresh_token_repository import RefreshTokenRepository


class JwtRefreshTokenCreateService:
    def __init__(self, jwt_repo: RefreshTokenRepository):
        self.jwt_repo = jwt_repo

    async def save_new_and_disable_old(self, new_token: Dict[str, Any]) -> None:
        await self.jwt_repo.disabled_not_expired_old_tokens_by_user(new_token.get("user_id"))
        await self.jwt_repo.create(new_token)

    async def disable_tokens_by_user(self, user_id: int) -> None:
        await self.jwt_repo.disabled_not_expired_old_tokens_by_user(user_id)
