from fastapi import APIRouter

from .health import router as health_router
from .v1.phonebook import router as phonebook_router

api_router = APIRouter(prefix="/api")

api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(phonebook_router, prefix="/v1", tags=["phonebook"])
