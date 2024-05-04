import json
import asyncio
from datetime import datetime
import time

from vk_api import auth
from database.crud import CRUD
from logger.config import LOGGER

from .utils import get_posts_from_tracked_accounts, get_validated_posts


async def add_all_new_posts_to_database():
    posts = await get_posts_from_tracked_accounts()
    validated_posts = get_validated_posts(posts)

    CRUD.create_posts(validated_posts)
    print(validated_posts)



async def repost_all_new_posts_from_database():
    posts = CRUD.get_posts()
    work_accounts = CRUD.get_work_accounts()
    for account in work_accounts:
        try:
            me = auth.auth(login=account['login'], password=account['password'])
        except Exception as e:
            LOGGER.error(f'Ошибка при входе в аккаунт {account["login"]} --- \n{e}')
            continue
        

        for post in posts:
            full_post_id = post['post_id']
            group_id = full_post_id[4:].split("_")[0]
            group_post_id = full_post_id[4:].split("_")[1]

            try:
                # проверка на то, была ли репостнута запись ранее.
                already_reposted = int(me.method(method='likes.isLiked', values={
                    'owner_id': group_id,
                    'item_id': group_post_id,
                    'type': 'post'
                })['copied'])

                if already_reposted:
                    LOGGER.info(f"аккаунт {account['alias']} пропустил повторяющийся пост {full_post_id}")
                    continue

                LOGGER.info(f"аккаунт {account['alias']} комментирует запись {full_post_id}")
                print(me.method(method='wall.createComment', values={
                    'owner_id': group_id,
                    'post_id': group_post_id,
                    'message': 'участвую'
                }))

                time.sleep(2)
                LOGGER.info(f"аккаунт {account['alias']} репостит запись {full_post_id}")
                resposne_obj = me.method(method='wall.repost', values={
                    'object': full_post_id,
                })

                time.sleep(2)
                LOGGER.info(f"аккаунт {account['alias']} вступает в группу поста {full_post_id}")
                print(me.method(method='groups.join', values={
                    'group_id': abs(int(group_id)),
                }))
                time.sleep(60)


                



            except Exception as e:
                LOGGER.error(f'Ошибка при работе с постом {full_post_id}:\n{e}')
                continue
            finally:
                LOGGER.info(f'----------КОНЕЦ-РЕПОСТА----------')

    CRUD.delete_all_posts()




GIFT_WORDS = ['конкурс', 'розыгрыш', "итоги", "дар", "репост", "побед", "билет", "абонемент", 'разыгр']

def string_contain(string: str, sub_str_list: list):
    result = False
    for sub_str in sub_str_list:
        if (string.lower().find(sub_str.lower()) != -1):
            result = True
            break
    return result

def post_validate(account, post):
    account_last_scan_data = account['last_scan_data'].timestamp()
    corresponds = True

    # Если пост не репостнут с другого аккаунта.
    if 'copy_history' not in post.keys():
        corresponds = False
        return corresponds
    # Если публикация старая.
    # print(datetime.fromtimestamp(account_last_scan_data),'--', datetime.fromtimestamp(post['date']))
    if account_last_scan_data > post['date']:
        corresponds = False
        return corresponds

    original_post = post['copy_history'][0]
    
    if not string_contain(original_post['text'], GIFT_WORDS):
        corresponds = False
        return corresponds
    
    return corresponds

