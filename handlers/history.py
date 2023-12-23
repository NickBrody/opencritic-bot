from telebot.types import Message
from data.history_database import show_history
from handlers.help import help_command
from loader import bot


@bot.message_handler(commands=['history'])
def check_history(message: Message) -> None:
    """Команда history, выводит последние 5 запросов от последнего к первому.
    Args:
    message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    Returns:
    None: Функция не возвращает значения."""
    show_history(message)
    help_command(message)