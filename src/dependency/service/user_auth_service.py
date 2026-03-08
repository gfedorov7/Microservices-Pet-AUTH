from fastapi.params import Depends

from src.dependency.repository.user_repository import get_user_repo
from src.repository.user_repository import UserRepository
from src.service.user_auth_service import UserAuthService
from src.util.hasher.bcrypt_hasher import BcryptHasher


def get_user_auth_service(
    user_repo: UserRepository = Depends(get_user_repo),
) -> UserAuthService:
    hasher = BcryptHasher()

    return UserAuthService(
        user_repo,
        hasher
    )