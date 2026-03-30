import logging
from functools import wraps

from tenacity import after_log, before_sleep_log, retry, stop_after_attempt, wait_exponential

from dependencies import get_logger


def retry_strategy(func):
    """Wrapper for retry strategy."""

    logger = get_logger()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        after=after_log(logger, logging.INFO),
    )
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper
