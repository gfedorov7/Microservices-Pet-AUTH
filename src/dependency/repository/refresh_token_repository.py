from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.helper.database_helper import database_helper
from src.model.refresh_token import RefreshToken
from src.repository.refresh_token_repository import RefreshTokenRepository
from src.repository.refresh_token_repository_impl import RefreshTokenRepositoryImpl


def get_refresh_token_repo(
    session: AsyncSession = Depends(database_helper.session_depends),
) -> RefreshTokenRepository:
    return RefreshTokenRepositoryImpl(session, RefreshToken)