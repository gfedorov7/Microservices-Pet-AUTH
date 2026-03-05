import datetime
from typing import Dict

import jwt

from src.util.encoder.encoder import Encoder


class JWTEncoder(Encoder):
    def __init__(self, private_key: str, algorithm: str, expires_after_seconds: int):
        self.private_key = private_key
        self.algorithm = algorithm
        self.exp = expires_after_seconds

    def encode(self, payload: Dict[str, any]) -> str:
        payload['exp'] = datetime.datetime.now() + datetime.timedelta(seconds=self.exp)
        return jwt.encode(payload, self.private_key, algorithm=self.algorithm)