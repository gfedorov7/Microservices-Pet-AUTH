from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.helper.database_helper import database_helper
from src.model.user import User
from src.repository.user_repository import UserRepository
from src.repository.user_repository_impl import UserRepositoryImpl


def get_user_repo(
    session: AsyncSession = Depends(database_helper.session_depends),
) -> UserRepository:
    return UserRepositoryImpl(session, User)