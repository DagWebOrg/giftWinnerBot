import logging

import asyncio

from aiogram.methods import DeleteWebhook

from dispatcher import bot, dp
from database.models import apply_models
from utils.permissions import set_allowed_users_to_settings
from tasks.tasks import search_and_repost_posts


async def main():
    apply_models()
    set_allowed_users_to_settings()
    search_and_repost_posts()

    # пропуск обновлений в момент неактивности бота
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

