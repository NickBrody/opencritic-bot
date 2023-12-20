from telebot.types import Message
from data.database_function import history
from handlers.check_value_func import check_value, count
from loader import bot
from states.states import States


@bot.message_handler(commands=['high'])
def high_check_input(message: Message) -> None:
    """Функция high_check_input запрашивает у пользователя год, передавая его в high_return_result.
    Также записывает команду в словарь history"""
    user_id = message.from_user.id
    if user_id in history:
        history[user_id].append(message.text)
        history[user_id] = history[user_id][-10:]
    else:
        history[user_id] = [message.text]
    bot.set_state(message.from_user.id, States.high, message.chat.id)
    bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")


@bot.message_handler(state=States.high)
def high_to_check_value(message: Message) -> None:
    """Функция high_to_check_value переходит в функцию check_value для проверки правильности введённых значений."""
    check_value(message, count)
