from flask import Flask, request
import telebot

from .bot import bot
from config.config import WEBHOOK_URL, BOT_TOKEN

server = Flask(__name__)


@server.route('/')
async def webhook():
    await bot.delete_webhook()

    # Set webhook
    await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
    return '!', 200


@server.route('/' + BOT_TOKEN, methods=['POST'])
async def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    await bot.process_new_updates([update])
    return "!", 200
