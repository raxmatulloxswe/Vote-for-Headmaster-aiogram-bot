from typing import Callable, Dict, Any, Awaitable
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Update, User, ChatMember
from aiogram import BaseMiddleware, Bot

import config
from app.keyboards.inline import inline_subscribe


EVENT_FROM_USER = 'event_from_user'


class CheckSubscriptionMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data['bot']
        user: User = data.get(EVENT_FROM_USER)

        chat_member: ChatMember = await bot.get_chat_member(chat_id=config.SUBSCRIPTION_CHANNEL_ID, user_id=user.id)
        print(chat_member)
        try:
            if chat_member.status not in ("member", "administrator", "creator"):
                return await bot.send_message(chat_id=user.id, text="Iltimos, kanalga obuna bo'ling!", reply_markup=inline_subscribe())

        except TelegramBadRequest as e:
            if "chat not found" in str(e):
                return await bot.send_message(chat_id=user.id, text="Kanal topilmadi yoki bot kanalga ulanmagan!")
            else:
                return await bot.send_message(chat_id=user.id, text=f"Kutilmagan xato: {e}")

        return await handler(event, data)
