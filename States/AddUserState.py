from aiogram.fsm.state import StatesGroup, State


class AddUserState(StatesGroup):
    get_address = State()
