from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    dsn: PostgresDsn
    pool_size: int


class AppSettings(BaseSettings):
    app_name: str
    database_settings: DatabaseSettings


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


app_settings = AppSettings()
