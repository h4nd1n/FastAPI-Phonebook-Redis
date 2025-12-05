import logging


def setup_logging():
    """
    Настраивает конфигурацию логирования приложения.

    Устанавливает уровень INFO и простое форматирование вывода: файл, строка,
    уровень, время, имя логгера и сообщение.
    """
    log_level = logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
