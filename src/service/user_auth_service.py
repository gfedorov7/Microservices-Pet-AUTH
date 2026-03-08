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
        user = await self.user_repo.get_by_login(user_in.get("login"))
        if user is None:
            raise AppException(app_errors[ErrorType.USER_NOT_FOUND])

        if not self.hasher.compare(user.password, user_in.get("password")):
            raise AppException(app_errors[ErrorType.INVALID_PASSWORD])

        return user
