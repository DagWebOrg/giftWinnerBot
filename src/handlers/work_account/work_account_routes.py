from aiogram import Router, Bot, types, F
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


@router.message(F.text == "Список рабочих аккаунтов 📝")
async def work_account_list(message: types.Message, state: FSMContext):
    is_authenticated(message)
    keyboard = kb.work_accounts_list()
    await state.set_state(KeyboardState.work_accounts_list)
    await message.answer("Cписок рабочих аккаунтов: ", reply_markup=keyboard)