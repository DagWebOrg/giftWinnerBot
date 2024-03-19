from aiogram import Router, Bot, types, F
from aiogram.fsm.context import FSMContext

from states.keyboard import KeyboardState
from states.post import PostState

from utils.permissions import is_authenticated
from utils.keyboards import KeyboardStorage as kb
from services.services import add_all_new_posts_to_database, repost_all_new_posts_from_database


from database.crud import CRUD


router = Router(name=__name__)


@router.message(F.text == "Информация о розыгрышах 🛍")
async def post_list(message: types.Message, state: FSMContext):
    is_authenticated(message)

    information = f'Список постов:\n\n{CRUD.get_posts()}'

    keyboard = kb.post_list()
    await state.set_state(KeyboardState.post_list)
    await message.answer(information, reply_markup=keyboard)


@router.message(F.text == "Искать новые посты 🔍")
async def post_find(message: types.Message, state: FSMContext):
    is_authenticated(message)
    keyboard = types.ReplyKeyboardRemove()
    await message.answer('🔎 Идет поиск...', reply_markup=keyboard)

    await add_all_new_posts_to_database(message)

    keyboard = kb.post_list()
    await state.set_state(KeyboardState.post_list)

    information = f'Список постов:\n\n{CRUD.get_posts()}'
    await message.answer(information, reply_markup=keyboard)


@router.message(F.text == "Репост постов на рабочие аккаунты 📋")
async def repost_posts(message: types.Message, state: FSMContext):
    is_authenticated(message)
    keyboard = types.ReplyKeyboardRemove()
    await message.answer('🔎 Идет репост...', reply_markup=keyboard)

    await repost_all_new_posts_from_database(message)

    keyboard = kb.post_list()
    await state.set_state(KeyboardState.post_list)

    information = f'Операция прошла успешно!\n\nСписок постов:\n\n{CRUD.get_posts()}'
    await message.answer(information, reply_markup=keyboard)


@router.message(F.text == "Удалить пост 🚫")
async def post_delete(message: types.Message, state: FSMContext):
    is_authenticated(message)

    information = f'Введите id поста, который необходимо удалить.'

    keyboard = kb.kb_for_return()
    await state.set_state(PostState.delete_post_id_entry)
    await message.answer(information, reply_markup=keyboard)


@router.message(PostState.delete_post_id_entry)
async def post_delete_id_entry(message: types.Message, state: FSMContext):
    is_authenticated(message)

    CRUD.delete_post(message.text)

    information = f'Пост был успешно удален.\n\n{CRUD.get_posts()}'

    keyboard = kb.post_list()
    await state.set_state(KeyboardState.post_list)
    await message.answer(information, reply_markup=keyboard) 





