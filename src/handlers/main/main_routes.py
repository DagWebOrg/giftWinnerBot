from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from states.keyboard import KeyboardState
from utils.permissions import is_authenticated
from utils.keyboards import KeyboardStorage as kb


router = Router(name=__name__)


@router.message()
async def message_handler(message: types.Message, state: FSMContext):
    is_authenticated(message)
    if await state.get_state() is None:
        keyboard = kb.initial()
        await state.set_state(KeyboardState.initial)
        await message.answer(text='Синхронизировал клавиатуру для тебя.', reply_markup=keyboard)
