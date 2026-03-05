from src.repository.user_repository import UserRepository
from src.util.error_message_and_code import app_errors, LOGIN_ALREADY_USED
from src.util.exception.unique_user_exception import UniqueUserException
from src.util.validator.validator import Validator


class UniqueLoginValidator(Validator):
    def __init__(self, login: str, user_repository: UserRepository) -> None:
        self.login = login
        self.user_repository = user_repository

    async def is_valid(self):
        if not self._check_login_to_unique():
            error = app_errors[LOGIN_ALREADY_USED]
            raise UniqueUserException(error["message"], error["code"])

        return True

    async def _check_login_to_unique(self):
        founded_logins = await self.user_repository.get_by_login(self.login)
        return len(founded_logins) == 0