from typing import Dict

import jwt

from src.util.decoder.decoder import Decoder
from src.util.exception.token_exception import TokenException
from src.util.error_message_and_code import app_errors, TOKEN_EXPIRED, TOKEN_INVALID


class JWTDecoder(Decoder):
    def __init__(self, public_key: str, algorithm: str):
        self.public_key = public_key
        self.algorithm = algorithm

    def decode(self, token: str) -> Dict[str, any]:
        try:
            return jwt.decode(token, self.public_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            error = app_errors[TOKEN_EXPIRED]
            raise TokenException(error["message"], error["code"])
        except jwt.InvalidTokenError:
            error = app_errors[TOKEN_INVALID]
            raise TokenException(error["message"], error["code"])
