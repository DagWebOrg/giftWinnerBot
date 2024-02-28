import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from dotenv import load_dotenv

from dispatcher import bot, dp
from database.crud import CRUD
from database.models import apply_models
from utils.permissions import set_allowed_users_to_settings
import settings

# apply_models()

load_dotenv()
# logging.basicConfig(level=logging.INFO)

async def main():
    # apply_models()
    set_allowed_users_to_settings()
    # print(settings.ALLOWED_USERS)

    set_allowed_users_to_settings()
    print(settings.ALLOWED_USERS)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())