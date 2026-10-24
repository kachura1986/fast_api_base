from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the application."""
    model_config = SettingsConfigDict(extra='ignore')

    # Application settings
    APP_TITLE: str = "FastAPI"
    DESCRIPTION: str = "The FastAPI application."
    HOST: str = '127.0.0.1'
    PORT: int = 8000


settings = Settings()
