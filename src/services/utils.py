from logger.config import LOGGER
from database.crud import CRUD
import datetime
from .http_requests.api import get_posts_from_api




async def get_posts_from_tracked_accounts():
    tracking_accounts = CRUD.get_tracking_accounts()
    posts = []

    for account in tracking_accounts:
        json_response = await get_posts_from_api(account['account_id'], count=20)
        # Если вернулся ответ с ошибкой.
        if 'error' in json_response.keys():
            error_msg = json_response.get('error').get('error_msg')
            LOGGER.error(f'Ошибка при сканировании аккаунта {account["account_id"]}:\n{error_msg}')
            continue

        new_posts = filter_new_posts(json_response['response'].get('items', []), \
                                      account['last_scan_data'])
        posts += new_posts

    update_scan_date_on_the_tracking_account(account)

    # Удаление дублирующихся постов.
    return(posts)


def get_validated_posts(posts):
    validated_posts = []
    for post in posts:
        if post_is_validated(post):
            original_post = post['copy_history'][0]

            post_id = f"wall{str(original_post['owner_id'])}_{str(original_post['id'])}"


            content = original_post['text'][:100]

            validated_posts.append({
            'post_id': post_id,
            'content': content,
            })

    return validated_posts


def filter_new_posts(posts, last_scan_data):
    new_posts = []
    for post in posts:
        if last_scan_data.timestamp() < post['date']:
            new_posts.append(post)

    # print(new_posts)
    return new_posts

GIFT_WORDS = ['конкурс', 'розыгрыш', "итоги", "дар", "репост", "побед", "билет", "абонемент", 'разыгр']


def post_is_validated(post):
    # print(post, '\n\n\n\n\n\n\n\!\n\n!\n\n')
    corresponds = True
    # Если пост не репостнут с другого аккаунта.
    if 'copy_history' not in post.keys():
        corresponds = False
        return corresponds
    # print(datetime.fromtimestamp(account_last_scan_data),'--', datetime.fromtimestamp(post['date']))

    original_post = post['copy_history'][0]
    
    # print(original_post)
    if not string_contain(original_post['text'], GIFT_WORDS):
        corresponds = False
        return corresponds
    
    

    return corresponds
    


def update_scan_date_on_the_tracking_account(account):
    CRUD.delete_tracking_account(account['alias'])
    CRUD.create_tracking_account(alias=account['alias'], account_id=account['account_id'])




def string_contain(string: str, sub_str_list: list):
    result = False
    for sub_str in sub_str_list:
        if (string.lower().find(sub_str.lower()) != -1):
            result = True
            break
    return result
    
