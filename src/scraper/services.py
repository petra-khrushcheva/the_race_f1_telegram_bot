import aiohttp

from bs4 import BeautifulSoup
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from scraper.models import Article
from core.database import get_session


URL = "https://www.the-race.com/formula-1/"


async def get_latest_articles():
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=URL)
    soup = BeautifulSoup(response.text, "lxml")
    articles = soup.find("div", class_="archive-width").find_all(
        class_="entry-title"
    )
    slugs = [
        article.find("a").get("href").split("/")[-2] for article in articles
    ][::-1]
    return slugs


async def get_articles_from_db():
    session: AsyncSession = get_session()
    result: Result = await session.execute(
        select(Article.slug).order_by(Article.created_at)
    )
    return result.scalars().all()


async def save_article_to_db(slug):
    session: AsyncSession = get_session()
    new_article = Article(slug=slug)
    session.add(new_article)
    await session.commit()


async def refresh_db_articles(slug):
    session: AsyncSession = get_session()
    oldest_article = session.execute(
        select(Article).order_by(Article.created_at).limit(1)
    )
    await session.delete(oldest_article)
    await save_article_to_db(slug=slug)


async def initial_scraping():
    slugs = await get_articles_from_db()
    for slug in slugs:
        await save_article_to_db(slug=slug)
