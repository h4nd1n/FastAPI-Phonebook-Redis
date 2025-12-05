class PhonebookBaseException(Exception):
    """Базовый класс доменных ошибок записной книжки."""


class PhoneNotFoundException(PhonebookBaseException):
    """Вызывается, когда телефона нет в хранилище."""


class PhoneAlreadyExistsException(PhonebookBaseException):
    """Вызывается при попытке создать уже существующий телефон."""


class WrongPhoneFormatException(PhonebookBaseException):
    """Вызывается если передан неверный формат телефона."""
