import json
import asyncio
from datetime import datetime

from vk_api import auth
from database.crud import CRUD
from logger.config import LOGGER

from .utils import get_new_posts_from_tracked_accounts, validate_posts, get_auth_session, take_part_in_the_draw


async def add_posts_from_tracking_accounts_to_db():
    from settings import NUMBER_OF_SCANNED_POST_FROM_ACCOUNT as posts_count

    posts = await get_new_posts_from_tracked_accounts(posts_count)
    validated_posts = validate_posts(posts)

    CRUD.create_posts(validated_posts)
    print(validated_posts)



async def process_posts_with_prize_draws_from_database():
    posts = CRUD.get_posts()
    work_accounts = CRUD.get_work_accounts()
    for account in work_accounts:
        try:
            vk_auth = get_auth_session(account['login'], account['password'])
        except Exception as e:
            LOGGER.error(f'Ошибка при входе в аккаунт {account["login"]} --- \n{e}')
            continue
        
        take_part_in_the_draw(vk_auth, account, posts)

    CRUD.delete_all_posts()
