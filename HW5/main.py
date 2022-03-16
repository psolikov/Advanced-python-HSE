import aiofiles as aiofiles
import aiohttp
import asyncio

URL = "https://picsum.photos/512"


async def get_img(file):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            img = await response.read()
            f_img = await aiofiles.open(f"{file}.jpg", mode='wb')
            await f_img.write(img)
            await f_img.close()


async def get_n_img(n):
    tasks = []

    for i in range(n):
        tasks.append(get_img(i))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(get_n_img(3))
