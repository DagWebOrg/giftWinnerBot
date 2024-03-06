import aiohttp
import asyncio



async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com/events') as resp:
            print(await resp.json())

asyncio.run(main())