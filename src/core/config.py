import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_password: str
    db_username: str
    db_echo: bool

    bot_token: SecretStr

    scraping_interval_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=f"{os.path.dirname(os.path.abspath(__file__))}/../../.env",
        extra="ignore",
    )

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.db_username}:"
            f"{self.db_password}@{self.db_hostname}:"
            f"{self.db_port}/{self.db_name}"
        )


settings = Settings()
