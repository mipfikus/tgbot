from aiogram import Router, F
from aiogram.types import CallbackQuery
from handlers.services import order_handler as handler
from handlers.keyboards import get_edit_select_keyboard, get_edit_fields_keyboard
from aiogram.fsm.context import FSMContext
from handlers.states import EditFSM

router = Router()

@router.callback_query(F.data == "clear_orders")
async def clear_orders(callback: CallbackQuery):
    handler.orders.remove_all()
    await callback.message.answer("🗑 Заказы очищены.")
    await callback.answer()

@router.callback_query(F.data == "edit_orders")
async def edit_orders_menu(callback: CallbackQuery):
    order_ids = list(handler.orders.get_items().keys())
    if not order_ids:
        await callback.message.answer("❗Нет заказов для редактирования.")
        await callback.answer()
        return
    await callback.message.answer(
        "Выберите подбор для редактирования:",
        reply_markup=get_edit_select_keyboard(order_ids)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("edit_"))
async def edit_order(callback: CallbackQuery):
    item_id = int(callback.data.split("_")[1])
    await callback.message.answer(
        f"Что вы хотите изменить в Подборе {item_id}?",
        reply_markup=get_edit_fields_keyboard(item_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("update_"))
async def update_field(callback: CallbackQuery, state: FSMContext):
    _, item_id, field = callback.data.split("_")
    await state.update_data(item_id=int(item_id), field=field)
    await callback.message.answer(f"Введите новое значение для {field}:")
    await state.set_state(EditFSM.waiting_for_new_value)
    await callback.answer()
