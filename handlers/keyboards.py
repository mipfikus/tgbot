from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_material_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Кирпич", callback_data="material_кирпич")],
            [InlineKeyboardButton(text="Бетон", callback_data="material_бетон")],
            [InlineKeyboardButton(text="Железобетон", callback_data="material_железобетон")]
        ]
    )

def get_back_keyboard(target: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_{target}")]
        ]
    )

def get_clear_edit_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Очистить", callback_data="clear_orders")],
            [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_orders")]
        ]
    )

def get_clear_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Очистить", callback_data="clear_orders")]
        ]
    )

def get_edit_select_keyboard(order_ids: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Подбор {oid}", callback_data=f"edit_{oid}")]
            for oid in order_ids
        ]
    )

def get_edit_fields_keyboard(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Изменить диаметр", callback_data=f"update_{order_id}_diameter")],
            [InlineKeyboardButton(text="Изменить глубину", callback_data=f"update_{order_id}_depth")],
            [InlineKeyboardButton(text="Изменить количество", callback_data=f"update_{order_id}_quantity")]
        ]
    )
