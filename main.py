import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import Command

from config import TOKEN
from handlers import bot_commands
from handlers.fsm_order import router as fsm_router
from handlers.callbacks import router as callback_router
from handlers.services import order_handler as handler
from handlers.keyboards import get_clear_edit_keyboard as get_clear_keyboard


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("list"))
async def list_orders(message: Message):
    orders = handler.orders.get_items()
    if not orders:
        await message.answer("📭 Список заказов пуст.")
        return
    text = "\n\n".join(
        [f"🟡 Подбор {id}:\n"
         f"Материал: {o['material']}\n"
         f"Диаметр: {o['diameter']} мм\n"
         f"Глубина: {o['depth']} см\n"
         f"Кол-во: {o['quantity']}\n"
         f"Объём: {round(o['volume'], 4)} м³\n"
         f"Вес: {o['weight']} кг\n"
         f"Цена: {o['price']} ₽"
         for id, o in orders.items()]
    )
    await message.answer(f"📋 Текущий заказ:\n\n{text}", reply_markup=get_clear_keyboard())

@dp.message(Command("clear"))
async def clear_command(message: Message):
    handler.orders.remove_all()
    await message.answer("🗑 Все заказы удалены.")

@dp.message(Command("total"))
async def total_summary(message: Message):
    summary = handler.orders.get_summary()
    if summary["total_quantity"] == 0:
        await message.answer("📭 Заказов пока нет.")
        return

    await message.answer(
        f"<b>📊 Итоги текущего заказа:</b>\n\n"
        f"🔢 Количество отверстий: <b>{summary['total_quantity']}</b>\n"
        f"📦 Общий объём: <b>{summary['total_volume']} м³</b>\n"
        f"⚖️ Общий вес: <b>{summary['total_weight']} кг</b>\n"
        f"💰 Общая цена: <b>{summary['total_price']} ₽</b>"
    )

async def main():
    dp.include_router(fsm_router)
    dp.include_router(callback_router)
    await bot_commands.set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
