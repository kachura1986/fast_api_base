from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the application.
    """
    # Application settings
    app_title: str = "FastAPI"
    description: str = "The FastAPI application."
    host: str = '127.0.0.1'
    port: int = 8000

    # Settings
    environment: str

    class Config:
        extra = 'ignore'


settings = Settings()
