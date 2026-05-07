"""
Центральная конфигурация Telegram-приложения.

Этот файл является единственной точкой чтения общего `.env` и хранит как
настройки самого бота, так и общие параметры интеграции с backend, которые
дальше проецируются в модульные конфиги.
"""

from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class MainSettings(BaseSettings):
    """Общие настройки процесса Telegram-бота."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    project_name: str = "Telegram Template"
    debug: bool = Field(default=False, validation_alias=AliasChoices("DEBUG", "debug"))
    token: SecretStr = Field(validation_alias="TOKEN")
    backend_url: str | None = Field(default=None, validation_alias="BACKEND_URL")
    backend_api_prefix: str = Field(default="/api", validation_alias="BACKEND_API_PREFIX")
    backend_request_timeout: float = Field(
        default=10.0,
        validation_alias="BACKEND_REQUEST_TIMEOUT",
    )
    auth_cache_max_size: int = Field(default=1000, validation_alias="AUTH_CACHE_MAX_SIZE")
    bot_parse_mode: str = Field(default="HTML", validation_alias="BOT_PARSE_MODE")

    @property
    def bot_token(self) -> str:
        """Возвращает сырой токен в формате, который нужен aiogram."""

        return self.token.get_secret_value()


settings = MainSettings()
