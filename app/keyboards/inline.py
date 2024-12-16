from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.callback_data import cb_main_menu_callback_data, MainMenuAction, cb_back_to_main_menu_callback_data
from app.utils.db_manager import db


def inline_back_to_main_menu():
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text='Asosiy menu', callback_data=cb_back_to_main_menu_callback_data())

    return inline_keyboard.as_markup()


async def inline_main_menu():
    directors = await db.get_directors()
    inline = InlineKeyboardBuilder()

    for director in directors:
        button_text = f"{director['school_number']} - {director['name']} - {director['score']}"
        inline.button(
            text=button_text,
            callback_data=f"director_{director['id']}"
        )
    inline.adjust(1)
    return inline.as_markup()


def inline_subscribe():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.button(text="🔗Kanalga a'zo bo'lish", url='https://t.me/raxmatulloxs_log')

    # Foydalanuvchiga obuna holatini tekshirish imkoniyatini beruvchi tugma
    inline_keyboard.button(text='''✅ Obuna bo'ldim''', callback_data='check_subscription')

    inline_keyboard.adjust(1)
    return inline_keyboard.as_markup()
