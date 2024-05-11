import time

from vk_api import auth
from vk_api.vk_api.exceptions import ApiError

from logger.config import LOGGER
from database.crud import CRUD
from .http_requests.api import get_posts_from_api




async def get_new_posts_from_tracked_accounts(posts_count):
    tracking_accounts = CRUD.get_tracking_accounts()
    posts = []

    for account in tracking_accounts:
        json_response = await get_posts_from_api(account['account_id'], count=posts_count)

        # Если вернулся ответ с ошибкой.
        if 'error' in json_response.keys():
            error_msg = json_response.get('error').get('error_msg')
            LOGGER.error(f'Ошибка при сканировании аккаунта {account["account_id"]}:\n{error_msg}')
            continue

        new_posts = filter_new_posts(json_response['response'].get('items', []), \
                                      account['last_scan_data'])
        posts += new_posts

        update_scan_date_on_the_tracking_account(account)
    return(posts)


def validate_posts(posts):
    validated_posts = []
    for post in posts:
        if post_is_validated(post):
            original_post = post['copy_history'][0]
            post_id = f"wall{str(original_post['owner_id'])}_{str(original_post['id'])}"
            # Не ограничивать количество текста, потому что при репосте будет нужен весь текст!!!!!!!!
            content = original_post['text'][:100]

            validated_posts.append({
            'post_id': post_id,
            'content': content,
            })

    return validated_posts


# Функция возвращает посты, с датой позднее последнего сканирования.
def filter_new_posts(posts, last_scan_data):
    new_posts = []
    for post in posts:
        if last_scan_data.timestamp() < post['date']:
            new_posts.append(post)

    return new_posts


def post_is_validated(post):
    from settings import GIFT_WORDS


    corresponds = True

    # Если пост не репостнут с другого аккаунта.
    if 'copy_history' not in post.keys():
        corresponds = False
        return corresponds

    original_post = post['copy_history'][0]
    
    # Если исходный пост не содержит ключевых слов.
    if not string_contain(original_post['text'], GIFT_WORDS):
        corresponds = False
        return corresponds

    return corresponds


def update_scan_date_on_the_tracking_account(account):
    CRUD.delete_tracking_account(account['alias'])
    CRUD.create_tracking_account(alias=account['alias'], account_id=account['account_id'])


def string_contain(string: str, substrings_list: list):
    result = False
    for sub_str in substrings_list:
        if (string.lower().find(sub_str.lower()) != -1):
            result = True
            break
    return result


def get_auth_session(account):
    vk_auth = auth.auth(login=account['login'], password=account['password'])
    return vk_auth

def take_part_in_the_draw(vk_auth, account, posts):
        for post in posts:
            full_post_id = post['post_id']
            group_id = full_post_id[4:].split("_")[0]
            group_post_id = full_post_id[4:].split("_")[1]

            try:
                # проверка на то, была ли репостнута запись ранее.
                if post_is_already_reposted(vk_auth, group_id, group_post_id):
                    LOGGER.info(f"Аккаунт {account['alias']} пропустил ранее обработанный пост с id {full_post_id}")
                    continue

                LOGGER.info(f"Аккаунт {account['alias']} комментирует пост с id {full_post_id}")
                write_a_comment_on_the_post(vk_auth, group_id, group_post_id)

                time.sleep(2)
                LOGGER.info(f"аккаунт {account['alias']} репостит запись {full_post_id}")
                repost_post(vk_auth, full_post_id)

                time.sleep(2)
                LOGGER.info(f"аккаунт {account['alias']} вступает в группу поста {full_post_id}")
                join_to_groups(vk_auth, [group_id])
                    
                time.sleep(2)
                groups_id_from_text = return_all_groups_id_from_text(post['content'])
                LOGGER.info(f"аккаунт {account['alias']} вступает в группы из текста поста {groups_id_from_text}")
                join_to_groups(vk_auth, groups_id_from_text)


                time.sleep(60)


            except Exception as e:
                LOGGER.error(f'Ошибка при работе с постом {full_post_id}:\n{e}')
                print(Exception)
                continue
            finally:
                LOGGER.info(f'----------КОНЕЦ-РАБОТЫ-С-ПОСТОМ-{full_post_id}----------')


def post_is_already_reposted(vk_auth, group_id, group_post_id):
    already_reposted = int(vk_auth.method(method='likes.isLiked', values={
        'owner_id': group_id,
        'item_id': group_post_id,
        'type': 'post'
    })['copied'])
    return already_reposted

def write_a_comment_on_the_post(vk_auth, group_id, group_post_id, message = 'Участвую'):
    vk_auth.method(method='wall.createComment', values={
    'owner_id': group_id,
    'post_id': group_post_id,
    'message': message
    })

def repost_post(vk_auth, full_post_id):
    vk_auth.method(method='wall.repost', values={
    'object': full_post_id,
    })

def join_to_groups(vk_auth, group_id_list: list):
    for group_id in group_id_list:
        try: 
            vk_auth.method(method='groups.join', values={
            'group_id': abs(int(group_id)),
            })
        # api_exception.code == 15 - значит, что мы уже вступили в это сообщество.
        # в таком случае выбрасывать исключение не нужно
        except ApiError as api_exception:
            if api_exception.code == 15:
                LOGGER.info(f'Группа с id {group_id} была пропущена. Аккаунт уже в числе ее участников.')
                continue
            raise ApiError


    
def return_all_groups_id_from_text(post_text):
    import re

    matches = re.findall(r'\[club(\d+)', post_text)
    matches += re.findall(r'vk.com/public(\d+)', post_text)
    communities_id = [match for match in matches]
    communities_id = list(set(communities_id))
    
    if matches:
        return communities_id
    else:
        return []

