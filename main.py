import uvicorn
from fastapi import FastAPI

from src.api.routers import main_router
from src.core.config import settings
from src.core.error_handler import ErrorHandler
from src.dependencies import get_logger

logger = get_logger()


def init_app() -> FastAPI:
    """
    Initialize and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    # Pass lifespan handler to FastAPI constructor
    app = FastAPI(title=settings.app_title, description=settings.description)

    # Logging
    logger.info("Starting FastAPI server...")

    # Initialize error handler
    ErrorHandler(app, logger)

    # Add routers and apply necessary configurations
    app.include_router(main_router)

    return app


app = init_app()

if __name__ == '__main__':
    uvicorn.run(app, host=settings.host, port=settings.port, log_config=None)
