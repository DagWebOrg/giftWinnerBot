import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import ErrorEvent, Message, ReplyKeyboardRemove
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.context import FSMContext

from utils.exceptions import AuthError, AccountAddingError
from states.authorization import AuthorizationState
from states.keyboard import KeyboardState

from utils.keyboards import KeyboardStorage

from handlers.main import main_routes
from handlers.authorization import authorization_routes
from handlers.work_account import work_account_routes
from handlers.tracking_account import tracking_account_routes
from handlers.post import post_routes
from handlers.other import other_routes


token = os.getenv('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher()

dp.include_router(main_routes.router)
dp.include_router(authorization_routes.router)
dp.include_router(work_account_routes.router)
dp.include_router(tracking_account_routes.router)
dp.include_router(post_routes.router)
dp.include_router(other_routes.router)


@dp.error(ExceptionTypeFilter(AuthError, AccountAddingError, ValueError),
          F.update.message.as_("message"))
async def error_handler(event: ErrorEvent, message: Message, state: FSMContext):
    keyboard = ReplyKeyboardRemove()

    if isinstance(event.exception, AuthError):
        await state.set_state(AuthorizationState.password_entry)
    
    if isinstance(event.exception, AccountAddingError):
        await state.set_state(KeyboardState.initial)
        keyboard = KeyboardStorage.initial()

    await message.answer(text=str(event.exception), reply_markup=keyboard)

   
   
