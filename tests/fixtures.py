import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import Message, CallbackQuery
from aiogram import Router

@pytest.fixture
def mock_message():
    """Mock сообщение"""
    mock_msg = AsyncMock(spec=Message)
    mock_msg.answer = AsyncMock()
    mock_msg.from_user = AsyncMock()
    mock_msg.from_user.id = AsyncMock()
    mock_msg.from_user.username = AsyncMock()
    mock_msg.chat = AsyncMock()
    mock_msg.send_copy = AsyncMock()

    return mock_msg

@pytest.fixture
def mock_callback():
    mock = MagicMock(spec=CallbackQuery)
    mock.message = MagicMock()
    mock.message.answer = AsyncMock()
    mock.from_user = MagicMock()
    mock.data = "send_random_value"
    mock.from_user.username = "test_user"
    return mock

@pytest.fixture
def mock_router():
    """Mock роутер"""
    router = Router()
    return router