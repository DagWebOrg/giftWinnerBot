from aiogram.fsm.state import State, StatesGroup

class KeyboardState(StatesGroup):
    initial = State()
    work_accounts_list = State()
    monitored_accounts_list = State()