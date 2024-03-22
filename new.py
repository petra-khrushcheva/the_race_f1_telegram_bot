import asyncio
import aiohttp

from bs4 import BeautifulSoup


URL = "https://www.the-race.com/formula-1/"


async def get_latest_articles():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=URL) as response:
            soup = BeautifulSoup(await response.text(), "lxml")
            articles = soup.find("div", class_="archive-width").find_all(
                class_="entry-title"
            )
            slugs = [
                article.find("a").get("href").split("/")[-2] for article in articles
            ][::-1]
            print(slugs)


asyncio.run(get_latest_articles())
