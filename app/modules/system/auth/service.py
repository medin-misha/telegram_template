"""
Auth-оркестрация системного Telegram-модуля.

Файл реализует базовый flow аутентификации, завязанный на backend telegram API:
сначала bot пытается залогинить пользователя по `telegram_id`, а если backend
ещё не знает этого пользователя, bot регистрирует его и сразу же повторяет
login, после чего кладёт backend payload в in-memory cache.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from aiogram.types import User

from app.modules.system.client import (
    BackendClientError,
    BackendUserNotFoundError,
    get_backend_client,
)
from app.modules.system.schemas import TelegramUserCreatePayload

from .cache import AuthSession, auth_cache

logger = logging.getLogger(__name__)


class AuthenticationFlowError(RuntimeError):
    """Login/register flow не завершился успешной auth-сессией."""


def get_cached_auth_session(telegram_id: int) -> AuthSession | None:
    """Возвращает кешированную auth-сессию пользователя, если она существует."""

    return auth_cache.get(telegram_id)


async def ensure_authenticated(telegram_user: User, no_cache: bool = False) -> AuthSession:
    """Гарантирует auth-сессию пользователя через cache и backend API."""

    cached_session = auth_cache.get(telegram_user.id)
    if no_cache:
        cached_session = None
    if cached_session is not None:
        return cached_session

    client = get_backend_client()

    try:
        backend_user = await client.login_telegram_user(telegram_user.id)
    except BackendUserNotFoundError:
        logger.info("Telegram user %s not found; provisioning via backend.", telegram_user.id)
        await client.create_telegram_user(_build_create_payload(telegram_user))
        backend_user = await client.login_telegram_user(telegram_user.id)
    except BackendClientError:
        raise
    except Exception as exc:
        raise AuthenticationFlowError(
            f"Unexpected authentication failure for user {telegram_user.id}"
        ) from exc
    session = AuthSession(
        telegram_id=telegram_user.id,
        telegram_user=backend_user,
    )
    if not no_cache:
        auth_cache.set(session)
    return session


def _build_create_payload(telegram_user: User) -> TelegramUserCreatePayload:
    """Собирает payload регистрации из Telegram user объекта aiogram."""

    return TelegramUserCreatePayload(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name,
        last_seen_at=datetime.now(UTC),
        is_blocket_bot=telegram_user.is_bot,
        language_code=telegram_user.language_code,
    )
