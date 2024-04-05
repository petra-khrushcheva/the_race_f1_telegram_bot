import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message
from aiogram.utils.markdown import hlink
from sqlalchemy import Result, delete, select

from bot.models import ChatID
from core import async_session
from scraper import Article


async def save_chat_id_to_db(chat_id: int):
    """
    Сохранение чат айди в базу данных.
    Вызывается при вызове команды /start пользователем бота.
    """
    async with async_session() as session:
        if not (
            await session.execute(
                select(ChatID).where(ChatID.chat_id == chat_id)
            )
        ).scalar_one_or_none():
            new_chat_id = ChatID(chat_id=chat_id)
            session.add(new_chat_id)
            await session.commit()


async def get_chat_ids():
    """
    Получение всех чат айди из базы данных.
    Вызывается из функции рассылки новых статей.
    """
    async with async_session() as session:
        result: Result = await session.execute(select(ChatID.chat_id))
        return result.scalars().all()


async def delete_chat_id(chat_id):
    """
    Удаление чат айди из базы данных.
    Вызывается при ошибке TelegramForbiddenError,
    то есть когда пользователь заблокировал бота.
    """
    async with async_session() as session:
        await session.execute(delete(ChatID).where(ChatID.chat_id == chat_id))
        await session.commit()


async def get_articles_from_db():
    """
    Получение слагов всех (трех) новейших статей, хранящихся в базе данных.
    Используется для отправки первых статей при запуске бота.
    Вызывается из функции send_initial_articles.
    """
    async with async_session() as session:
        result: Result = await session.execute(
            select(Article.slug).order_by(Article.created_at)
        )
        return result.scalars().all()


async def send_article(chat_id: int | str, slug: str, bot: Bot):
    """Функция отправки одной статьи пользователю бота."""
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=hlink(
                url=f"https://www.the-race.com/formula-1/{slug}/", title="🏎️"
            ),
        )
    except TelegramForbiddenError:
        await delete_chat_id(chat_id=chat_id)


async def send_initial_articles(message: Message):
    """
    Отправка трех последних статей. Выполняется при вызове
    команды /start пользователем бота.
    """
    slugs = await get_articles_from_db()
    for slug in slugs:
        await send_article(chat_id=message.chat.id, slug=slug, bot=message.bot)


async def send_new_article(slug: str, bot: Bot):
    """
    Отправка новейшей статьи всем пользователем бота.
    Используется в общей функции check_for_updates.
    """
    chat_ids = await get_chat_ids()
    for chat_id in chat_ids:
        await send_article(chat_id=chat_id, slug=slug, bot=bot)
        await asyncio.sleep(0.05)
