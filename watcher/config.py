from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)

    API_KEY: str
    DELAY: int = 300
    MAX_RETRIES: int = 5


settings = Settings()
