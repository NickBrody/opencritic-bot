from telebot.types import Message
from telebot.custom_filters import StateFilter

from loader import bot
from data.models import db, User

from handlers import custom, help, high, history, low, start

db.connect()
db.create_tables([User], safe=True)


@bot.message_handler(func=lambda message: True)
def default(message: Message) -> None:
    """Хэндлер для контроля ввода правильных команд. Содержит понятное для пользователя сообщение"""
    bot.send_message(message.chat.id, f"Неверный ввод! Введите команду /help для просмотра функций бота")


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()
