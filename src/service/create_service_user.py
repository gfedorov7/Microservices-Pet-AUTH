from typing import Dict, Any

from src.repository.user_repository import UserRepository
from src.schemas.user import UserRead
from src.util.errors.error_catalogs import app_errors
from src.util.errors.error_types import ErrorType
from src.util.exception.app_exception import AppException
from src.util.hasher.hasher import Hasher
from src.util.validator.validator import Validator


class UserCreateService:
    def __init__(
            self,
            user_repo: UserRepository,
            new_user_validator: Validator,
            hasher: Hasher
    ):
        self.user_repo = user_repo
        self.new_user_validator = new_user_validator
        self.hasher = hasher

    async def create_user(self, new_user: Dict[str, Any]) -> UserRead:
        try:
            _ = self.new_user_validator.is_valid()
        except AppException as e:
            raise e

        password = new_user.pop("password", None)
        if password is None:
            raise AppException(app_errors[ErrorType.PASSWORD_IS_NOT_SPECIFIED])

        hash_password = self.hasher.hash(password)
        new_user["password"] = hash_password

        user = await self.user_repo.create(new_user)
        return UserRead(**user)