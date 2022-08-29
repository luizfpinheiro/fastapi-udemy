from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Application configs 
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/faculdade"

    class Config:
        case_sensitive = True


settings = Settings()
