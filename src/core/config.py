from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the application."""
    model_config = SettingsConfigDict(extra='ignore')

    # Application settings
    APP_TITLE: str = "FastAPI"
    DESCRIPTION: str = "The FastAPI application."
    HOST: str = '127.0.0.1'
    PORT: int = 8000

    # Temporary files
    TEMP_DIR: Path = Path(__file__).resolve().parents[2] / '.temp'
    LOGS_DIR: Path = TEMP_DIR / 'logs'


settings = Settings()
