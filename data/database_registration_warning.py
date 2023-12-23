from telebot.types import Message
from data.models import User
from handlers.start import bot_start


def database_register_warning(message: Message) -> None:
    """Если пользователь отсутствует в базе данных, то функция добавляет его туда. Иначе ничего не делает.
    Args:
    message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    Returns:
    None: Функция не возвращает значения"""
    user_id = message.from_user.id
    if User.filter(user_id=user_id).first():
        pass
    else:
        bot_start(message)
