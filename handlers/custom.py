import json
from telebot.types import Message
from config import api
from data.history_data import history
from handlers.help import help_command
from loader import bot
from states.states import States

year_data = {}


@bot.message_handler(commands=['custom'])
def custom_input_year(message: Message) -> None:
    """Функция custom_input_year запрашивает у пользователя год, передавая его в custom_check_input.
    Также записывает команду в словарь history"""
    user_id = message.from_user.id
    if user_id in history:
        history[user_id].append(message.text)
        history[user_id] = history[user_id][-10:]
    else:
        history[user_id] = [message.text]
    bot.send_message(message.chat.id, "Введите искомый год (не раньше 2016)")
    year_data[user_id] = {}
    bot.set_state(message.from_user.id, States.custom_check_year, message.chat.id)


@bot.message_handler(state=States.custom_check_year)
def custom_check_input(message: Message) -> None:
    """Функция custom_check_input проверяет введённый пользователем год до тех пор, пока он не станет
    соответствовать требованиям (ввод должен быть в диапазоне от 2016 до 2023).
    В случае успеха вызывает custom_return_result"""
    user_id = message.from_user.id
    try:
        year = int(message.text)
        if 2016 <= year <= 2023:
            year_data[user_id]['year'] = year
            bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")
            bot.set_state(message.from_user.id, States.custom, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Неверный год!")
            bot.send_message(message.chat.id, "Введите год от 2016 до 2023")
            bot.set_state(message.from_user.id, States.custom_check_year, message.chat.id)

    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
        bot.set_state(message.from_user.id, States.custom_check_year, message.chat.id)


@bot.message_handler(state=States.custom)
def custom_return_result(message: Message) -> None:
    """Функция custom_return_result проверяет введённое пользователем число до тех пор, пока оно не станет
    соответствовать требованиям (ввод должен быть в диапазоне от 1 до 12).
    В случае успеха вызывает custom_api_check из файла api.py. Сразу после вызывает функцию help_command для удобства
    пользователя."""
    user_id = message.from_user.id
    user_info = year_data.get(user_id, {})
    year = user_info.get('year')
    try:
        user_input_custom = int(message.text)
        if 0 < user_input_custom <= 12:
            bot.send_message(message.chat.id, f"Самые крутые игры {year} года:")
            result = api.custom_api_check(user_input_custom, year)
            json_raw = json.dumps(result, ensure_ascii=False, indent=2)
            bot.send_message(message.chat.id, f'{result}')
            bot.set_state(message.from_user.id, States.base, message.chat.id)
            help_command(message)
        else:
            bot.send_message(message.chat.id, "Неверное число!")
            bot.send_message(message.chat.id, "Введите число от 1 до 12")
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
