from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router, types, html

from .callbacks import send_random_value
from .keyboard import get_random_keyboard

router = Router()

@router.message(CommandStart()) # /start
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!")

@router.message(Command("status")) # /status
async def command_status_handler(message: Message) -> None:
    await message.answer(f"username: {html.bold(message.from_user.username)}, id: {html.bold(message.from_user.id)}")

@router.message(Command("help")) # /help
async def command_help_handler(message: Message) -> None:
    help_text = f"""
Привет! Я бот. Вот список доступных команд:

/start - Запускает бота и выводит информацию о пользователе.
/help - Выводит справочную информацию о боте и доступных командах.
/status - Выводит ID и имя пользователя.
/random - Команда выводит кнопку ответ на нажатие которой - сообщение

Разработчики: @yk_rf228, @pashkabesik
    """
    await message.answer(help_text)

@router.message(Command("random"))  # /random - команда в которой используется кнопка под сообщением
async def cmd_random(message: types.Message):
    keyboard = get_random_keyboard()  # Получаем клавиатуру
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил кое-что",
        reply_markup=keyboard
    )

@router.message()
async def echo_handler(message: Message) -> None:

    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
