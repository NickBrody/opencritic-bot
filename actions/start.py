import telebot

def start_bot(bot, message):
    bot.send_message(message.chat.id, "Hello world!")

def handle_hello(bot, message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Здравствуйте, {name}!")

def nothing(bot, message):
    bot.send_message(message.chat.id, 'Такой команды нет, меня ещё дорабатывают :)')