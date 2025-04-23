from aiogram.types import InlineKeyboardMarkup

import pytest
from fixtures import mock_message, mock_router
from tgbot.handlers.handlers import command_random_handler

@pytest.mark.asyncio
async def test_command_random_handler(mock_router, mock_message):
    # Вызываем хендлер
    await command_random_handler(mock_message)
    # Проверка, что mock_message был вызван
    assert mock_message.answer.called, "message.answer не был вызван"
    # Проверяем, что mock_ был вызван один раз с ожидаемым результатом


    called_args, called_kwargs = mock_message.answer.call_args
    assert called_args[0] == "Нажмите на кнопку, чтобы бот отправил кое-что"

    # markup = called_kwargs['reply_markup']
    # assert isinstance(markup, InlineKeyboardMarkup), "reply_markup не является"
