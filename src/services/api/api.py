import asyncio

from utils.api import make_api_request


async def get_posts_from_tracking_account(account_id, count = 2):
    data = {
    'access_token': '',
    'v': 5.199,
    'owner_id': account_id,
    'count': count,
    }

    return await make_api_request(method = 'wall.get', data = data)

    #response.items[0].date - дата


def repost_posts_to_work_account():
    ...
