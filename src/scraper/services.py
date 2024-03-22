import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy import delete, select

from core.database import async_session
from scraper.models import Article

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
    async with async_session() as session:
        new_article = Article(slug=slug)
        session.add(new_article)
        await session.commit()


async def refresh_db_articles(slug):
    async with async_session() as session:
        oldest_article = (
            await session.execute(
                select(Article).order_by(Article.created_at).limit(1)
            )
        ).scalar_one()
        await session.delete(oldest_article)
        await session.commit()
        await save_article_to_db(slug=slug)


async def initial_scraping():
    slugs = await get_latest_articles()
    for slug in slugs:
        await save_article_to_db(slug=slug)


async def delete_all_articles():
    async with async_session() as session:
        await session.execute(delete(Article))
        await session.commit()
