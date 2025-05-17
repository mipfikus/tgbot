import pytest
from fixtures import mock_message, mock_router, mock_callback
from handlers.callbacks import send_random_value
from handlers.handlers import command_help_handler, command_status_handler, command_start_handler, echo_handler, command_random_handler
from aiogram import html
from aiogram.types import InlineKeyboardMarkup

# Когда тест помечен @pytest.mark.asyncio, он становится сопрограммой (coroutine), вместе с ключевым словом await в теле
# pytest выполнит функцию теста как задачу asyncio, используя цикл событий, предоставляемый фикстурой event_loop
# https://habr.com/ru/companies/otus/articles/337108/

@pytest.mark.asyncio
async def test_command_help_handler(mock_router, mock_message):
    # Вызываем хендлер
    await command_help_handler(mock_message)
    # Проверка, что mock_message был вызван
    assert mock_message.answer.called, "message.answer не был вызван"
    # Проверяем, что mock_ был вызван один раз с ожидаемым результатом
    mock_message.answer.assert_called_once_with(text=f"""
Привет! Я бот. Вот список доступных команд:

/start - Запускает бота и выводит информацию о пользователе.
/help - Выводит справочную информацию о боте и доступных командах.
/status - Выводит ID и имя пользователя.
/random - Команда выводит кнопку ответ на нажатие которой - сообщение

Разработчики: @yk_rf228, @pashkabesik
    """)

@pytest.mark.asyncio
async def test_command_status_handler(mock_router, mock_message):
    # Вызываем хендлер
    await command_status_handler(mock_message)
    # Проверка, что mock_message был вызван
    assert mock_message.answer.called, "message.answer не был вызван"

    called_args, called_kwargs = mock_message.answer.call_args
    assert called_args[0] == f"username: {html.bold(mock_message.from_user.username)}, id: {html.bold(mock_message.from_user.id)}"

@pytest.mark.asyncio
async def test_command_start_handler(mock_router, mock_message):
    # Вызываем хендлер
    await command_start_handler(mock_message)
    # Проверка, что mock_message был вызван
    assert mock_message.answer.called, "message.answer не был вызван"

    called_args, called_kwargs = mock_message.answer.call_args
    assert called_args[0] == f"Привет, {html.bold(mock_message.from_user.full_name)}!"

@pytest.mark.asyncio
async def test_command_random_handler(mock_router, mock_message):
    # Вызываем хендлер
    await command_random_handler(mock_message)
    # Проверка, что mock_message был вызван
    assert mock_message.answer.called, "message.answer не был вызван"
    # Проверяем, что mock_ был вызван один раз с ожидаемым результатом

    called_args, called_kwargs = mock_message.answer.call_args

    assert called_args[0] == "Нажмите на кнопку, чтобы бот отправил кое-что"

    markup = called_kwargs['reply_markup']
    assert isinstance(markup, InlineKeyboardMarkup), 'reply_markup не является Inline-клавиатурой'

@pytest.mark.asyncio
async def test_send_random_value(mock_callback):
    # Вызываем хендлер
    await send_random_value(mock_callback)

    # Проверка, что ответ был отправлен
    assert mock_callback.message.answer.called, "message.answer не был вызван"

    # Проверяем, что ответ содержит ожидаемый текст
    called_args, _ = mock_callback.message.answer.call_args
    assert called_args[0] == 'кое-что'

@pytest.mark.asyncio
async def test_echo(mock_message):
    chat_id = 22222
    mock_message.chat.id = chat_id
    await echo_handler(mock_message)

    mock_message.send_copy.assert_awaited_once_with(chat_id=chat_id)
