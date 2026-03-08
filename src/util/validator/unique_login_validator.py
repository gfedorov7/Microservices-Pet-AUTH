from src.repository.user_repository import UserRepository
from src.util.errors.error_catalogs import app_errors
from src.util.errors.error_types import ErrorType
from src.util.exception.app_exception import AppException
from src.util.validator.validator import Validator


class UniqueLoginValidator(Validator):
    def __init__(self, login: str, user_repository: UserRepository) -> None:
        self.login = login
        self.user_repository = user_repository

    async def is_valid(self):
        if not await self._check_login_to_unique():
            raise AppException(app_errors[ErrorType.LOGIN_ALREADY_USED])

        return True

    async def _check_login_to_unique(self):
        founded_logins = await self.user_repository.get_by_login(self.login)
        return not bool(founded_logins)