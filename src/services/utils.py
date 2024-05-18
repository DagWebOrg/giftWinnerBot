import time
import random

from vk_api import auth
from vk_api.vk_api.exceptions import ApiError

from logger.config import LOGGER
from database.crud import CRUD
from .http_requests.api import get_posts_from_api

import settings




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
            content = original_post['text']

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
    if not string_contains_at_least_one_word(original_post['text'], GIFT_WORDS):
        corresponds = False
        return corresponds

    return corresponds


def update_scan_date_on_the_tracking_account(account):
    CRUD.delete_tracking_account(account['alias'])
    CRUD.create_tracking_account(alias=account['alias'], account_id=account['account_id'])


def string_contains_at_least_one_word(string: str, substrings_list: list):
    result = False
    for sub_str in substrings_list:
        if (string.lower().find(sub_str.lower()) != -1):
            result = True
            break
    return result

# На вход подаются несколько наборов слов, должно встретиться каждое слово хотя бы из одного набора.
#   [
#       ['первое слово', 'второе слово'], - первый набор
#        ['qwer', 'skldfngdlfgj', '1111'], - второй набор
#   ]
def string_contains_every_word(string: str, all_substrings_lists: list[list]):
    for substrings_list in all_substrings_lists:
        contain_a_set_of_words = True
        for sub_str in substrings_list:
            if (string.lower().find(sub_str.lower()) != -1):
                continue
            else:
                contain_a_set_of_words = False
        if contain_a_set_of_words:
            return True
    return False

        

def get_auth_session(login, password):
    vk_auth = auth.auth(login=login, password=password)
    return vk_auth

def take_part_in_the_draw(vk_auth, account, posts):
        for post in posts:
            full_post_id = post['post_id']
            group_id = full_post_id[4:].split("_")[0]
            group_post_id = full_post_id[4:].split("_")[1]

            try:
                # проверка на то, была ли репостнута запись ранее.
                if post_is_already_liked(vk_auth, group_id, group_post_id):
                    LOGGER.info(f"Аккаунт {account['alias']} пропустил ранее обработанный пост с id {full_post_id}")
                    continue

                # Если в посте сказано отметить друга
                if string_contains_every_word(post['content'], settings.WORDS_DEFINING_THAT_POST_WITH_A_FRIENDS_MARK):
                    LOGGER.info(f"Аккаунт {account['alias']} комментирует пост, в котором нужно отметить друзей с id {full_post_id}")
                    write_a_friends_mark_comment_on_the_post(vk_auth, group_id, group_post_id)
                else:
                    LOGGER.info(f"Аккаунт {account['alias']} комментирует пост с id {full_post_id}")
                    write_a_standart_comment_on_the_post(vk_auth, group_id, group_post_id)

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


def post_is_already_liked(vk_auth, group_id, group_post_id):
    already_liked = int(vk_auth.method(method='likes.isLiked', values={
        'owner_id': group_id,
        'item_id': group_post_id,
        'type': 'post'
    })['copied'])
    return already_liked

def write_a_standart_comment_on_the_post(vk_auth, group_id, group_post_id, message = 'Участвую'):
    for comment_list in settings.STANDART_COMMENTS:
        comment = random.choice(comment_list)

        vk_auth.method(method='wall.createComment', values={
        'owner_id': group_id,
        'post_id': group_post_id,
        'message': comment
        })

        time.sleep(3)

def write_a_friends_mark_comment_on_the_post(vk_auth, group_id, group_post_id, number_of_marks = 3):
    work_accounts = CRUD.get_work_accounts()

    my_identificator = vk_auth.__dict__['token']['user_id']

    all_work_accounts = []
    selected_work_accounts = []

    # Достаем все id из бд
    for account in work_accounts:
        if my_identificator != account['account_id']:
            all_work_accounts.append({
                'account_id': account['account_id'],
                'alias': account['alias']
                })
    
    # Выбираем id аккаунтов для репоста
    if len(all_work_accounts) < number_of_marks:
        selected_work_accounts = random.sample(all_work_accounts, len(all_work_accounts))
    else:
        selected_work_accounts = random.sample(all_work_accounts, number_of_marks)

    for account in selected_work_accounts:
        vk_auth.method(method='wall.createComment', values={
        'owner_id': group_id,
        'post_id': group_post_id,
        'message': f"@id{account['account_id']} ({account['alias']})"
        })

        time.sleep(3)




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
    
def get_id_by_login_and_password(login, password):
    try:
        vk_auth = get_auth_session(login, password)
        account_id = vk_auth.__dict__['token']['user_id']
        return account_id
    except Exception as e:
        LOGGER.error(f'Ошибка при записи рабочего аккаунта в бд. Не удалось залогиниться с помощью vk_api. {login} --- \n{e}')
        return False

