from redis.asyncio import Redis

from src.core.domain_exceptions import (
    PhoneAlreadyExistsException,
    PhoneNotFoundException,
)
from src.schemas.phonebook_schema import PhoneAddressSchema
from src.utils.phone import normalize_phone


class PhonebookService:
    """
    Инкапсулирует операции телефон→адрес поверх Redis.
    """

    def __init__(self, redis: Redis, key_prefix: str = "phonebook:"):
        self.redis = redis
        self.key_prefix = key_prefix

    @staticmethod
    def _normalize(phone: str) -> str:
        return normalize_phone(phone)

    def _make_key(self, normalized_phone: str) -> str:
        return f"{self.key_prefix}{normalized_phone}"

    async def get(self, phone: str) -> PhoneAddressSchema:
        normalized = self._normalize(phone)
        address = await self.redis.get(self._make_key(normalized))
        if address is None:
            raise PhoneNotFoundException()
        return PhoneAddressSchema(phone=normalized, address=address)

    async def create(self, phone: str, address: str) -> PhoneAddressSchema:
        normalized = self._normalize(phone)
        created = await self.redis.setnx(self._make_key(normalized), address)
        if not created:
            raise PhoneAlreadyExistsException()
        return PhoneAddressSchema(phone=normalized, address=address)

    async def update(self, phone: str, address: str) -> PhoneAddressSchema:
        normalized = self._normalize(phone)
        exists = await self.redis.exists(self._make_key(normalized))
        if not exists:
            raise PhoneNotFoundException()
        await self.redis.set(self._make_key(normalized), address)
        return PhoneAddressSchema(phone=normalized, address=address)

    async def delete(self, phone: str) -> None:
        normalized = self._normalize(phone)
        deleted = await self.redis.delete(self._make_key(normalized))
        if deleted == 0:
            raise PhoneNotFoundException()
