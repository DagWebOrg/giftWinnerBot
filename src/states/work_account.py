from aiogram.fsm.state import State, StatesGroup

class WorkAccountState(StatesGroup):
    create_alias_entry = State()
    create_access_token_entry = State()
    delete_alias_entry = State()

