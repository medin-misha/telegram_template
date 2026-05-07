"""
Локальные Pydantic-схемы системного Telegram-модуля.

Системный модуль использует эти схемы как контракт с backend API, не импортируя
напрямую код из `fastapi_template`. Это снижает связность между двумя
шаблонами и позволяет развивать bot/runtime отдельно от backend-репозитория.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserProfileRead(BaseModel):
    """Минимальная read-схема профиля пользователя из backend."""

    model_config = ConfigDict(extra="ignore")

    id: int
    telegram_user_id: int
    phone: str | None = None
    email: str | None = None
    timezone: str | None = None
    full_name: str | None = None
    note: str | None = None
    created_at: datetime
    updated_at: datetime


class TelegramUserLoginPayload(BaseModel):
    """Payload для запроса логина пользователя через backend."""

    telegram_id: int


class TelegramUserCreatePayload(BaseModel):
    """Payload для регистрации Telegram-пользователя через backend."""

    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    last_seen_at: datetime | None = None
    is_blocket_bot: bool = False
    language_code: str | None = None


class TelegramUserRead(BaseModel):
    """Ответ backend с данными Telegram-пользователя и профиля."""

    model_config = ConfigDict(extra="ignore")

    id: int
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    last_seen_at: datetime | None = None
    is_blocket_bot: bool = False
    language_code: str | None = None
    created_at: datetime
    updated_at: datetime
    user_profile: UserProfileRead | None = None
