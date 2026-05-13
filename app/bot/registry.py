"""
Явный реестр модульных роутеров.

Все активные Telegram-модули подключаются здесь вручную, чтобы состав
приложения был прозрачен и легко отслеживался при отладке и развитии шаблона.
"""

from aiogram import Dispatcher

from app.modules.rmq_module.handlers import router as rmq_router
from app.modules.system.handlers import router as system_router


def register_routers(dispatcher: Dispatcher) -> None:
    """Подключает активные модульные роутеры к общему dispatcher."""

    dispatcher.include_router(system_router)
    dispatcher.include_router(rmq_router)
