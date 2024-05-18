from aiogram import Router, Bot, types, F
from aiogram.fsm.context import FSMContext

from states.keyboard import KeyboardState
from states.work_account import WorkAccountState

from utils.permissions import is_authenticated
from utils.keyboards import KeyboardStorage as kb
from utils.formatters import format_work_accounts_to_alias_list
from utils.exceptions import AccountAddingError

from services.utils import get_id_by_login_and_password

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
    await state.set_state(WorkAccountState.create_login_entry)
    await message.answer("Введите логин аккаунта: ", reply_markup=keyboard)


@router.message(WorkAccountState.create_login_entry)
async def work_account_login_entry(message: types.Message, state: FSMContext):
    is_authenticated(message)
    login = message.text.strip()
    await state.update_data({'login': login})
    keyboard = kb.kb_for_return()
    await state.set_state(WorkAccountState.create_password_entry)
    await message.answer("Введите пароль аккаунта: ", reply_markup=keyboard)


@router.message(WorkAccountState.create_password_entry)
async def work_account_password_entry(message: types.Message, state: FSMContext, bot: Bot):
    is_authenticated(message)

    # Удаляем пароль из чата после введения.
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    password = message.text.strip()
    await state.update_data({'password': password})

    data = await state.get_data()

    # логинимся и получаем id аккаунта
    data['account_id'] = get_id_by_login_and_password(data['login'], data['password'])

    # если id аккаунта не получен - вызываем исключение
    if not data['account_id']:
        raise AccountAddingError(message='Ошибка при добавлении аккаунта. Не удалось авторизоваться и получить id по введенным данным.')

    
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
