import requests
from bs4 import BeautifulSoup

URL = "https://www.the-race.com/formula-1"

response = requests.get(url=URL)

soup = BeautifulSoup(response.text, "lxml")


def check_updates():
    pass
#  new_articles = []
#  old_articles = []
# for article in new_articles:
#     if article not in old_articles:
#        refresh_db_articles(slug)
#        get_chat_ids
#        for chat_id in chat_ids:
#            bot.send_message
#     continue