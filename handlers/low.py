import json
from telebot.types import Message
from config import api
from data.history_data import history
from handlers.help import help_command
from loader import bot
from states.states import States


@bot.message_handler(commands=['low'])
def low_check_input(message: Message) -> None:
    """Функция low_check_input запрашивает у пользователя год, передавая его в low_return_result.
    Также записывает команду в словарь history"""
    user_id = message.from_user.id
    if user_id in history:
        history[user_id].append(message.text)
        history[user_id] = history[user_id][-10:]
    else:
        history[user_id] = [message.text]

    bot.set_state(message.from_user.id, States.low, message.chat.id)
    bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")


@bot.message_handler(state=States.low)
def low_return_result(message: Message) -> None:
    """Функция low_return_result проверяет введённое пользователем число до тех пор, пока оно не станет
    соответствовать требованиям (ввод должен быть в диапазоне от 1 до 12).
    В случае успеха вызывает low_api_check из файла api.py. Сразу после вызывает функцию help_command для удобства
    пользователя."""
    try:
        user_input_low = int(message.text)
        if 0 < user_input_low <= 12:
            bot.send_message(message.chat.id, "Самые непопулярные игры текущего года:")
            result = api.low_api_check(user_input_low)
            json_raw = json.dumps(result, ensure_ascii=False, indent=2)
            bot.send_message(message.chat.id, f'{result}')
            bot.set_state(message.from_user.id, States.base, message.chat.id)
            help_command(message)
        else:
            bot.send_message(message.chat.id, "Неверное число!")
            bot.send_message(message.chat.id, "Введите число от 1 до 12")
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")