from src.util.errors.app_error import AppError


class AppException(Exception):
    def __init__(self, app_error: AppError):
        self.message = app_error.message
        self.status_code = app_error.code
        super().__init__(self.message)