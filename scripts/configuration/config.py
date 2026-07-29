from pathlib import Path
from urllib.parse import quote_plus

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[0]

class DatabaseSettings(BaseSettings):

    # Database
    host: str
    port: int
    user: str
    password: str
    name: str

    @field_validator('user', 'password', mode='before')
    @classmethod
    def url_encode_credentials(cls, value: str) -> str:
        return quote_plus(value)

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        env_prefix='DATABASE_',
        extra='ignore',
    )

    @property
    def database_url(self: object) -> str:
        return f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}/{self.name}'

class Settings(BaseModel):

    # Configuration settings
    database: DatabaseSettings = DatabaseSettings()

settings = Settings()