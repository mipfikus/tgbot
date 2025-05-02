import pytest
from main import main
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio
from aiogram.types import BotCommand
from handlers.bot_commands import set_commands
from fixtures import mock_bot, mock_set_commands, mock_dispatcher, mock_callback_router,mock_handler_router, mock_logger

@pytest.mark.asyncio
async def test_set_command_list(mock_bot):
    await set_commands(mock_bot)
    commands = [
        BotCommand(command="/start", description="Запускает бота"),
        BotCommand(command="/help", description="Выводит справочную информацию"),
        BotCommand(command="/status", description="Выводит статус пользователя"),
        BotCommand(command="/random", description="Отправляет сообщение с кнопкой"),
    ]
    mock_bot.set_my_commands.assert_awaited_once_with(commands)


@pytest.mark.asyncio
async def test_main_initialization(mock_bot, mock_dispatcher, mock_handler_router, mock_callback_router, mock_set_commands, mock_logger):
    with patch(target="main.Bot", return_value=mock_bot),patch(target="main.Dispatcher", return_value=mock_dispatcher),patch("handlers.handlers.router", mock_handler_router), patch("handlers.callbacks.router", mock_callback_router):
        await main()

        mock_logger.assert_called_once()
        mock_dispatcher.include_router.assert_any_call(mock_handler_router)
        mock_dispatcher.include_router.assert_any_call(mock_callback_router)
        mock_dispatcher.startup.register.assert_called_once_with(mock_set_commands)
        mock_dispatcher.start_polling.assert_awaited_once_with(mock_bot)
