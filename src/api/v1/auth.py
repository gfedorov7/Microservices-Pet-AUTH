import json
from datetime import datetime, timedelta
from typing import Any, Coroutine

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.requests import Request

from src.config import settings
from src.dependency.cache.redis_cache import get_redis_cache
from src.dependency.producer.kafka_producer import get_my_kafka_producer
from src.dependency.repository.user_repository import get_user_repo
from src.dependency.service.jwt_refresh_token_create_service import get_jwt_refresh_token_create_service
from src.dependency.service.jwt_service import get_jwt_service
from src.dependency.service.user_auth_service import get_user_auth_service
from src.dependency.service.user_create_service import get_user_create_service
from src.model.user import User
from src.repository.user_repository import UserRepository
from src.schemas.refresh_token import RefreshTokenModelCreate
from src.schemas.token import Token, TokenRegenerate
from src.schemas.user import UserCreate, UserLogin, UserRead
from src.service.jwt_refresh_token_create_service import JwtRefreshTokenCreateService
from src.service.jwt_service import JwtService
from src.service.user_auth_service import UserAuthService
from src.service.user_create_service import UserCreateService
from src.util.cache.cache import Cache
from src.util.enum.available_type import AvailableType
from src.util.exception.app_exception import AppException
from src.util.producer.producer import Producer
from src.util.validator.new_user_validator import NewUserValidator
from src.util.validator.password_validator import PasswordValidator
from src.util.validator.unique_login_validator import UniqueLoginValidator


api_router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBearer()

@api_router.post("/sign-up")
async def sign_up(
        request: Request,
        user_in: UserCreate,
        producer: Producer = Depends(get_my_kafka_producer),
        user_repo: UserRepository = Depends(get_user_repo),
        jwt_rt_create_service: JwtRefreshTokenCreateService = Depends(get_jwt_refresh_token_create_service),
        jwt_service: JwtService = Depends(get_jwt_service),
        user_create_service: UserCreateService = Depends(get_user_create_service)
):
    try:
        new_user_validator = get_new_user_validator(user_in.login, user_in.password, user_repo)
        new_user = await user_create_service.create_user(user_in.model_dump(), new_user_validator)
        token = await token_generator(new_user.id, jwt_service, jwt_rt_create_service)
        await event(request, "success-auth", AvailableType.user_signed_up,
              jwt_service, producer, token.access_token)
        return token
    except AppException:
        await event(request, "unsuccess-auth",
                    AvailableType.user_login_failed, jwt_service, producer)
        raise

@api_router.post("/login")
async def login(
        request: Request,
        user_in: UserLogin,
        producer: Producer = Depends(get_my_kafka_producer),
        auth_service: UserAuthService = Depends(get_user_auth_service),
        jwt_service: JwtService = Depends(get_jwt_service),
        jwt_rt_create_service: JwtRefreshTokenCreateService = Depends(get_jwt_refresh_token_create_service),
):
    try:
        user = await auth_service.login(user_in.model_dump())
        token = await token_generator(user.id, jwt_service, jwt_rt_create_service)
        await event(request, "success-login",
                    AvailableType.user_logged_in, jwt_service,
                    producer, token.access_token)
        return token
    except AppException:
        await event(request, "unsuccess-login",
                    AvailableType.user_login_failed, jwt_service, producer)
        raise

@api_router.post("/refresh")
async def refresh(
        token: TokenRegenerate,
        jwt_service: JwtService = Depends(get_jwt_service),
        jwt_rt_create_service: JwtRefreshTokenCreateService = Depends(get_jwt_refresh_token_create_service),
):
    user_id = get_user_id_from_token(token.refresh_token, jwt_service)
    await jwt_rt_create_service.check_valid_for_user_refresh_token(user_id, token.refresh_token)
    return await token_generator(user_id, jwt_service, jwt_rt_create_service)

@api_router.post("/logout")
async def logout(
        request: Request,
        token: TokenRegenerate,
        producer: Producer = Depends(get_my_kafka_producer),
        jwt_service: JwtService = Depends(get_jwt_service),
        jwt_rt_create_service: JwtRefreshTokenCreateService = Depends(get_jwt_refresh_token_create_service),
):
    user_id = get_user_id_from_token(token.refresh_token, jwt_service)
    await jwt_rt_create_service.disable_tokens_by_user(user_id, token.refresh_token)
    await event(request, "success-logout", AvailableType.user_logged_out, jwt_service, producer)
    return {"message": "success"}

@api_router.get("/me")
async def me(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        jwt_service: JwtService = Depends(get_jwt_service),
        user_repo: UserRepository = Depends(get_user_repo),
        cache: Cache = Depends(get_redis_cache)
) -> UserRead:
    access_token = credentials.credentials
    user_id = get_user_id_from_token(access_token, jwt_service)

    return await get_or_set_to_cache_user_by_id(user_id, user_repo, cache)

async def event(
        request: Request,
        title: str,
        available_type: AvailableType,
        jwt_service: JwtService,
        producer: Producer,
        access_token: str = None,
        anonymous_user_id: str = None,
):
    user_id = None
    if access_token:
        user_id = get_user_id_from_token(access_token, jwt_service)

    payload = {
        "user_id": user_id,
        "anonymus_user_id": anonymous_user_id,
        "type": available_type.value,
        "timestamp": datetime.now().isoformat(),
        "user-agent": request.headers.get("user-agent"),
        "ip": get_ip(request),
    }

    producer.send(title, payload)

def get_new_user_validator(login: str, password: str, user_repo: UserRepository):
    password_validator = PasswordValidator(password)
    unique_login_validator = UniqueLoginValidator(login, user_repo)
    return NewUserValidator(password_validator, unique_login_validator)

def get_user_id_from_token(
        token: str,
        jwt_service: JwtService = Depends(get_jwt_service),
):
    payload = jwt_service.decode(token)

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

async def get_or_set_to_cache_user_by_id(
        user_id: int,
        user_repo: UserRepository,
        cache: Cache,
) -> UserRead:
    user_cache_key = f"user:{user_id}"
    user = await cache.get(user_cache_key)
    if user:
        return UserRead.model_validate_json(user)

    user = await user_repo.get_by_id(user_id)
    user_schema = UserRead(**user.to_dict())
    await cache.set(user_cache_key, user_schema.model_dump_json())
    return user_schema

def get_ip(request):
    x_forwarded_for = request.headers.get("x-forwarded-for")

    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]

    return request.client.host