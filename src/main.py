import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from redis.asyncio import Redis

from src.api import api_router
from src.api.exception_handlers import setup_exception_handlers
from src.core.config import Config, load_config
from src.core.logging import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("🚀 Запускаем Phonebook API...")
    config: Config = load_config(path=".env")

    redis = Redis(
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
        password=config.redis.password or None,
        decode_responses=True,
    )
    await redis.ping()

    app.state.config = config
    app.state.redis = redis
    try:
        yield
    finally:
        logger.info("🛑 Останавливаем Phonebook API...")
        close = getattr(redis, "aclose", redis.close)
        await close()


def create_app() -> FastAPI:
    app = FastAPI(title="Phonebook API", version="1.0.0", lifespan=lifespan)
    app.include_router(api_router, tags=["Phonebook API"])
    setup_exception_handlers(app)
    return app


if __name__ == "__main__":
    uvicorn.run("src.main:create_app", host="0.0.0.0", port=8080, factory=True)
