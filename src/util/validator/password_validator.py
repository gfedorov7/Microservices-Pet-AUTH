import re

from src.config import settings
from src.util.error_message_and_code import app_errors, PASSWORD_SHORT, PASSWORD_HAS_NOT_SPEC, PASSWORD_HAS_NOT_NUMBERS, \
    PASSWORD_HAS_NOT_LETTERS
from src.util.exception.password_invalid_exception import PasswordInvalidException
from src.util.validator.validator import Validator



class PasswordValidator(Validator):
    def __init__(self, password):
        self.password = password
        self.len_password = settings.password_params_settings.len_password
        self.available_spec_symbols = settings.password_params_settings.available_spec_symbols

    def is_valid(self) -> bool:
        if not self._check_len_password():
            error = app_errors[PASSWORD_SHORT]
            raise PasswordInvalidException(error["message"], error["code"])
        if not self._check_available_spec_symbols():
            error = app_errors[PASSWORD_HAS_NOT_SPEC]
            raise PasswordInvalidException(error["message"], error["code"])
        if not self._check_numbers_in_password():
            error = app_errors[PASSWORD_HAS_NOT_NUMBERS]
            raise PasswordInvalidException(error["message"], error["code"])
        if not self._check_letters_in_password():
            error = app_errors[PASSWORD_HAS_NOT_LETTERS]
            raise PasswordInvalidException(error["message"], error["code"])

        return True

    def _check_len_password(self):
        return len(self.password) >= self.len_password

    def _check_available_spec_symbols(self):
        return any(map(lambda s: s in self.password, self.available_spec_symbols))

    def _check_numbers_in_password(self):
        return re.search('\d+', self.password) is not None

    def _check_letters_in_password(self):
        return re.search('[a-zA-Z]', self.password) is not None