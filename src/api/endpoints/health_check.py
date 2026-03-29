from fastapi import APIRouter, Depends

from src.core.config import settings
from src.dependencies import get_logger

router = APIRouter()


@router.get('', response_model=str)
def health_check(logger=Depends(get_logger)) -> str:
    """Check that the API is running and ready to receive requests.

    Args:
        logger (logging.Logger): Logger instance for logging messages.

    Returns:
        str: A string indicating the status of the application.
    """
    message = f"'{settings.app_title}' is running"

    logger.info(message)

    return message
