import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import ErrorEvent, Message
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.context import FSMContext


from handlers.account import account_routes
from utils.exceptions import AuthError
from states.account import AccountState

token = os.getenv('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher()

dp.include_router(account_routes.router)


@dp.error(ExceptionTypeFilter(AuthError, ValueError), F.update.message.as_("message") )
async def error_handler(event: ErrorEvent, message: Message, state: FSMContext):
    if not isinstance(event, ValueError):
        await state.set_state(AccountState.password_entry)
    await message.answer(text=str(event.exception))

   
   
