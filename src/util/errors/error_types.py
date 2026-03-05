from enum import Enum


class ErrorType(Enum):
    TOKEN_EXPIRED = "Token expired"
    TOKEN_INVALID = "Token invalid"

    PASSWORD_SHORT = "Password short"
    PASSWORD_HAS_NOT_SPEC = "Password has not spec"
    PASSWORD_HAS_NOT_NUMBERS = "Password has not numbers"
    PASSWORD_HAS_NOT_LETTERS = "Password has not letters"

    LOGIN_ALREADY_USED = "Login already used"