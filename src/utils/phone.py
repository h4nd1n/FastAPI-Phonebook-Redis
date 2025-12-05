import re

from src.core.domain_exceptions import WrongPhoneFormatException


def normalize_phone(raw: str) -> str:
    """
    Нормализует телефон, убирая все символы кроме цифр.

    Бросает ValueError, если длина результата вне диапазона 5–15 цифр.
    """
    digits_only = re.sub(r"\D", "", raw or "")
    if not 5 <= len(digits_only) <= 15:
        raise WrongPhoneFormatException(
            "Номер телефона должен слдержать от 5 до 15 цифр"
        )
    return digits_only
