from aiogram.fsm.state import State, StatesGroup

class ServiceTokenState(StatesGroup):
    replace_token_entry = State()