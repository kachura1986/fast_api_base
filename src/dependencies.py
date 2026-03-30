import logging
from functools import lru_cache

from core.logger import setup_logging


# --- Dependency Providers ---
@lru_cache()
def get_logger() -> logging.Logger:
    return setup_logging('app.log')
