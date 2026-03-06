import datetime
from datetime import datetime
from typing import Dict, Any

import jwt

from src.util.encoder.encoder import Encoder


class JWTEncoder(Encoder):
    def __init__(self, private_key: str, algorithm: str):
        self.private_key = private_key
        self.algorithm = algorithm

    def encode(self, payload: Dict[str, Any], expired_at: datetime) -> str:
        payload['exp'] = expired_at
        return jwt.encode(payload, self.private_key, algorithm=self.algorithm)