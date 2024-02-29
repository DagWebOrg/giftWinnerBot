from aiogram import Router, Bot, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from states.authorization import AuthorizationState
from states.keyboard import KeyboardState
from utils.permissions import is_authenticated
from utils.exceptions import AuthError
from utils.keyboards import KeyboardStorage as kb

import settings
from database.crud import CRUD


router = Router(name=__name__)


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет, кот!")
    is_authenticated(message)
    keyboard = kb.initial()
    await state.set_state(KeyboardState.initial)
    await message.answer("Ты уже авторизован.", reply_markup=keyboard)

    
    
     

@router.message(AuthorizationState.password_entry)
async def authenticate_user(message: types.Message, state: FSMContext, bot: Bot):

    text = "Неправильный код подтверждения."
    keyboard = types.ReplyKeyboardRemove()
    if message.text == settings.BOT_PASSWORD:
        # добавление нового id в список разрешенных.
        user_id = int(message.from_user.id)
        CRUD.create_user(user_id)
        settings.ALLOWED_USERS.append(int(user_id))
        # удаление введенного кода подтверждения из чата.
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        
        text = 'Ты успешно авторизовался!'
        keyboard = kb.initial()
        await state.set_state(KeyboardState.initial)

    await message.answer(text=text, reply_markup=keyboard)
