import json


import requests
import telebot

from telebot.storage import StateMemoryStorage

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


import api
from config import BOT_TOKEN


from states import States


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)




@bot.message_handler(commands=['start', 'hello-world'])
def start(message):
    bot.send_message(message.chat.id, "Hello world!")


@bot.message_handler(func=lambda message: "привет" in message.text.lower())
def hello(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Здравствуйте, {name}!")



@bot.message_handler(commands=['low'])
def low(message):
    bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")
    bot.set_state(message.from_user.id, States.high, message.chat.id)
    bot.register_next_step_handler(message, low_state)

@bot.message_handler(state=States.low)
def low_state(message):
    user_input_low = int(message.text)
    if user_input_low > 0 and user_input_low <= 12:
        bot.send_message(message.chat.id, "Самые непопулярные игры текущего года:")
        result = api.low(user_input_low)
        json_raw = json.dumps(result, ensure_ascii=False, indent=2)
        bot.send_message(message.chat.id, f'{result}')
    else:
        bot.send_message(message.chat.id, "Неверное число!")
        bot.send_message(message.chat.id, "Введите число от 1 до 12")
        bot.register_next_step_handler(message, low_state)



@bot.message_handler(commands=['high'])
def high(message):
    bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")
    bot.set_state(message.from_user.id, States.high, message.chat.id)
    bot.register_next_step_handler(message, high_state)

@bot.message_handler(state=States.high)
def high_state(message):
    user_input_high = int(message.text)
    if user_input_high > 0 and user_input_high <= 12:
        print(user_input_high)
        bot.send_message(message.chat.id, "Лучшие игры текущего года:")
        result = api.high(user_input_high)
        json_raw = json.dumps(result, ensure_ascii=False, indent=2)
        bot.send_message(message.chat.id, f'{result}')
    else:
        bot.send_message(message.chat.id, "Неверное число!")
        bot.send_message(message.chat.id, "Введите число от 1 до 12")
        bot.register_next_step_handler(message, high_state)



@bot.message_handler(func=lambda message: True)
def default(message):
    bot.send_message(message.chat.id, 'Такой команды нет, меня ещё дорабатывают :)')



if __name__ == '__main__':
    bot.infinity_polling()


