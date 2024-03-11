from aiogram import Router, Bot, types, F
from aiogram.fsm.context import FSMContext

from states.keyboard import KeyboardState
from states.work_account import WorkAccountState

from utils.permissions import is_authenticated
from utils.keyboards import KeyboardStorage as kb
from utils.formatters import format_work_accounts_to_alias_list

from database.crud import CRUD


router = Router(name=__name__)


@router.message(F.text == "Список рабочих аккаунтов 📝")
async def work_account_list(message: types.Message, state: FSMContext):
    is_authenticated(message)

    information = f'Список рабочих аккаунтов:\n\n{format_work_accounts_to_alias_list(CRUD.get_work_accounts())}'

    keyboard = kb.work_accounts_list()
    await state.set_state(KeyboardState.work_accounts_list)
    await message.answer(information, reply_markup=keyboard)


@router.message(F.text == "Добавить новый аккаунт ✍🏻")
async def create_work_account(message: types.Message, state: FSMContext):
    is_authenticated(message)
    keyboard = kb.kb_for_return()
    await state.set_state(WorkAccountState.create_alias_entry)
    await message.answer("Введите alias аккаунта: ", reply_markup=keyboard)


@router.message(WorkAccountState.create_alias_entry)
async def work_account_create_alias_entry(message: types.Message, state: FSMContext):
    is_authenticated(message)
    alias = message.text.strip()
    await state.set_data({'alias': alias})
    keyboard = kb.kb_for_return()
    await state.set_state(WorkAccountState.create_access_token_entry)
    await message.answer("Введите токен доступа аккаунта: ", reply_markup=keyboard)


@router.message(WorkAccountState.create_access_token_entry)
async def work_account_token_entry(message: types.Message, state: FSMContext, bot: Bot):
    is_authenticated(message)

    # Удаляем токен из чата после введения.
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


    access_token = message.text.strip()
    await state.update_data({'access_token': access_token})

    data = await state.get_data()
    CRUD.create_work_account(**data)

    keyboard = kb.work_accounts_list()
    await state.set_state(KeyboardState.work_accounts_list)

    information = f'Список рабочих аккаунтов:\n\n{format_work_accounts_to_alias_list(CRUD.get_work_accounts())}'

    await message.answer(information, reply_markup=keyboard)


@router.message(F.text == 'Удалить аккаунт ❌')
async def delete_work_account(message: types.Message, state: FSMContext):
    is_authenticated(message)

    information = f'Введите alias аккаунта, который необходимо удалить.'

    keyboard = kb.kb_for_return()
    await state.set_state(WorkAccountState.delete_alias_entry)
    await message.answer(information, reply_markup=keyboard)


# Удаление аккаунта по alias
@router.message(WorkAccountState.delete_alias_entry)
async def work_account_delete_alias_entry(message: types.Message, state: FSMContext):
    is_authenticated(message)

    CRUD.delete_work_account(message.text)

    information = f'Аккаунт был успешно удален.\n\n{format_work_accounts_to_alias_list(CRUD.get_work_accounts())}'

    keyboard = kb.work_accounts_list()
    await state.set_state(KeyboardState.work_accounts_list)
    await message.answer(information, reply_markup=keyboard)
