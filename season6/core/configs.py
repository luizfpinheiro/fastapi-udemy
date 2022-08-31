from typing import List

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/faculdade"
    DB_BASE_MODEL = declarative_base()

    JWT_SECRET: str = 'N1bJ7xnV4XbSYadP9ZcOcyIIYVXc2hZeIqfy8-f5xxk' # created by python.secrets
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 4  # 1 week
    """
    # Generate token
    import secrets
    token: str = secrets.token_urlsafe(32)
    """
    class Config:
        case_sensitive = True


settings = Settings()
