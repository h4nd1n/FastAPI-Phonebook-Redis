from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.utils.phone import normalize_phone


class PhoneBase(BaseModel):
    phone: str = Field(min_length=5, max_length=20)
    address: str = Field(min_length=1, max_length=500)

    model_config = ConfigDict(extra="forbid")

    @field_validator("phone")
    @classmethod
    def _normalize_phone(cls, value: str) -> str:
        return normalize_phone(value)


class PhoneCreateSchema(PhoneBase):
    """Данные для создания связки телефон-адрес."""


class PhoneUpdateSchema(BaseModel):
    address: str = Field(min_length=1, max_length=500)

    model_config = ConfigDict(extra="forbid")


class PhoneAddressSchema(PhoneBase):
    """Модель ответа со связкой телефон-адрес."""
