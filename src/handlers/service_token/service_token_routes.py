from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext

from states.keyboard import KeyboardState
from states.service_token import ServiceTokenState

from utils.permissions import is_authenticated
from utils.keyboards import KeyboardStorage as kb
from utils.formatters import format_tracking_accounts_to_list

from database.crud import CRUD


router = Router(name=__name__)


@router.message(F.text == "Добавить/обновить токен 🎛")
async def service_token(message: types.Message, state: FSMContext):
    is_authenticated(message)

    keyboard = kb.kb_for_return()
    await state.set_state(ServiceTokenState.replace_token_entry)
    await message.answer('Введите новый токен:', reply_markup=keyboard)


@router.message(ServiceTokenState.replace_token_entry)
async def service_token_entry(message: types.Message, state: FSMContext, bot: Bot):
    is_authenticated(message)

    # Удаляем токен из чата после введения.
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    token = message.text.strip()

    CRUD.update_service_token(token = token)

    keyboard = kb.initial()
    await state.set_state(KeyboardState.initial)

    information = 'Токен был успешно обновлен!'

    await message.answer(information, reply_markup=keyboard)