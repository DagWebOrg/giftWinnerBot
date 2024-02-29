from aiogram.fsm.state import State, StatesGroup

class KeyboardState(StatesGroup):
    initial = State()
    work_authorization_list = State()
    monitored_authorization_list = State()