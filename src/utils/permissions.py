from aiogram import types
from aiogram.fsm.context import FSMContext

import settings
from utils.exceptions import AuthError

from database.crud import CRUD
from states.account import AccountState


def is_authenticated(message: types.Message):
    if int(message.from_user.id) not in settings.ALLOWED_USERS:
        raise AuthError()
    return True

def set_allowed_users_to_settings():
    users = CRUD.get_users()
    settings.ALLOWED_USERS = users    
    
    
