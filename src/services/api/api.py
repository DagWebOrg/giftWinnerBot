import asyncio

from database.crud import CRUD
from utils.api import make_api_request


async def get_posts_from_tracking_account(account_id, count = 1):
    service_token = CRUD.get_service_token()

    data = {
    'access_token': service_token,
    'v': 5.199,
    'owner_id': account_id,
    'count': count,
    }

    return await make_api_request(method = 'wall.get', data = data)

    #response.items[0].date - дата


async def repost_posts_to_work_account(access_token, post_id):
    
    data = {
        'access_token': access_token,
        'v': 5.199,
        'object': post_id,
    }

    return await make_api_request(method = 'wall.repost', data = data)

