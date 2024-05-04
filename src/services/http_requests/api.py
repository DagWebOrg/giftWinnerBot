import asyncio
import aiohttp

from database.crud import CRUD

# Функция, выполняющая сканирование новых постов с отслеживаемых аккаунтов.
async def get_posts_from_api(account_id, count = 1):
    service_token = CRUD.get_service_token()

    data = {
    'access_token': service_token,
    'v': 5.199,
    'owner_id': account_id,
    'count': count,
    }

    return await make_api_request(method = 'wall.get', data = data)


async def make_api_request(method: str, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://api.vk.com/method/{method}', data=data) as resp:
            return await resp.json()

