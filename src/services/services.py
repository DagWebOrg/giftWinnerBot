import json
import asyncio

from vk_api import auth
from database.crud import CRUD
from .api.api import get_posts_from_tracking_account, repost_posts_to_work_account

async def add_all_new_posts_to_database(message):
    tracking_accounts = CRUD.get_tracking_accounts()
    validated_posts = []

    # переделать под GATHER асинхронно РАЗДЕЛИТЬ НА ФУНКЦИИ КОД МАКСИМУМ 10 строк
    for account in tracking_accounts:
        print(account['last_scan_data'].timestamp(), '<---')
        account_last_scan_data = account['last_scan_data'].timestamp()

        response_obj = await get_posts_from_tracking_account(account['account_id'], count=10)

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
            # if account_last_scan_data > post['date']:
            #     continue

            original_post = post['copy_history'][0]

            post_id = f"wall{str(original_post['owner_id'])}_{str(original_post['id'])}"
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
        print(account['login'], '---', account['password'])

        try:
            me = auth.auth(login=account['login'], password=account['password'])
        except Exception as e:
            await message.answer(f'Ошибка при входе в аккаунт {account["login"]} --- \n{e}')
            continue
        

        for post in posts:
            post_id = post['post_id']

            # post_response = me.method(method='wall.addLike', values={
            #     'post_id': post_id,
            # })
            try:
                resposne_obj = me.method(method='wall.repost', values={
                    'object': post_id,
                })
            except Exception as e:
                await message.answer(f'Ошибка при репосте поста {post["post_id"]}:\n{e}')
                continue

            # print(post_response)
            print(resposne_obj,'\n\n')



    CRUD.delete_all_posts()

