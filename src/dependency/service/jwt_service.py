from src.config import settings
from src.service.jwt_service import JwtService
from src.util.decoder.jwt_decoder import JwtDecoder
from src.util.encoder.jwt_encoder import JwtEncoder


def get_jwt_service() -> JwtService:
    encoder = JwtEncoder(settings.keys_settings.private_key, settings.token_settings.token_algorithm)
    decoder = JwtDecoder(settings.keys_settings.public_key, settings.token_settings.token_algorithm)

    return JwtService(encoder, decoder)