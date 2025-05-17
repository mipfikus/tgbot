from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import logging
from .keyboard import get_random_keyboard
from aiogram import types, Router, filters, F
from sqlalchemy import select
from db import async_session, User
from .keyboard import keyboard_start
from sqlalchemy import insert

# информация о статусе
status_string: str = """
UserId: {}
UserName: {}
"""

router = Router()

@router.message(CommandStart()) # /start
async def command_start_handler(message: Message) -> None:
    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        result = await session.execute(query)
        if result.scalars().all():
            info = "Чтобы продолжить, вызовите команду /status"
            await message.answer(info)
        else:
            await  message.answer("Выберите роль", reply_markup=keyboard_start)
    logging.info(f"user {message.from_user.id} starts bot ")

@router.message(Command("status")) # /status
async def command_status_handler(message: Message) -> None:
    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        result = await session.execute(query)
        user = result.scalar()
        if user.tutorcode:
            info = status_string + "Код преподавателя: {}"
            info = info.format(user.user_id, user.username, user.tutorcode)
        if user.subscribe:
            code = str(user.subscribe)
            info = status_string + "Преподаватель: {}"
            query = select(User).where(code == User.tutorcode)
            result = await session.execute(query)
            tutor = result.scalar()
            try:
                info = info.format(user.user_id, user.username, tutor.username)
            except:
                info = info.format(user.user_id, user.username)
        await message.answer(info)
    logging.info(f"user {message.from_user.id} gets status ")

@router.message(F.text.startswith("tutorcode-"))
async def start_student(message):
    async with async_session() as session:
        new_user = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "subscribe": str(message.text.split("-")[1])
        }
        insert_query = insert(User).values(new_user)
        await session.execute(insert_query)
        await session.commit()
        await message.answer("Пользователь добавлен!")
        logging.info(f"Пользователь {message.from_user.username} добавлен в базу данных с ролью слушатель!")

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
    await message.answer(text=help_text)
    logging.info(f"user {message.from_user.id} gets help ")

@router.message(Command("random"))  # /random - команда в которой используется кнопка под сообщением
async def command_random_handler(message: types.Message):
    keyboard = get_random_keyboard()  # Получаем клавиатуру
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил кое-что",
        reply_markup=keyboard
    )
    logging.info(f"user {message.from_user.id} gets random ")

@router.message()
async def echo_handler(message: Message) -> None:

    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
        logging.info(f"user {message.from_user.id} leaves unhandled message")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
        logging.info(f"user {message.from_user.id} leaves unhandled message unsuccessfully")

