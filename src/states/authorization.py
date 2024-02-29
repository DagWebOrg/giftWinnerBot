from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class AuthorizationState(StatesGroup):
    password_entry = State()
