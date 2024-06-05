from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class MapStorageHubConfig(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str
    db_url: str
    googlemaps_api_key: str

    model_config = SettingsConfigDict(env_file='hub_api/.env')


@lru_cache
def map_storage_hub_config(env_file: str = 'hub_api/.env') -> MapStorageHubConfig:
    return MapStorageHubConfig(_env_file=env_file)
