from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    # Telegram
    bot_token: str = Field(..., env="BOT_TOKEN")

    # Database
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")

    # Brawl Stars
    brawl_api_token: str = Field(..., env="BRAWL_API_TOKEN")

    # CryptoBot
    cryptobot_token: str = Field(..., env="CRYPTOBOT_TOKEN")
    cryptobot_webhook_secret: str = Field(..., env="CRYPTOBOT_WEBHOOK_SECRET")

    # Admin
    admin_ids: List[int] = Field(default_factory=list, env="ADMIN_IDS")

    # Web
    webhook_host: str = Field("0.0.0.0", env="WEBHOOK_HOST")
    webhook_port: int = Field(8000, env="WEBHOOK_PORT")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:"
            f"{self.db_password}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()