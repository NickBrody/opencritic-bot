import json
from sqlite3 import IntegrityError
import telebot
from telebot.storage import StateMemoryStorage
from peewee import IntegrityError
from telebot.types import Message
import api
from config import BOT_TOKEN
from states import States
from models import db, User

db.connect()
db.create_tables([User], safe=True)

history = {}

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)

"""Команда start. Регистрирует пользователя в базе данных, если его там нет.
Сразу же вызывает функцию help для удобства пользователя."""


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
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


"""Команда help, показывает основные команды бота"""


@bot.message_handler(commands=['help'])
def help(message: Message) -> None:
    bot.send_message(message.chat.id, "Выберите функцию:\n"
                                      "/high - Показ лучших игр текущего года\n"
                                      "/low - Показ самых непопулярных игр текущего года\n"
                                      "/custom - Показ лучших игр выбранного года\n"
                                      "/history - Последние 10 ваших запросов")


"""Команда history, записывает запросы пользователей и показывает им их по id.
Выводит последние 10 запросов от последнего к первому"""


@bot.message_handler(commands=['history'])
def add_history(message: Message) -> None:
    user_id = message.from_user.id
    try:
        bot.send_message(message.chat.id, f"История ваших запросов: {', '.join(reversed(history[user_id]))}")
        help(message)
    except KeyError:
        bot.send_message(message.chat.id, "У вас ещё нет истории запросов")
        help(message)


"""Приветствует пользователя на сообщение 'привет'. Аналог функции start"""


@bot.message_handler(func=lambda message: "привет" in message.text.lower())
def hello(message: Message) -> None:
    start(message)


"""Команда low, показывает до 12 самых непопулярных игр текущего года.
Осуществляет контроль ввода, выводя понятные для пользователя сообщения в случае ошибки"""


@bot.message_handler(commands=['low'])
def low(message: Message) -> None:
    user_id = message.from_user.id
    if user_id in history:
        history[user_id].append(message.text)
        history[user_id] = history[user_id][-10:]
    else:
        history[user_id] = [message.text]
    bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")
    bot.set_state(message.from_user.id, States.low, message.chat.id)
    bot.register_next_step_handler(message, low_func)


@bot.message_handler(state=States.low)
def low_func(message: Message) -> None:
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
            bot.register_next_step_handler(message, low_func)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
        bot.register_next_step_handler(message, low_func)


"""Команда high, показывает до 12 самых популярных игр текущего года.
Осуществляет контроль ввода, выводя понятные для пользователя сообщения в случае ошибки"""


@bot.message_handler(commands=['high'])
def high(message: Message) -> None:
    user_id = message.from_user.id
    if user_id in history:
        history[user_id].append(message.text)
        history[user_id] = history[user_id][-10:]
    else:
        history[user_id] = [message.text]
    bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")
    bot.set_state(message.from_user.id, States.high, message.chat.id)
    bot.register_next_step_handler(message, high_func)


@bot.message_handler(state=States.high)
def high_func(message: Message) -> None:
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
            bot.register_next_step_handler(message, high_func)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
        bot.register_next_step_handler(message, high_func)


"""Команда custom, показывает до 12 самых популярных игр выбранного года.
Пользователь может выбирать год в диапазоне от 2016 до 2023 года.
Осуществляет контроль ввода, выводя понятные для пользователя сообщения в случае ошибки"""


@bot.message_handler(commands=['custom'])
def custom_year(message: Message) -> None:
    user_id = message.from_user.id
    if user_id in history:
        history[user_id].append(message.text)
        history[user_id] = history[user_id][-10:]
    else:
        history[user_id] = [message.text]
    bot.send_message(message.chat.id, "Введите искомый год (не раньше 2016)")
    bot.set_state(message.from_user.id, States.custom, message.chat.id)
    bot.register_next_step_handler(message, custom)


def custom(message: Message) -> None:
    try:
        year = int(message.text)
        if 2016 <= year <= 2023:
            bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")
            bot.set_state(message.from_user.id, States.custom, message.chat.id)
            bot.register_next_step_handler(message, custom_func, year)
        else:
            bot.send_message(message.chat.id, "Неверный год!")
            bot.send_message(message.chat.id, "Введите год от 2016 до 2023")
            bot.register_next_step_handler(message, custom)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
        bot.register_next_step_handler(message, custom)


@bot.message_handler(state=States.custom)
def custom_func(message: Message, year: int) -> None:
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
            bot.register_next_step_handler(message, custom_func, year)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
        bot.register_next_step_handler(message, custom_func, year)


"""Хэндлер для контроля ввода правильных команд. Содержит понятное для пользователя сообщение"""


@bot.message_handler(func=lambda message: True)
def default(message: Message) -> None:
    bot.send_message(message.chat.id, f"Неверный ввод! Введите команду /help для просмотра функций бота")


if __name__ == '__main__':
    bot.infinity_polling()
