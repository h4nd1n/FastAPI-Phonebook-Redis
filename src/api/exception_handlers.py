import logging

from fastapi import APIRouter, FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse

from src.core.domain_exceptions import (
    PhoneAlreadyExistsException,
    PhoneNotFoundException,
    WrongPhoneFormatException,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["exception"])


async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unexpected error while handling %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка сервера"},
    )


async def phone_not_found_handler(request: Request, exc: PhoneNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Телефон не найден"},
    )


async def phone_already_exists_handler(
    request: Request, exc: PhoneAlreadyExistsException
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Телефон уже существует"},
    )


async def phone_wrong_format_handler(
    request: Request, exc: PhoneAlreadyExistsException
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": "Неверный формат телефона"},
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(PhoneNotFoundException, phone_not_found_handler)
    app.add_exception_handler(PhoneAlreadyExistsException, phone_already_exists_handler)
    app.add_exception_handler(WrongPhoneFormatException, phone_wrong_format_handler)
    app.add_exception_handler(Exception, global_exception_handler)
