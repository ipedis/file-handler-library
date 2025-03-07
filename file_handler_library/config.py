from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    storage_type: str
    local_storage_base: str = ''
    key: str
    secret: str
    app_env: str
    storage_url: str | None
    storage_region: str | None
