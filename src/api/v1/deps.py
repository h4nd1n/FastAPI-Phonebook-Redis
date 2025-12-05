from typing import Annotated

from fastapi import Depends, Request
from redis.asyncio import Redis

from src.services.phonebook_service import PhonebookService
from src.utils.phone import normalize_phone


def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis


def get_key_prefix(request: Request) -> str:
    return request.app.state.config.redis.key_prefix


def get_phonebook_service(
    redis: Annotated[Redis, Depends(get_redis_client)],
    key_prefix: Annotated[str, Depends(get_key_prefix)],
) -> PhonebookService:
    return PhonebookService(redis=redis, key_prefix=key_prefix)


def normalize_phone_param(phone: str) -> str:
    return normalize_phone(phone)
