import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from dotenv import load_dotenv

from dispatcher import bot, dp


load_dotenv()
logging.basicConfig(level=logging.INFO)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())