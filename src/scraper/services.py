import aiohttp

from bs4 import BeautifulSoup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from scraper.models import Article
from core.database import get_session


URL = "https://www.the-race.com/formula-1/"


async def get_latest_articles():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=URL) as response:
            soup = BeautifulSoup(await response.text(), "lxml")
            articles = soup.find("div", class_="archive-width").find_all(
                class_="entry-title"
            )
            slugs = [
                article.find("a").get("href").split("/")[-2]
                for article in articles
            ][::-1]
            return slugs


async def save_article_to_db(slug):
    session: AsyncSession = get_session()
    new_article = Article(slug=slug)
    session.add(new_article)
    await session.commit()


async def refresh_db_articles(slug):
    session: AsyncSession = get_session()
    oldest_article = await session.execute(
        select(Article).order_by(Article.created_at).limit(1)
    )
    await session.delete(oldest_article)
    await save_article_to_db(slug=slug)


async def initial_scraping():
    slugs = await get_latest_articles()
    for slug in slugs:
        await save_article_to_db(slug=slug)
