from typing import Dict, Any

from src.repository.refresh_token_repository import RefreshTokenRepository
from src.util.errors.error_catalogs import app_errors
from src.util.errors.error_types import ErrorType
from src.util.exception.app_exception import AppException
from src.util.hasher.hasher import Hasher


class JwtRefreshTokenCreateService:
    def __init__(self, jwt_repo: RefreshTokenRepository, hasher: Hasher):
        self.jwt_repo = jwt_repo
        self.hasher = hasher

    async def save_new_and_disable_old(self, new_token: Dict[str, Any]) -> None:
        await self.jwt_repo.disabled_not_expired_old_tokens_by_user(new_token.get("user_id"))
        new_token["token"] = self.hasher.hash(new_token["token"])
        await self.jwt_repo.create(new_token)

    async def disable_tokens_by_user(self, user_id: int, rt: str) -> None:
        hashed_rt = self.hasher.hash(rt)
        await self.jwt_repo.disabled_not_expired_old_tokens_by_user(user_id, hashed_rt)

    async def check_valid_for_user_refresh_token(self, user_id: int, rt: str) -> None:
        hash_token = self.hasher.hash(rt)
        refresh_token_model = await self.jwt_repo.get_by_refresh_token(hash_token)
        if refresh_token_model.user_id != user_id:
            raise AppException(app_errors[ErrorType.TOKEN_NOT_FOR_THIS_USER])
        if refresh_token_model.is_expired:
            raise AppException(app_errors[ErrorType.TOKEN_EXPIRED])
