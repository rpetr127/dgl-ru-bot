from telebot.async_telebot import AsyncTeleBot, logger
from config.config import *
import logging


logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
bot = AsyncTeleBot(BOT_TOKEN)
