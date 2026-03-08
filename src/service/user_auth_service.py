from typing import Any, Dict

from src.model.user import User
from src.repository.user_repository import UserRepository
from src.util.errors.error_catalogs import app_errors
from src.util.errors.error_types import ErrorType
from src.util.exception.app_exception import AppException
from src.util.hasher.hasher import Hasher


class UserAuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        hasher: Hasher,
    ):
        self.user_repo = user_repo
        self.hasher = hasher

    async def login(self, user_in: Dict[str, Any]) -> User:
        user = await self._get_user_by_login(user_in.get("login"))
        self._compare_password(user_in.get("password"), user.password)

        return user

    async def _get_user_by_login(self, login: str) -> User:
        user = await self.user_repo.get_by_login(login)
        if user is None:
            raise AppException(app_errors[ErrorType.USER_NOT_FOUND])

        return user

    def _compare_password(self, password: str, hashed_password: bytes) -> None:
        if not self.hasher.compare(hashed_password, password):
            raise AppException(app_errors[ErrorType.INVALID_PASSWORD])