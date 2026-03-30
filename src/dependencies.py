import logging

from core.logger import setup_logging

_logger: logging.Logger | None = None


def get_logger() -> logging.Logger:
    global _logger

    if _logger is None:
        _logger = setup_logging('app.log')

    return _logger
