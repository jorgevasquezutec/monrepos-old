from pydantic_settings import BaseSettings,SettingsConfigDict

__all__ = ("api_settings")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    HOST: str
    PORT: int
    TITLE: str
    PREFIX: str
    SQL_DATABASE_URI: str



api_settings =Settings(_env_file='.env', _env_file_encoding='utf-8')