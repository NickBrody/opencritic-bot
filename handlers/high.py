from telebot.types import Message
from data.database_registration_warning import database_register_warning
from data.history_database import creating_history
from handlers.check_value_func import check_value, count
from loader import bot
from states.states import States


@bot.message_handler(commands=['high'])
def high_check_input(message: Message) -> None:
    """Функция high_check_input запрашивает у пользователя год, передавая его в high_return_result.
    Args:
    message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    Returns:
    None: Функция не возвращает значения."""
    database_register_warning(message)
    creating_history(message)
    bot.set_state(message.from_user.id, States.high, message.chat.id)
    bot.send_message(message.chat.id, "Введите количество игр (не больше 12)")



@bot.message_handler(state=States.high)
def high_to_check_value(message: Message) -> None:
    """Функция high_to_check_value переходит в функцию check_value для проверки правильности введённых значений.
    Args:
    message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    Returns:
    None: Функция не возвращает значения."""
    check_value(message, count)
