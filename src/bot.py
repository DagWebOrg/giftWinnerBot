import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from dotenv import load_dotenv

from dispatcher import bot, dp
from database.crud import CRUD


load_dotenv()
logging.basicConfig(level=logging.INFO)

async def main():
    CRUD.loginfo()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())