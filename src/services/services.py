import json
import asyncio
from datetime import datetime

from vk_api import auth
from database.crud import CRUD
from .api.api import get_posts_from_tracking_account, repost_posts_to_work_account

GIFT_WORDS = ['конкурс', 'розыгрыш', "итоги", "дар", "репост", "побед", "билет", "абонемент"]

def string_contain(string: str, sub_str_list: list):
    result = False
    for sub_str in sub_str_list:
        if (string.lower().find(sub_str.lower()) != -1):
            result = True
            break
    return result


async def add_all_new_posts_to_database(message):
    tracking_accounts = CRUD.get_tracking_accounts()
    validated_posts = []

    # переделать под GATHER асинхронно РАЗДЕЛИТЬ НА ФУНКЦИИ КОД МАКСИМУМ 10 строк
    for account in tracking_accounts:
        print(account['last_scan_data'].timestamp(), '<---')
        account_last_scan_data = account['last_scan_data'].timestamp()

        response_obj = await get_posts_from_tracking_account(account['account_id'], count=15)

        # Если вернулся ответ с ошибкой.
        if 'error' in response_obj.keys():
            error_msg = response_obj.get('error').get('error_msg')
            await message.answer(f'Ошибка при сканировании аккаунта {account["account_id"]}:\n{error_msg}')
            continue

        posts = response_obj['response'].get('items', [])

        for post in posts:
            # Если пост не репостнут с другого аккаунта.
            if 'copy_history' not in post.keys():
                continue
            # Если публикация старая.
            print(datetime.fromtimestamp(account_last_scan_data),'--', datetime.fromtimestamp(post['date']))
            if account_last_scan_data > post['date']:
                continue

            original_post = post['copy_history'][0]

            post_id = f"wall{str(original_post['owner_id'])}_{str(original_post['id'])}"
            
            if string_contain(original_post['text'], []):
                content = original_post['text'][:100]
                validated_posts.append({
                'post_id': post_id,
                'content': content,
                })

        # print(posts)
        
        # Если постов > 0.
        if posts:
            CRUD.delete_tracking_account(account['alias'])
            CRUD.create_tracking_account(alias=account['alias'], account_id=account['account_id'])

        
    CRUD.create_posts(posts=validated_posts)
    print(validated_posts)


async def repost_all_new_posts_from_database(message):
    posts = CRUD.get_posts()
    work_accounts = CRUD.get_work_accounts()


    for account in work_accounts:
        try:
            me = auth.auth(login=account['login'], password=account['password'])
        except Exception as e:
            await message.answer(f'Ошибка при входе в аккаунт {account["login"]} --- \n{e}')
            continue
        

        for post in posts:
            post_id = post['post_id']
            group_id = post_id.split("-")[1].split("_")[0]
            group_post_id = post_id.split("-")[1].split("_")[1]


            print(me.method(method='wall.createComment', values={
                    'owner_id': f'-{group_id}',
                    'post_id': group_post_id,
                    'message': 'участвую'
                }))

            try:
                resposne_obj = me.method(method='wall.repost', values={
                    'object': post_id,
                })


                print(me.method(method='groups.join', values={
                    'group_id': group_id,
                }))

                



            except Exception as e:
                await message.answer(f'Ошибка при репосте поста {post["post_id"]}:\n{e}')
                continue

            # print(post_response)
            print(resposne_obj,'\n\n')



    CRUD.delete_all_posts()

