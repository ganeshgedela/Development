from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_ENGINE: str = "postgres"
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "tracenova"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
