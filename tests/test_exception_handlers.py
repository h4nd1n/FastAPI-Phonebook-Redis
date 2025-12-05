import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.api.exception_handlers import setup_exception_handlers


@pytest.mark.asyncio
async def test_global_exception_handler_returns_500():
    app = FastAPI()
    setup_exception_handlers(app)

    @app.get("/boom")
    async def boom():
        raise RuntimeError("unexpected")

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/boom")

    assert response.status_code == 500
    assert response.json() == {"detail": "Внутренняя ошибка сервера"}
