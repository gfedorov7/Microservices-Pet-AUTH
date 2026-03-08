from fastapi import Depends

from src.dependency.repository.user_repository import get_user_repo
from src.repository.user_repository import UserRepository
from src.service.user_create_service import UserCreateService
from src.util.hasher.bcrypt_hasher import BcryptHasher


def get_user_create_service(
        user_repo: UserRepository = Depends(get_user_repo),
) -> UserCreateService:
    hasher = BcryptHasher()

    return UserCreateService(
        user_repo,
        hasher
    )