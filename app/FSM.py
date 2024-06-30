from aiogram.fsm.state import StatesGroup, State


class ProfileEditing(StatesGroup):
    name = State()
