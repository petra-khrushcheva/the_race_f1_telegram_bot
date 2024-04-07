![Workflow badge](https://github.com/petra-khrushcheva/the_race_f1_telegram_bot/actions/workflows/main.yml/badge.svg)

# Телеграм бот The Race - Formula 1 🏎️

Парсер проверяет обновления сайта The Race - Formula 1, и присылает свежие статьи всем подписчикам телеграм бота. 
Chat-id подписчиков и последние статьи сохраняются в базу данных PostgreSQL.
***
### Технологии
Aiogram 3.4  
SQLAlchemy 2.0  
Beautifulsoup4 4.12  
Aiohttp 3.9  
PostgreSQL  
Pydantic settings 2.2  
Alembic 1.13  
***
### Установка
- Создайте бота через [@BotFather](https://t.me/botfather) по [инструкции](https://core.telegram.org/bots/tutorial#obtain-your-bot-token).
- Добавьте описание и команды для своего бота из файла [bot_texts.txt](https://github.com/petra-khrushcheva/the_race_f1_telegram_bot/blob/main/bot_texts.txt).
- Клонируйте проект:
```
git clone git@github.com:petra-khrushcheva/the_race_f1_telegram_bot.git
``` 
- Перейдите в директорию the_race_f1_telegram_bot:
```
cd the_race_f1_telegram_bot
``` 
- Cоздайте переменные окружения по [образцу](https://github.com/petra-khrushcheva/the_race_f1_telegram_bot/blob/main/.env.example).
- Запустите Docker-compose:
```
docker compose -f docker-compose-dev.yml up
``` 
Готово! It's lights out and away we go!
