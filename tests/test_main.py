import pytest
from httpx import ASGITransport, AsyncClient

from src import main
from src.core.config import Config, RedisConfig


class DummyRedis:
    def __init__(self):
        self.ping_called = False
        self.closed = False

    async def ping(self):
        self.ping_called = True
        return True

    async def aclose(self):
        self.closed = True
        return None

    async def close(self):
        return await self.aclose()


@pytest.mark.asyncio
async def test_create_app_uses_lifespan(monkeypatch):
    dummy_redis = DummyRedis()
    monkeypatch.setattr(
        main, "load_config", lambda path=".env": Config(redis=RedisConfig())
    )
    monkeypatch.setattr(main, "Redis", lambda **kwargs: dummy_redis)

    app = main.create_app()

    async with app.router.lifespan_context(app):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            response = await client.get("/api/health")

    assert response.status_code == 200
    assert dummy_redis.ping_called
    assert dummy_redis.closed
