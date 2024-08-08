import requests
from telebot.types import Message
from data.database_registration_warning import database_register_warning
from data.history_database import creating_history
from handlers.check_value_func import check_value, count
from loader import bot
from states.states import States
from config import config
from config.config import GAME_URL
from api.api import get_game_api
from api.dicts.dicts import game_dict
from data.models import Commands

@bot.message_handler(commands=['game'])
def game_input(message: Message) -> None:
    # """Функция high_check_input запрашивает у пользователя год, передавая его в high_return_result.
    # Args:
    # message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    # Returns:
    # None: Функция не возвращает значения."""
    database_register_warning(message)
    creating_history(message)
    bot.set_state(message.from_user.id, States.game, message.chat.id)
    bot.send_message(message.chat.id, "Введите полное название игры")



@bot.message_handler(state=States.game)
def game_search(message: Message) -> None:
    # """Функция high_to_check_value переходит в функцию check_value для проверки правильности введённых значений.
    # Args:
    # message (Message): Объект сообщения, содержащий введённое пользователем сообщение.
    # Returns:
    # None: Функция не возвращает значения."""
    user_game = message.text
    querystring = {"criteria":user_game}
    response = requests.get(GAME_URL, headers=config.headers, params=querystring)
    bot.send_message(message.chat.id, "Поиск игры...")

    user_string = message.text
    user_id = message.from_user.id
    command = Commands.select().where(Commands.user == user_id).order_by(Commands.id.desc()).get()
    command.user_params = user_string
    command.save()

    games_list = response.json()
    game_id = str(games_list[0]["id"])
    game_title = str(games_list[0]["name"]).replace(" ", "-").replace(":", "-").lower()
    game_link = game_id + "/" + game_title

    get_game_api(game_link)

    msg = f"{game_dict['name']} - {game_dict["score"]} баллов"
    photo_path = game_dict['img']
    bot.send_photo(message.chat.id, photo=photo_path, caption=msg)
    
 