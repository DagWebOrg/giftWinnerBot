from database.crud import CRUD
from .api.api import get_posts_from_tracking_account


async def add_all_new_posts_to_database():
    tracking_accounts = CRUD.get_tracking_accounts()
    validated_posts = []

    for account in tracking_accounts:
        print(account['last_scan_data'].timestamp(), '<---')
        account_last_scan_data = account['last_scan_data'].timestamp()

        response_obj = await get_posts_from_tracking_account(account['account_id'], 1)
        posts = response_obj['response']['items']

        for post in posts:
            if account_last_scan_data < post['date']:
                validated_posts.append({
                    'post_id': f"wall{post['owner_id']}_{post['id']}",
                    'content': post['text'][:100],
                })

        print(posts)
        
        # Если постов > 0.
        if posts:
            CRUD.delete_tracking_account(account['alias'])
            CRUD.create_tracking_account(alias=account['alias'], account_id=account['account_id'])

        
    CRUD.create_posts(posts=validated_posts)
    print(validated_posts)


def repost_all_new_posts_from_database():
    ...