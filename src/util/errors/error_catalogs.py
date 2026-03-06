from src.util.errors.app_error import AppError
from src.util.errors.error_types import ErrorType

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

    ErrorType.PASSWORD_IS_NOT_SPECIFIED: AppError(
        message="Password is not specified",
        code=422,
    ),
}