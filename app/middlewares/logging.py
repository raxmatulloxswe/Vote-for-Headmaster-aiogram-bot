from typing import Callable, Dict, Any, Awaitable

from aiogram.types import Update
from aiogram import BaseMiddleware

from loguru import logger


class LoggingMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        logger.info(f"Receive update {event}")
        return await handler(event, data)


__all__ = [
    'LoggingMiddleware'
]
