from telebot.types import Message
from data.database_function import database_check
from loader import bot
from states.states import States


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """Функция bot_start. Запускает функцию для регистрации пользователя в базе данных, если его там нет."""
    database_check(message)
    bot.set_state(message.from_user.id, States.base, message.chat.id)


@bot.message_handler(func=lambda message: "привет" in message.text.lower())
def bot_say_hello(message: Message) -> None:
    """Приветствует пользователя на сообщение 'привет'. Аналог функции start"""
    bot_start(message)

