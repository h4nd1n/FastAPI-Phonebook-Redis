import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.v1.deps import (
    get_phonebook_service,
    normalize_phone_param,
)
from src.schemas.phonebook_schema import (
    PhoneAddressSchema,
    PhoneCreateSchema,
    PhoneUpdateSchema,
)
from src.services.phonebook_service import PhonebookService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/phones", tags=["phonebook"])


@router.get(
    "/{phone}",
    status_code=status.HTTP_200_OK,
    summary="Получить адрес по телефону",
    description="Возвращает адрес, связанный с указанным номером телефона.",
    response_model=PhoneAddressSchema,
    responses={
        status.HTTP_200_OK: {"description": "Адрес найден"},
        status.HTTP_404_NOT_FOUND: {"description": "Телефон не найден"},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Неверный формат телефона"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
)
async def get_address_endpoint(
    phone: Annotated[str, Depends(normalize_phone_param)],
    phonebook_service: Annotated[PhonebookService, Depends(get_phonebook_service)],
):
    return await phonebook_service.get(phone)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Создать связку телефон-адрес",
    description="Сохраняет связку телефон-адрес в Redis. Возвращает созданную запись.",
    response_model=PhoneAddressSchema,
    responses={
        status.HTTP_201_CREATED: {"description": "Адрес создан"},
        status.HTTP_409_CONFLICT: {"description": "Телефон уже существует"},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Неверный формат телефона"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
)
async def create_address_endpoint(
    payload: PhoneCreateSchema,
    phonebook_service: Annotated[PhonebookService, Depends(get_phonebook_service)],
):
    return await phonebook_service.create(phone=payload.phone, address=payload.address)


@router.put(
    "/{phone}",
    status_code=status.HTTP_200_OK,
    summary="Обновить адрес",
    description="Обновляет адрес для указанного телефона.",
    response_model=PhoneAddressSchema,
    responses={
        status.HTTP_200_OK: {"description": "Адрес обновлен"},
        status.HTTP_404_NOT_FOUND: {"description": "Телефон не найден"},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Неверный формат телефона"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
)
async def update_address_endpoint(
    phone: Annotated[str, Depends(normalize_phone_param)],
    payload: PhoneUpdateSchema,
    phonebook_service: Annotated[PhonebookService, Depends(get_phonebook_service)],
):
    return await phonebook_service.update(phone=phone, address=payload.address)


@router.delete(
    "/{phone}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить запись",
    description="Удаляет связку телефон-адрес.",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Адрес удален"},
        status.HTTP_404_NOT_FOUND: {"description": "Телефон не найден"},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Неверный формат телефона"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        },
    },
)
async def delete_address_endpoint(
    phone: Annotated[str, Depends(normalize_phone_param)],
    phonebook_service: Annotated[PhonebookService, Depends(get_phonebook_service)],
):
    await phonebook_service.delete(phone)
