import asyncio

from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError
from sqlalchemy import Result, select

from bot.models import ChatID
from bot.main import bot
from core.database import async_session
from scraper.models import Article


async def save_chat_id_to_db(chat_id: int):
    async with async_session() as session:
        if not (
            await session.execute(select(ChatID).where(chat_id == chat_id))
        ).scalar_one_or_none():
            new_chat_id = ChatID(chat_id=chat_id)
            session.add(new_chat_id)
            await session.commit()


async def get_chat_ids():
    async with async_session() as session:
        result: Result = await session.execute(select(ChatID.chat_id))
        return result.scalars().all()


async def get_articles_from_db():
    async with async_session() as session:
        result: Result = await session.execute(
            select(Article.slug).order_by(Article.created_at)
        )
        return result.scalars().all()


async def send_initial_articles(message: Message):
    slugs = await get_articles_from_db()
    for slug in slugs:
        try:
            await message.answer(
                text=f"https://www.the-race.com/formula-1/{slug}/"
            )
        except TelegramForbiddenError:
            pass


async def send_new_article(slug):
    chat_ids = get_chat_ids()
    for chat_id in chat_ids:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=f"https://www.the-race.com/formula-1/{slug}/",
            )
            await asyncio.sleep(0.05)
        except TelegramForbiddenError:
            pass
