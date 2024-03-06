from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from states.keyboard import KeyboardState
from states.tracking_account import TrackingAccountState

from utils.permissions import is_authenticated
from utils.keyboards import KeyboardStorage as kb
from utils.formatters import format_tracking_accounts_to_list

from database.crud import CRUD


router = Router(name=__name__)


@router.message(F.text == "Список отслеживаемых аккаунтов 👁")
async def tracking_account_list(message: types.Message, state: FSMContext):
    is_authenticated(message)

    information = f'Список отслеживаемых аккаунтов:\n\n{format_tracking_accounts_to_list(CRUD.get_tracking_accounts())}'

    keyboard = kb.tracking_accounts_list()
    await state.set_state(KeyboardState.tracking_accounts_list)
    await message.answer(information, reply_markup=keyboard)


@router.message(F.text == "Добавить новый аккаунт 🖌")
async def create_tracking_account(message: types.Message, state: FSMContext):
    is_authenticated(message)
    keyboard = kb.kb_for_return()
    await state.set_state(TrackingAccountState.create_alias_entry)
    await message.answer("Введите alias аккаунта: ", reply_markup=keyboard)


@router.message(TrackingAccountState.create_alias_entry)
async def tracking_account_create_alias_entry(message: types.Message, state: FSMContext):
    is_authenticated(message)
    alias = message.text.strip()
    await state.set_data({'alias': alias})
    keyboard = kb.kb_for_return()
    await state.set_state(TrackingAccountState.create_id_entry)
    await message.answer("Введите id аккаунта: ", reply_markup=keyboard)


@router.message(TrackingAccountState.create_id_entry)
async def tracking_account_token_entry(message: types.Message, state: FSMContext):
    is_authenticated(message)
    account_id = message.text.strip()
    await state.update_data({'account_id': account_id})

    data = await state.get_data()
    CRUD.create_tracking_account(**data)

    keyboard = kb.tracking_accounts_list()
    await state.set_state(KeyboardState.tracking_accounts_list)

    information = f'Список отслеживаемых аккаунтов:\n\n{format_tracking_accounts_to_list(CRUD.get_tracking_accounts())}'

    await message.answer(information, reply_markup=keyboard)


@router.message(F.text == 'Удалить аккаунт 🚫')
async def delete_tracking_account(message: types.Message, state: FSMContext):
    is_authenticated(message)

    information = f'Введите alias аккаунта, который необходимо удалить.'

    keyboard = kb.kb_for_return()
    await state.set_state(TrackingAccountState.delete_alias_entry)
    await message.answer(information, reply_markup=keyboard)


@router.message(TrackingAccountState.delete_alias_entry)
async def tracking_account_delete_alias_entry(message: types.Message, state: FSMContext):
    is_authenticated(message)

    CRUD.delete_tracking_account(message.text)

    information = f'Аккаунт был успешно удален.\n\n{format_tracking_accounts_to_list(CRUD.get_tracking_accounts())}'

    keyboard = kb.tracking_accounts_list()
    await state.set_state(KeyboardState.tracking_accounts_list)
    await message.answer(information, reply_markup=keyboard)