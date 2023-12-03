import json
from sqlite3 import IntegrityError

import requests
import telebot
from telebot.storage import StateMemoryStorage
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from peewee import IntegrityError

from models import db, User



import api
from config import BOT_TOKEN
from states import States


db.connect()
db.create_tables([User], safe=True)

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)


@bot.message_handler(commands=['start', 'hello-world'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        User.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        bot.reply_to(message, f"Здравствуйте! Я - бот для поиска самых лучших игр последних лет! "
                                      f"Введите команду /help для начала работы с ботом.")
    except IntegrityError:
        bot.reply_to(message, f"Рад вас снова видеть, {first_name}!"
                              f" Введите команду /help для начала работы с ботом.")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Выберите функцию:\n"
                                      "/high - Показ лучших игр текущего года\n"
                                      "/low - Показ самых непопулярных игр текущего года\n"
                                      "/custom - Показ лучших игр выбранного года\n")


@bot.message_handler(func=lambda message: "привет" in message.text.lower())
def hello(message):
    start(message)


@bot.message_handler(commands=['low'])
def low(message):
    bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")
    bot.set_state(message.from_user.id, States.high, message.chat.id)
    bot.register_next_step_handler(message, low_state)


@bot.message_handler(state=States.low)
def low_state(message):
    try:
        user_input_low = int(message.text)
        if 0 < user_input_low <= 12:
            bot.send_message(message.chat.id, "Самые непопулярные игры текущего года:")
            result = api.low(user_input_low)
            json_raw = json.dumps(result, ensure_ascii=False, indent=2)
            bot.send_message(message.chat.id, f'{result}')
            help(message)

        else:
            bot.send_message(message.chat.id, "Неверное число!")
            bot.send_message(message.chat.id, "Введите число от 1 до 12")
            bot.register_next_step_handler(message, low_state)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
        bot.register_next_step_handler(message, low_state)


@bot.message_handler(commands=['high'])
def high(message):
    bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")
    bot.set_state(message.from_user.id, States.high, message.chat.id)
    bot.register_next_step_handler(message, high_state)


@bot.message_handler(state=States.high)
def high_state(message):
    try:
        user_input_high = int(message.text)
        if 0 < user_input_high <= 12:
            bot.send_message(message.chat.id, "Лучшие игры текущего года:")
            result = api.high(user_input_high)
            json_raw = json.dumps(result, ensure_ascii=False, indent=2)
            bot.send_message(message.chat.id, f'{result}')
            help(message)
        else:
            bot.send_message(message.chat.id, "Неверное число!")
            bot.send_message(message.chat.id, "Введите число от 1 до 12")
            bot.register_next_step_handler(message, high_state)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
        bot.register_next_step_handler(message, high_state)


@bot.message_handler(commands=['custom'])
def custom_year(message):
    bot.send_message(message.chat.id, "Введите искомый год (не раньше 2016)")
    bot.set_state(message.from_user.id, States.custom, message.chat.id)
    bot.register_next_step_handler(message, custom)


def custom(message):
    try:
        year = int(message.text)
        if 2016 <= year <= 2023:
            bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")
            bot.set_state(message.from_user.id, States.custom, message.chat.id)
            bot.register_next_step_handler(message, custom_state, year)
        else:
            bot.send_message(message.chat.id, "Неверный год!")
            bot.send_message(message.chat.id, "Введите год от 2016 до 2023")
            bot.register_next_step_handler(message, custom)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
        bot.register_next_step_handler(message, custom)


@bot.message_handler(state=States.custom)
def custom_state(message, year):
    try:
        user_input_custom = int(message.text)
        if 0 < user_input_custom <= 12:
            bot.send_message(message.chat.id, f"Самые крутые игры {year} года:")
            result = api.custom(user_input_custom, year)
            json_raw = json.dumps(result, ensure_ascii=False, indent=2)
            bot.send_message(message.chat.id, f'{result}')
            help(message)
        else:
            bot.send_message(message.chat.id, "Неверное число!")
            bot.send_message(message.chat.id, "Введите число от 1 до 12")
            bot.register_next_step_handler(message, custom_state, year)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
        bot.register_next_step_handler(message, custom_state, year)


@bot.message_handler(func=lambda message: True)
def default(message):
    bot.send_message(message.chat.id, f"Неверный ввод! Введите команду /help для просмотра функций бота")


if __name__ == '__main__':
    bot.infinity_polling()
