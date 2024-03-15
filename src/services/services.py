import json

from database.crud import CRUD
from .api.api import get_posts_from_tracking_account, repost_posts_to_work_account

async def add_all_new_posts_to_database(message):
    tracking_accounts = CRUD.get_tracking_accounts()
    validated_posts = []

    # переделать под GATHER асинхронно РАЗДЕЛИТЬ НА ФУНКЦИИ КОД МАКСИМУМ 10 строк
    for account in tracking_accounts:
        print(account['last_scan_data'].timestamp(), '<---')
        account_last_scan_data = account['last_scan_data'].timestamp()

        response_obj = await get_posts_from_tracking_account(account['account_id'], count=1)

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


async def repost_all_new_posts_from_database():
    posts = CRUD.get_posts()
    work_accounts = CRUD.get_work_accounts()

    for account in work_accounts:
        access_token = account['access_token']

        

        for post in posts:
            post_id = post['post_id']

            print(post_id)

            response_obj = await repost_posts_to_work_account(
                access_token=access_token,
                post_id=post_id,
            )

            print(response_obj)

    CRUD.delete_all_posts()
