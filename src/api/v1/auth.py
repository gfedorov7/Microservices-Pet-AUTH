from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi.params import Depends

from src.config import settings
from src.dependency.repository.user_repository import get_user_repo
from src.dependency.service.jwt_refresh_token_create_service import get_jwt_refresh_token_create_service
from src.dependency.service.jwt_service import get_jwt_service
from src.dependency.service.user_auth_service import get_user_auth_service
from src.dependency.service.user_create_service import get_user_create_service
from src.model.user import User
from src.repository.user_repository import UserRepository
from src.schemas.refresh_token import RefreshTokenModelCreate
from src.schemas.token import Token, TokenRegenerate
from src.schemas.user import UserCreate, UserLogin
from src.service.jwt_refresh_token_create_service import JwtRefreshTokenCreateService
from src.service.jwt_service import JwtService
from src.service.user_auth_service import UserAuthService
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
    new_user_validator = get_new_user_validator(user_in.login, user_in.password, user_repo)
    new_user = await user_create_service.create_user(user_in.model_dump(), new_user_validator)
    return await token_generator(new_user.id, jwt_service, jwt_rt_create_service)

@api_router.post("/login")
async def login(
        user_in: UserLogin,
        auth_service: UserAuthService = Depends(get_user_auth_service),
        jwt_service: JwtService = Depends(get_jwt_service),
        jwt_rt_create_service: JwtRefreshTokenCreateService = Depends(get_jwt_refresh_token_create_service),
):
    user = await auth_service.login(user_in.model_dump())
    return await token_generator(user.id, jwt_service, jwt_rt_create_service)

@api_router.post("/refresh")
async def refresh(
        token: TokenRegenerate,
        jwt_service: JwtService = Depends(get_jwt_service),
        jwt_rt_create_service: JwtRefreshTokenCreateService = Depends(get_jwt_refresh_token_create_service),
):
    user_id = get_user_id_from_refresh_token(token.refresh_token, jwt_service)
    return await token_generator(user_id, jwt_service, jwt_rt_create_service)

@api_router.post("/logout")
async def logout(
        token: TokenRegenerate,
        jwt_service: JwtService = Depends(get_jwt_service),
        jwt_rt_create_service: JwtRefreshTokenCreateService = Depends(get_jwt_refresh_token_create_service),
):
    user_id = get_user_id_from_refresh_token(token.refresh_token, jwt_service)
    await jwt_rt_create_service.disable_tokens_by_user(user_id)

    return {"message": "success"}

def get_new_user_validator(login: str, password: str, user_repo: UserRepository):
    password_validator = PasswordValidator(password)
    unique_login_validator = UniqueLoginValidator(login, user_repo)
    return NewUserValidator(password_validator, unique_login_validator)

def get_user_id_from_refresh_token(
        refresh_token: str,
        jwt_service: JwtService = Depends(get_jwt_service),
):
    payload = jwt_service.decode(refresh_token)

    return payload.get("user_id")

async def token_generator(
        user_id: int,
        jwt_service: JwtService = Depends(get_jwt_service),
        jwt_rt_create_service: JwtRefreshTokenCreateService = Depends(get_jwt_refresh_token_create_service),
):
    payload = {
        "user_id": user_id,
    }

    access_token_expired = datetime.now() + timedelta(seconds=settings.token_settings.token_access_expires)
    access_token = jwt_service.encode(payload, access_token_expired)

    refresh_token_expired = datetime.now() + timedelta(seconds=settings.token_settings.token_refresh_expires)
    refresh_token = jwt_service.encode(payload, refresh_token_expired)

    refresh_token_schema = RefreshTokenModelCreate(
        token=refresh_token,
        expired_at=refresh_token_expired,
        user_id=user_id
    )
    await jwt_rt_create_service.save_new_and_disable_old(refresh_token_schema.model_dump())

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )