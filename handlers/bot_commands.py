from aiogram.types import BotCommand
from aiogram import Bot

async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="add", description="Добавить заказ"),
        BotCommand(command="list", description="Показать заказы"),
        BotCommand(command="clear", description="Очистить список заказов"),
        BotCommand(command="total", description="Итоги заказа"),
    ]
    await bot.set_my_commands(commands)
