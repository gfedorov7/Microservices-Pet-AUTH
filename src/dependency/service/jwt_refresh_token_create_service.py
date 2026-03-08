from fastapi import Depends

from src.dependency.repository.refresh_token_repository import get_refresh_token_repo
from src.repository.refresh_token_repository import RefreshTokenRepository
from src.service.jwt_refresh_token_create_service import JwtRefreshTokenCreateService


def get_jwt_refresh_token_create_service(
        jwt_repo: RefreshTokenRepository = Depends(get_refresh_token_repo),
) -> JwtRefreshTokenCreateService:
    return JwtRefreshTokenCreateService(jwt_repo)