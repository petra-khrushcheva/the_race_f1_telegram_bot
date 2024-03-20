import requests

from bs4 import BeautifulSoup
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from scraper.models import Article
from core.database import get_session


URL = "https://www.the-race.com/formula-1/"


async def get_latest_articles():
    response = requests.get(url=URL)
    soup = BeautifulSoup(response.text, "lxml")
    slugs = soup.find_all("a", class_="archive_width")
    print(slugs)

get_latest_articles()

# вытаскивает из супа список слагов и разворачивает его, возвращает список


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
    pass
