import pytest

from src.core.domain_exceptions import WrongPhoneFormatException
from src.utils.phone import normalize_phone


def test_normalize_phone_strips_and_keeps_digits():
    assert normalize_phone("+1 (234) 567-8900") == "12345678900"


@pytest.mark.parametrize("raw", ["1234", "1" * 16, "", None])
def test_normalize_phone_invalid_length(raw):
    with pytest.raises(WrongPhoneFormatException):
        normalize_phone(raw)
