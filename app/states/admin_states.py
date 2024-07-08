from aiogram.fsm.state import StatesGroup, State


class MessageToAnotherUser(StatesGroup):
    msg = State()
