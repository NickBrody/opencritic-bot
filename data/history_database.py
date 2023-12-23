from typing import Any
from telebot.types import Message
from data.models import Commands, User
from loader import bot


def creating_history(message: Message) -> None:
    """Добавляет сообщения пользователя в базу данных.
    Args:
    message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    Returns:
    None: Функция не возвращает значения"""
    user_id = message.from_user.id
    Commands.create(
        user=user_id,
        user_message=message.text,
        user_params=None
    )


def show_history(message: Message) -> None:
    """Показывает историю 5 последних запросов вместе с параметрами.
    Args:
    message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    Returns:
    None: Функция не возвращает значения"""
    user = User.get(User.user_id == message.from_user.id)
    messages = Commands.select().where(Commands.user == user).order_by(Commands.id.desc()).limit(5)
    count = 0
    for msg in messages:
        count += 1
        string = ""
        string += f"{count}. Выбранная команда: {msg.user_message}, Параметры: {msg.user_params}"
        bot.send_message(message.chat.id, string)


def get_last_user_choice(user_id: Any) -> Any:
    """Возвращает последний запрос пользователя для проверки в check_value_func.
    Args:
    user_id (Any): Объект, содержащий id пользователя.
    Returns:
    Any: Функция возвращает значение Any."""
    last_message = Commands.select().where(Commands.user == user_id).order_by(Commands.id.desc()).get()
    user_choice = last_message.user_message
    return user_choice
