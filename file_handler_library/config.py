from pydantic import BaseSettings


class StorageSettings(BaseSettings):
    storage_type: str
    key: str
    secret: str
    app_env: str
    storage_url: str | None
    storage_region: str | None

    class Config:
        env_file = '.env'
