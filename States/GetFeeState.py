from aiogram.fsm.state import StatesGroup, State


class GetFeeState(StatesGroup):
    get_kb = State()
    get_from_address = State()
    get_to_address = State()
    get_amount = State()
