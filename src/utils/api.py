import aiohttp


async def make_api_request(method: str, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://api.vk.com/method/{method}', data=data) as resp:
            return await resp.json()