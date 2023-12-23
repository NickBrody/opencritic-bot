from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['help'])
def help_command(message: Message) -> None:
    """Функция help_command, показывает основные команды бота.
    Args:
    message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    Returns:
    None: Функция не возвращает значения."""
    bot.send_message(message.chat.id, "Выберите функцию:\n"
                                      "/high - Показ лучших игр текущего года\n"
                                      "/low - Показ самых непопулярных игр текущего года\n"
                                      "/custom - Показ лучших игр выбранного года\n"
                                      "/history - Последние 5 ваших запросов")
