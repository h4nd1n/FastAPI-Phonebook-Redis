import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.api import api_router
from src.api.exception_handlers import setup_exception_handlers
from src.core.config import Config, RedisConfig
from src.services.phonebook_service import PhonebookService


class FakeRedis:
    def __init__(self):
        self.storage: dict[str, str] = {}

    async def get(self, key: str):
        return self.storage.get(key)

    async def setnx(self, key: str, value: str) -> bool:
        if key in self.storage:
            return False
        self.storage[key] = value
        return True

    async def set(self, key: str, value: str):
        self.storage[key] = value
        return True

    async def exists(self, key: str) -> int:
        return 1 if key in self.storage else 0

    async def delete(self, key: str) -> int:
        return 1 if self.storage.pop(key, None) is not None else 0

    async def ping(self) -> bool:
        return True

    async def aclose(self):
        return None


@pytest.fixture
def fake_redis():
    return FakeRedis()


@pytest.fixture
def app(fake_redis):
    app = FastAPI()
    app.state.redis = fake_redis
    app.state.config = Config(redis=RedisConfig())
    app.include_router(api_router)
    setup_exception_handlers(app)
    return app


@pytest.fixture
def phonebook_service(fake_redis) -> PhonebookService:
    return PhonebookService(redis=fake_redis)


@pytest_asyncio.fixture
async def client(app):
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c
