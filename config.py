from pydantic_settings import BaseSettings
from pydantic.v1 import Field
from typing import Dict


class Settings(BaseSettings):
    active_profile: str = Field(..., env='ACTIVE_PROFILE')
    url_database_local: str = Field(..., env='URL_DATABASE_LOCAL')
    url_database_dev: str = Field(..., env='URL_DATABASE_DEV')
    url_database_production: str = Field(..., env='URL_DATABASE_PRODUCTION')

    @property
    def database_urls(self) -> Dict[str, str]:
        return {
            "local": self.url_database_local,
            "dev": self.url_database_dev,
            "production": self.url_database_production,
        }

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
