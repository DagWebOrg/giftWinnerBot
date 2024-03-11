import aiohttp
import asyncio

data={
    'access_token': '',
    'owner_id':'mikhalchuk.vanya',
    'v': 5.199,
}

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.vk.com/method/wall.get', data=data) as resp:
            print(await resp.json())

asyncio.run(main())