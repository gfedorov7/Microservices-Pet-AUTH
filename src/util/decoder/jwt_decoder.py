from typing import Dict, Any

import jwt

from src.util.decoder.decoder import Decoder
from src.util.errors.error_catalogs import app_errors
from src.util.errors.error_types import ErrorType
from src.util.exception.app_exception import AppException


class JwtDecoder(Decoder):
    def __init__(self, public_key: str, algorithm: str):
        self.public_key = public_key
        self.algorithm = algorithm

    def decode(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(token, self.public_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise AppException(app_errors[ErrorType.TOKEN_EXPIRED])
        except jwt.InvalidTokenError:
            raise AppException(app_errors[ErrorType.TOKEN_INVALID])
