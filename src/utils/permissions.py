from aiogram import types
from aiogram.fsm.context import FSMContext

from logger.config import LOGGER
import settings
from utils.exceptions import AuthError
from database.crud import CRUD

from states.authorization import AuthorizationState


def is_authenticated(message: types.Message):
    if int(message.from_user.id) not in settings.ALLOWED_USERS:
        LOGGER.error(f'Пользователь с id {message.from_user.id} не авторизован!')
        raise AuthError()
    return True


def set_allowed_users_to_settings():
    settings.ALLOWED_USERS = CRUD.get_users()
        
    
    
