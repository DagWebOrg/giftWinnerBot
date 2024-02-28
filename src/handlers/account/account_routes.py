from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from states.account import AccountState
from utils.permissions import is_authenticated
from utils.exceptions import AuthError

import settings
from database.crud import CRUD



router = Router(name=__name__)

# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    if not is_authenticated(message):
        await state.set_state(AccountState.password_entry)
        await message.answer("Введи код!")
     

@router.message(AccountState.password_entry)
async def authenticate_user(message: types.Message, state: FSMContext):
   
    text = "Неправильный код подтверждения"
    if message.text == settings.BOT_PASSWORD:
        user_id = int(message.from_user.id)
        CRUD.create_user(user_id)
        settings.ALLOWED_USERS.append(int(user_id))
        text = 'Вы успешно авторизовались!'
        await state.clear()

    await message.answer(text=text)


@router.message()
async def message_handler(message: types.Message):
    is_authenticated(message)
   

        