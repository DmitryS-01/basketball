from aiogram.fsm.state import StatesGroup, State


class ProfileEditing(StatesGroup):
    name = State()


class IsShooting(StatesGroup):
    is_shooting = State()
