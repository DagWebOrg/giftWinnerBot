from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from states.keyboard import KeyboardState
from utils.permissions import is_authenticated
from utils.keyboards import KeyboardStorage as kb


router = Router(name=__name__)

@router.message(F.text.lower() == "вернуться на главную 🏚")
async def back_to_home(message: types.Message, state: FSMContext):
    keyboard = kb.initial()
    await state.set_state(KeyboardState.initial)
    await message.answer("Главная страница: ", reply_markup=keyboard)


@router.message()
async def message_handler(message: types.Message, state: FSMContext):
    is_authenticated(message)
    if await state.get_state() is None:
        keyboard = kb.initial()
        await state.set_state(KeyboardState.initial)
        await message.answer(text='Бот был перезапущен. Вы очутились на главной странице...', reply_markup=keyboard)
