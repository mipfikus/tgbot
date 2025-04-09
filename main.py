# version 1.0.0
import asyncio
import logging
import sys
from config import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from utils import setup_logger

from handlers import handlers
from handlers import callbacks
from handlers.bot_commands import set_commands

dp = Dispatcher()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_router(handlers.router)
    dp.include_router(callbacks.router)
    dp.startup.register(set_commands)


    # запуск логирования
    setup_logger(fname=__name__)

    await dp.start_polling(bot)

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())