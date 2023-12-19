from peewee import IntegrityError
from data.models import User
from loader import bot

history = {}


def database_check(message):
    """Функция database_check. Регистрирует пользователя в базе данных, если его там нет.
     После приветствует пользователя"""
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
