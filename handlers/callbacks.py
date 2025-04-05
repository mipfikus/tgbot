from aiogram import types, Router, F

router = Router()

@router.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('кое-что')
