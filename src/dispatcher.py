import os

from aiogram import Bot, Dispatcher
from aiogram.types import ErrorEvent

from handlers.account import account_routes

token = os.getenv('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher()

dp.include_router(account_routes.router)

# @dp.error()
# async def error_handler(event: ErrorEvent):
#     LOGGER.critical(event.exception)
