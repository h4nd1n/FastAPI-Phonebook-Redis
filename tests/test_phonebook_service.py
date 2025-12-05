import pytest

from src.core.domain_exceptions import (
    PhoneAlreadyExistsException,
    PhoneNotFoundException,
    WrongPhoneFormatException,
)


@pytest.mark.asyncio
async def test_service_create_and_get(phonebook_service, fake_redis):
    created = await phonebook_service.create("+1 (555) 222-33-44", "Где-то")

    assert created.phone == "15552223344"
    assert created.address == "Где-то"

    fetched = await phonebook_service.get("1-555-222-33-44")
    assert fetched.phone == "15552223344"
    assert fetched.address == "Где-то"
    assert fake_redis.storage["phonebook:15552223344"] == "Где-то"


@pytest.mark.asyncio
async def test_service_create_conflict(phonebook_service, fake_redis):
    fake_redis.storage["phonebook:12345"] = "Сохранено"

    with pytest.raises(PhoneAlreadyExistsException):
        await phonebook_service.create("12345", "Other")


@pytest.mark.asyncio
async def test_service_get_missing(phonebook_service):
    with pytest.raises(PhoneNotFoundException):
        await phonebook_service.get("00000")


@pytest.mark.asyncio
async def test_service_update_existing(phonebook_service, fake_redis):
    fake_redis.storage["phonebook:88888"] = "Старый"

    updated = await phonebook_service.update("88888", "Новый")

    assert updated.address == "Новый"
    assert fake_redis.storage["phonebook:88888"] == "Новый"


@pytest.mark.asyncio
async def test_service_update_missing(phonebook_service):
    with pytest.raises(PhoneNotFoundException):
        await phonebook_service.update("99999", "Ничего")


@pytest.mark.asyncio
async def test_service_delete(phonebook_service, fake_redis):
    fake_redis.storage["phonebook:10101"] = "tmp"

    await phonebook_service.delete("10101")

    assert "phonebook:10101" not in fake_redis.storage


@pytest.mark.asyncio
async def test_service_delete_missing(phonebook_service):
    with pytest.raises(PhoneNotFoundException):
        await phonebook_service.delete("22222")


@pytest.mark.asyncio
async def test_service_rejects_invalid_phone(phonebook_service):
    with pytest.raises(WrongPhoneFormatException):
        await phonebook_service.create("12", "Bad")
