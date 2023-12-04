import json
import telebot
from telebot.types import Message
from telebot import custom_filters
from telebot.storage import StateMemoryStorage

from actions.start import start_bot, handle_hello, nothing
import api
from config import BOT_TOKEN

# from states import States


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)


@bot.message_handler(commands=['start', 'hello-world'])
def start(message):
    start_bot(bot, message)


@bot.message_handler(func=lambda message: "привет" in message.text.lower())
def hello(message):
    handle_hello(bot, message)


@bot.message_handler(func=lambda message: True)
def default(message):
    nothing(bot, message)


if __name__ == '__main__':
    bot.infinity_polling()
