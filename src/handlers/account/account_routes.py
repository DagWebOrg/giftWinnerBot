from aiogram import Router, types
from aiogram.filters.command import Command


router = Router(name=__name__)

# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

