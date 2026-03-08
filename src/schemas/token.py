from pydantic import BaseModel

from src.config import settings


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = settings.token_settings.token_type

class TokenRegenerate(BaseModel):
    refresh_token: str