import asyncio
import re
import sqlite3
from datetime import datetime

import pytz
import telebot
from flask import Flask, request

from .bot import bot, logger
from config.config import BOT_TOKEN, WEBAPP_HOST, WEBAPP_PORT
from .run_server import server
from parser import RSSParser
CHAT_ID = 909040171
sent_messages_quantity = int()

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('../db/database.db')
        self.cursor = self.connection.cursor()

    def add_data(self, *args):
        self.cursor.execute('INSERT INTO my_messages (chat_id, message, publish_date) values(?, ?, ?)', args)
        self.connection.commit()

    def update_messages(self, chat_id, message, pub_date):
        self.cursor.execute('UPDATE my_messages SET publish_date=?, message=? WHERE chat_id=?', (
            pub_date, message, chat_id))
        self.connection.commit()

    def select_data(self):
        result = self.cursor.execute("SELECT message, publish_date FROM my_messages").fetchone()
        return result


db = Database()


class Article:
    def __init__(self):
        parser = RSSParser('https://www.dgl.ru/feed')
        self.feed = parser.parse()

    @property
    def article_text(self):
        self._article_text = self.feed[0].title + '\n\n' + self.feed[0].description + '\n' + self.feed[0].link
        return self._article_text

    def is_now_published(self):
        data = db.select_data()
        pub_date = self.feed[0].publish_date
        s1 = re.search(r'\d+:\d+', pub_date).group(0)
        logger.info(str(s1))
        s2 = datetime.now(pytz.UTC).strftime('%H:%M')
        logger.info(f'{s1}, {s2}')
        current_hour = datetime.now(pytz.UTC).hour
        if data is None or data[0] != self.article_text and s1 == s2:
            return True
        elif current_hour in range(11, 13) and sent_messages_quantity == 0:
            return False


def save_data(chat_id, text, pub_date):
    data = db.select_data()
    if data is None:
        db.add_data(chat_id, text, pub_date)
    else:
        db.update_messages(chat_id, text, pub_date)


async def broadcaster():
    global sent_messages_quantity
    while True:
        article = Article()
        if article.is_now_published():
            article_feed = article.feed[0]
            photo = article_feed.content_image
            text = article.article_text
            pub_date = article_feed.publish_date
            if datetime.now().hour != 23:
                sent_messages_quantity += 1
                if photo:
                    m = await bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=text)
                else:
                    m = await bot.send_message(chat_id=CHAT_ID, text=text, disable_web_page_preview=True)
                save_data(m.chat.id, text, pub_date)
            else:
                sent_messages_quantity = 0
                save_data(CHAT_ID, text, pub_date)
        else:
            continue
        await asyncio.sleep(30.0)


@server.route('/' + BOT_TOKEN, methods=['POST'])
async def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    await bot.process_new_updates([update])
    return "!", 200



# run broadcast function
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(broadcaster())

    #run server
    server.run(host=WEBAPP_HOST, port=WEBAPP_PORT)
