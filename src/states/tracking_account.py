from aiogram.fsm.state import State, StatesGroup

class TrackingAccountState(StatesGroup):
    create_alias_entry = State()
    create_id_entry = State()
    delete_alias_entry = State()

