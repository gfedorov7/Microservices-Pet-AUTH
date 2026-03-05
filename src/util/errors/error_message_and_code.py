from src.util.errors.app_error import AppError
from src.util.errors.error_types import ErrorType

TOKEN_EXPIRED = "Token expired"
TOKEN_INVALID = "Token invalid"

PASSWORD_SHORT = "Password short"
PASSWORD_HAS_NOT_SPEC = "Password has not spec"
PASSWORD_HAS_NOT_NUMBERS = "Password has not numbers"
PASSWORD_HAS_NOT_LETTERS = "Password has not letters"

LOGIN_ALREADY_USED = "Login already used"

app_errors = {
    ErrorType.TOKEN_EXPIRED: AppError(
        message="Token already expired",
        code=401,
    ),
    ErrorType.TOKEN_INVALID: AppError(
        message="Invalid token",
        code=401,
    ),

    ErrorType.PASSWORD_SHORT: AppError(
        message="The password is too short",
        code=400,
    ),
    ErrorType.PASSWORD_HAS_NOT_SPEC: AppError(
        message="The password does not contain any special characters",
        code=400,
    ),
    ErrorType.PASSWORD_HAS_NOT_NUMBERS: AppError(
        message="The password does not contain numbers",
        code=400,
    ),
    ErrorType.PASSWORD_HAS_NOT_LETTERS: AppError(
        message="The password does not contain letter",
        code=400,
    ),

    ErrorType.LOGIN_ALREADY_USED: AppError(
        message="Login is already used another user",
        code=409,
    ),
}