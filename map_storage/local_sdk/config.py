from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class LocalMapStorageConfig(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str
    db_url: str

    model_config = SettingsConfigDict(env_file='../../local_sdk/.env')


@lru_cache
def local_map_storage_config(env_file: str = '.env') -> LocalMapStorageConfig:
    return LocalMapStorageConfig(_env_file=env_file)
