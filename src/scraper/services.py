import asyncio
import logging

import aiohttp
from aiogram import Bot
from bs4 import BeautifulSoup
from sqlalchemy import delete, select

from bot.services import get_articles_from_db, send_new_article
from core import async_session, settings
from scraper.models import Article

URL = "https://www.the-race.com/formula-1/"


async def get_page_data(url):
    """Получение html кода заданной страницы."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                return await response.text()
        except aiohttp.ClientError as exception:
            logging.exception(exception)


def parse_page_data(html):
    """
    Получение слагов всех (трех) самых новых статей с сайта.
    """
    soup = BeautifulSoup(html, "lxml")
    articles = soup.find("div", class_="archive-width").find_all(
        class_="entry-title"
    )
    slugs = [
        article.find("a").get("href").split("/")[-2]
        for article in articles
    ][::-1]
    return slugs


async def get_latest_articles(url=URL):
    """
    Получение слагов всех (трех) самых новых статей с сайта.
    """
    html = await get_page_data(url)
    return parse_page_data(html=html)


async def save_article_to_db(slug):
    """Сохранение слага одной статьи в базу данных."""
    async with async_session() as session:
        new_article = Article(slug=slug)
        session.add(new_article)
        await session.commit()


async def refresh_db_articles(slug):
    """
    Обновление статей, хранящихся в базе данных. Удаляется самая старая статья
    и сохраняется новая, полученная при парсинге.
    """
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
    """
    Первоначальный парсинг. Выполняется при запуске бота.
    """
    slugs = await get_latest_articles()
    for slug in slugs:
        await save_article_to_db(slug=slug)


async def delete_all_articles():
    """
    Удаление слагов всех статей из базы данных. Выполняется при остановке бота.
    """
    async with async_session() as session:
        await session.execute(delete(Article))
        await session.commit()


async def check_for_updates(bot: Bot):
    """
    Общая функция проверки обновлений. Парсит статьи с сайта, сравнивает их
    с хранящимися в базе данных, при получении новой статьи обновляет бд
    и рассылает статью всем пользователям бота.
    """
    new_articles = await get_latest_articles()
    old_articles = await get_articles_from_db()
    for slug in new_articles:
        if slug not in old_articles:
            await refresh_db_articles(slug)
            await send_new_article(slug=slug, bot=bot)
        continue


async def periodic_scraping(
    bot: Bot, interval_sec=settings.scraping_interval_seconds
):
    """
    Функция переодической проверки обновлений.
    Периодичность проверки можно задать в настройках.
    """
    while True:
        await asyncio.sleep(interval_sec)
        await check_for_updates(bot=bot)
