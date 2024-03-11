from aiogram.fsm.state import StatesGroup, State


class GetBalanceState(StatesGroup):
    get_kb = State()
    get_address = State()
