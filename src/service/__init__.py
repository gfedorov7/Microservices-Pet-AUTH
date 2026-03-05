from typing import Dict

from src.util.decoder.decoder import Decoder
from src.util.encoder.encoder import Encoder


class JWTService:
    def __init__(self, encoder: Encoder, decoder: Decoder):
        self.encoder = encoder
        self.decoder = decoder

    def encode(self, payload: Dict[str, any]) -> str:
        return self.encoder.encode(payload)

    def decode(self, token: str) -> Dict[str, any]:
        return self.decoder.decode(token)