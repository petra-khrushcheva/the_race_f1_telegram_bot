from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from scraper.models import Article
from core.database import get_session


async def get_latest_articles(soup):
    pass


# вытаскивает из супа список слагов и разворачивает его, возвращает список


async def get_articles_from_db():
    session: AsyncSession = get_session()
    result: Result = await session.execute(
        select(Article.slug).order_by(Article.created_at) #блин, здесь desc or asc???
    )
    return result.scalars().all()


async def save_article_to_db(slug):
    pass


# создает строку в бд


async def refresh_db_articles(new_slug):
    pass
#  удалить старейшую строку из бд и сохранить новую


async def initial_scraping():
    pass
