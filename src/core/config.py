from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the application.
    """
    model_config = SettingsConfigDict(extra='ignore')

    # Application settings
    app_title: str = "FastAPI"
    description: str = "The FastAPI application."
    host: str = '127.0.0.1'
    port: int = 8000


settings = Settings()
