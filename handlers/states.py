from aiogram.fsm.state import StatesGroup, State

class OrderFSM(StatesGroup):
    material = State()
    diameter = State()
    depth = State()
    quantity = State()

class EditFSM(StatesGroup):
    waiting_for_new_value = State()
