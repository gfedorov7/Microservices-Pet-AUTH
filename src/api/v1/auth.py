from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi.params import Depends

from src.config import settings
from src.dependency.repository.user_repository import get_user_repo
from src.dependency.service.jwt_refresh_token_create_service import get_jwt_refresh_token_create_service
from src.dependency.service.jwt_service import get_jwt_service
from src.dependency.service.user_create_service import get_user_create_service
from src.repository.user_repository import UserRepository
from src.schemas.refresh_token import RefreshTokenModelCreate
from src.schemas.token import Token
from src.schemas.user import UserCreate
from src.service.jwt_refresh_token_create_service import JwtRefreshTokenCreateService
from src.service.jwt_service import JwtService
from src.service.user_create_service import UserCreateService
from src.util.validator.new_user_validator import NewUserValidator
from src.util.validator.password_validator import PasswordValidator
from src.util.validator.unique_login_validator import UniqueLoginValidator


api_router = APIRouter(prefix="/auth", tags=["Auth"])

@api_router.post("/sign-up")
async def sign_up(
        user_in: UserCreate,
        user_repo: UserRepository = Depends(get_user_repo),
        jwt_rt_create_service: JwtRefreshTokenCreateService = Depends(get_jwt_refresh_token_create_service),
        jwt_service: JwtService = Depends(get_jwt_service),
        user_create_service: UserCreateService = Depends(get_user_create_service)
):
    password_validator = PasswordValidator(user_in.password)
    unique_login_validator = UniqueLoginValidator(user_in.login, user_repo)
    new_user_validator = NewUserValidator(password_validator, unique_login_validator)

    new_user = await user_create_service.create_user(user_in.model_dump(), new_user_validator)

    payload = {
        "user_id": new_user.id,
    }

    access_token_expired = datetime.now() + timedelta(seconds=settings.token_settings.token_access_expires)
    access_token = jwt_service.encode(payload, access_token_expired)

    refresh_token_expired = datetime.now() + timedelta(seconds=settings.token_settings.token_refresh_expires)
    refresh_token = jwt_service.encode(payload, refresh_token_expired)

    refresh_token_schema = RefreshTokenModelCreate(
        token=refresh_token,
        expired_at=refresh_token_expired,
        user_id=new_user.id
    )
    await jwt_rt_create_service.save_new_and_disable_old(refresh_token_schema.model_dump())

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )

