import re

from src.config import settings
from src.util.errors.error_catalogs import app_errors
from src.util.errors.error_types import ErrorType
from src.util.exception.app_exception import AppException
from src.util.validator.validator import Validator


class PasswordValidator(Validator):
    def __init__(self, password):
        self.password = password
        self.len_password = settings.password_params_settings.len_password
        self.available_spec_symbols = settings.password_params_settings.available_spec_symbols

    async def is_valid(self) -> bool:
        if not self._check_len_password():
            raise AppException(app_errors[ErrorType.PASSWORD_SHORT])
        if not self._check_available_spec_symbols():
            raise AppException(app_errors[ErrorType.PASSWORD_HAS_NOT_SPEC])
        if not self._check_numbers_in_password():
            raise AppException(app_errors[ErrorType.PASSWORD_HAS_NOT_NUMBERS])
        if not self._check_letters_in_password():
            raise AppException(app_errors[ErrorType.PASSWORD_HAS_NOT_LETTERS])

        return True

    def _check_len_password(self):
        return len(self.password) >= self.len_password

    def _check_available_spec_symbols(self):
        return any(map(lambda s: s in self.password, self.available_spec_symbols))

    def _check_numbers_in_password(self):
        return re.search(r"\d+", self.password) is not None

    def _check_letters_in_password(self):
        return re.search(r"[a-zA-Z]", self.password) is not None