from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentinel Scope"
    VERSION: str = "0.1.0"
    DEFAULT_SIMULATE: bool = True

    class Config:
        env_prefix = "SS_"


settings = Settings()
