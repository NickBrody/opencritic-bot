from telebot.types import Message
from data.database_registration_warning import database_register_warning
from data.history_database import creating_history
from handlers.check_value_func import check_value, year_data, count
from loader import bot
from states.states import States


@bot.message_handler(commands=['custom'])
def custom_input_year(message: Message) -> None:
    """Функция custom_input_year запрашивает у пользователя год, передавая его в custom_check_input.
    Также записывает команду в словарь history.
    Args:
    message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    Returns:
    None: Функция не возвращает значения."""
    database_register_warning(message)
    creating_history(message)
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Введите искомый год (не раньше 2016)")
    year_data[user_id] = {}
    bot.set_state(message.from_user.id, States.custom_check_year, message.chat.id)


@bot.message_handler(state=States.custom_check_year)
def custom_check_input(message: Message) -> None:
    """Функция custom_check_input проверяет введённый пользователем год до тех пор, пока он не станет
    соответствовать требованиям (ввод должен быть в диапазоне от 2016 до 2023).
    В случае успеха вызывает custom_return_result.
    Args:
    message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    Returns:
    None: Функция не возвращает значения."""
    user_id = message.from_user.id
    try:
        year = int(message.text)
        if 2016 <= year <= 2024:
            year_data[user_id]['year'] = year
            bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")
            bot.set_state(message.from_user.id, States.custom, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Неверный год!")
            bot.send_message(message.chat.id, "Введите год от 2016 до 2024")
            bot.set_state(message.from_user.id, States.custom_check_year, message.chat.id)

    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
        bot.set_state(message.from_user.id, States.custom_check_year, message.chat.id)


@bot.message_handler(state=States.custom)
def custom_return_result(message: Message) -> None:
    """Функция custom_return_result переходит в функцию check_value для проверки правильности введённых значений.
    Args:
    message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    Returns:
    None: Функция не возвращает значения."""
    check_value(message, count)
