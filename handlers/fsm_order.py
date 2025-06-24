from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from handlers.states import OrderFSM, EditFSM
from handlers.services import order_handler as handler
from handlers.keyboards import (
    get_material_keyboard,
    get_back_keyboard
)

MIN_DIAMETER = 18
MAX_DIAMETER = 800

router = Router()

# ▶ START FSM ДЛЯ ДОБАВЛЕНИЯ ЗАКАЗА

@router.message(F.text == "/add")
async def start_order(message: Message, state: FSMContext):
    await message.answer("Выберите материал:", reply_markup=get_material_keyboard())
    await state.set_state(OrderFSM.material)

@router.callback_query(F.data.startswith("material_"))
async def material_selected(callback: CallbackQuery, state: FSMContext):
    material = callback.data.split("_", 1)[1]
    await state.update_data(material=material)
    await callback.message.answer(
        "Введите диаметр отверстия в мм (например, 52):",
        reply_markup=get_back_keyboard("material")
    )
    await state.set_state(OrderFSM.diameter)
    await callback.answer()

@router.message(OrderFSM.diameter)
async def get_diameter(message: Message, state: FSMContext):
    try:
        diameter = int(message.text)
        if diameter < MIN_DIAMETER or diameter > MAX_DIAMETER:
            await message.answer(
                f"⚠️ Диаметр должен быть от {MIN_DIAMETER} до {MAX_DIAMETER} мм. Попробуйте ещё раз."
            )
            return
        await state.update_data(diameter=diameter)
        await message.answer("Введите глубину отверстия в см:", reply_markup=get_back_keyboard("diameter"))
        await state.set_state(OrderFSM.depth)
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число.")

@router.message(OrderFSM.depth)
async def get_depth(message: Message, state: FSMContext):
    await state.update_data(depth=int(message.text))
    await message.answer("Введите количество отверстий:", reply_markup=get_back_keyboard("depth"))
    await state.set_state(OrderFSM.quantity)

@router.message(OrderFSM.quantity)
async def finish_order(message: Message, state: FSMContext):
    await state.update_data(quantity=int(message.text))
    data = await state.get_data()

    handler.handle_orders(
        data["material"],
        data["diameter"],
        data["depth"],
        data["quantity"]
    )

    await message.answer("✅ Заказ добавлен.")
    await state.clear()

@router.callback_query(F.data == "back_to_material")
async def back_to_material(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите материал:", reply_markup=get_material_keyboard())
    await state.set_state(OrderFSM.material)
    await callback.answer()

@router.callback_query(F.data == "back_to_diameter")
async def back_to_diameter(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите диаметр отверстия в мм:", reply_markup=get_back_keyboard("material"))
    await state.set_state(OrderFSM.diameter)
    await callback.answer()

@router.callback_query(F.data == "back_to_depth")
async def back_to_depth(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите глубину отверстия в см:", reply_markup=get_back_keyboard("diameter"))
    await state.set_state(OrderFSM.depth)
    await callback.answer()

@router.message(EditFSM.waiting_for_new_value)
async def handle_new_value(message: Message, state: FSMContext):
    data = await state.get_data()
    item_id = data.get("item_id")
    field = data.get("field")

    try:
        new_value = int(message.text)
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число.")
        return

    if field == "diameter" and (new_value < MIN_DIAMETER or new_value > MAX_DIAMETER):
        await message.answer(
            f"⚠️ Диаметр должен быть от {MIN_DIAMETER} до {MAX_DIAMETER} мм. Попробуйте ещё раз."
        )
        return

    handler.orders.update_item_field(item_id, field, new_value)

    field_names = {
        "diameter": "диаметр",
        "depth": "глубину",
        "quantity": "количество"
    }
    field_rus = field_names.get(field, field)

    await message.answer(f"✅ {field_rus.capitalize()} успешно обновлено для Подбора {item_id}")
    await state.clear()
