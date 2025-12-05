import pytest

from src.utils.phone import normalize_phone


@pytest.mark.asyncio
async def test_create_phone_201(client, fake_redis):
    payload = {"phone": "+7 (999) 123-45-67", "address": "Москва, Красная площадь"}

    response = await client.post("/api/v1/phones", json=payload)

    assert response.status_code == 201
    assert response.json() == {
        "phone": "79991234567",
        "address": "Москва, Красная площадь",
    }
    assert (
        fake_redis.storage[f"phonebook:{normalize_phone(payload['phone'])}"]
        == payload["address"]
    )


@pytest.mark.asyncio
async def test_create_phone_conflict_409(client, fake_redis):
    phone = "1234567890"
    fake_redis.storage[f"phonebook:{phone}"] = "Old address"

    response = await client.post(
        "/api/v1/phones", json={"phone": phone, "address": "Новый адрес"}
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Телефон уже существует"


@pytest.mark.asyncio
async def test_get_phone_200(client, fake_redis):
    phone = "380971112233"
    fake_redis.storage[f"phonebook:{phone}"] = "РОССИЯ"

    response = await client.get(f"/api/v1/phones/{phone}")

    assert response.status_code == 200
    assert response.json() == {"phone": phone, "address": "РОССИЯ"}


@pytest.mark.asyncio
async def test_get_phone_404(client):
    response = await client.get("/api/v1/phones/00000")

    assert response.status_code == 404
    assert response.json()["detail"] == "Телефон не найден"


@pytest.mark.asyncio
async def test_update_phone_200(client, fake_redis):
    phone = "15551234567"
    fake_redis.storage[f"phonebook:{phone}"] = "Старый"

    response = await client.put(
        f"/api/v1/phones/{phone}", json={"address": "Обновленный адрес"}
    )

    assert response.status_code == 200
    assert response.json() == {"phone": phone, "address": "Обновленный адрес"}
    assert fake_redis.storage[f"phonebook:{phone}"] == "Обновленный адрес"


@pytest.mark.asyncio
async def test_update_phone_404(client):
    response = await client.put(
        "/api/v1/phones/11111", json={"address": "Не должен сохраниться"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Телефон не найден"


@pytest.mark.asyncio
async def test_delete_phone_204(client, fake_redis):
    phone = "441234567890"
    fake_redis.storage[f"phonebook:{phone}"] = "Лондон"

    response = await client.delete(f"/api/v1/phones/{phone}")

    assert response.status_code == 204
    assert f"phonebook:{phone}" not in fake_redis.storage


@pytest.mark.asyncio
async def test_delete_phone_404(client):
    response = await client.delete("/api/v1/phones/12345")

    assert response.status_code == 404
    assert response.json()["detail"] == "Телефон не найден"


@pytest.mark.asyncio
async def test_invalid_phone_validation(client):
    response = await client.post(
        "/api/v1/phones", json={"phone": "abc", "address": "Nowhere"}
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_phone_wrong_format_422(client):
    response = await client.get("/api/v1/phones/1234")

    assert response.status_code == 422
    assert response.json()["detail"] == "Неверный формат телефона"


@pytest.mark.asyncio
async def test_update_phone_wrong_format_422(client):
    response = await client.put("/api/v1/phones/12-34", json={"address": "Не важно"})

    assert response.status_code == 422
    assert response.json()["detail"] == "Неверный формат телефона"


@pytest.mark.asyncio
async def test_delete_phone_wrong_format_422(client):
    response = await client.delete("/api/v1/phones/abcd")

    assert response.status_code == 422
    assert response.json()["detail"] == "Неверный формат телефона"
