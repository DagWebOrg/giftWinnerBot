import os
import logging

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from dotenv import load_dotenv

from dispatcher import bot, dp
from database.crud import CRUD
from database.models import apply_models
from utils.permissions import set_allowed_users_to_settings
import settings

# apply_models()

# logging.basicConfig(level=logging.INFO)

async def main():
    # apply_models()
    set_allowed_users_to_settings()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

