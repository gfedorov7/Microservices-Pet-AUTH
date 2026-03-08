from src.util.exception.app_exception import AppException
from src.util.validator.validator import Validator


class NewUserValidator(Validator):
    def __init__(self, password_validator: Validator, unique_login_validator: Validator):
        self.password_validator = password_validator
        self.unique_login_validator = unique_login_validator

    async def is_valid(self) -> bool:
        try:
            await self.password_validator.is_valid()
            await self.unique_login_validator.is_valid()
        except AppException as e:
            raise e

        return True