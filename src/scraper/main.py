import asyncio

from core.config import settings
from scraper.services import get_latest_articles, refresh_db_articles
from bot.services import send_new_article, get_articles_from_db


async def check_for_updates():
    new_articles = await get_latest_articles()
    old_articles = await get_articles_from_db()
    for slug in new_articles:
        if slug not in old_articles:
            await refresh_db_articles(slug)
            await send_new_article(slug)
        continue


async def periodic_scraping(interval_sec=settings.scraping_interval_seconds):
    while True:
        await asyncio.sleep(interval_sec)
        await check_for_updates()
