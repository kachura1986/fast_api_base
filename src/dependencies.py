import logging

from src.core.logger import setup_logging

# --- Logging ---
_logger = setup_logging('app.log')


# --- Dependency Providers ---
def get_logger() -> logging.Logger:
    return _logger
