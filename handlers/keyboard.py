from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get_random_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    return builder.as_markup()