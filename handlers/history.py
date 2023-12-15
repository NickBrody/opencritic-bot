from telebot.types import Message
from data.history_data import history
from handlers.help import help_command
from loader import bot


@bot.message_handler(commands=['history'])
def check_history(message: Message) -> None:
    """Команда history, записывает запросы пользователей и показывает им их по id.
    Выводит последние 10 запросов от последнего к первому"""
    user_id = message.from_user.id
    try:
        bot.send_message(message.chat.id, f"История ваших запросов: {', '.join(reversed(history[user_id]))}")
        help_command(message)
    except KeyError:
        bot.send_message(message.chat.id, "У вас ещё нет истории запросов")
        help_command(message)
