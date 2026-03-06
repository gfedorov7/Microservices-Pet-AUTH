from datetime import datetime
from typing import Dict, Any

from src.util.decoder.decoder import Decoder
from src.util.encoder.encoder import Encoder


class JWTService:
    def __init__(self, encoder: Encoder, decoder: Decoder):
        self.encoder = encoder
        self.decoder = decoder

    def encode(self, payload: Dict[str, Any], expired_at: datetime) -> str:
        return self.encoder.encode(payload, expired_at)

    def decode(self, token: str) -> Dict[str, Any]:
        return self.decoder.decode(token)