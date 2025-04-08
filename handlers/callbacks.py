from aiogram import types, Router, F
import logging

router = Router()

@router.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('кое-что')
    logging.info(f"user {callback.from_user.id} gets random value ")

