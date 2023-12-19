from api import api
from api.api import big_dict_high, big_dict_low, big_dict_custom
from config.config import PIC_URL
from data.database_function import history
from handlers.help import help_command
from loader import bot
from states.states import States

year_data = {}

count = 0


def check_value(message, count):
    """Функция check_value проверяет введённое пользователем число до тех пор, пока оно не станет
    соответствовать требованиям (ввод должен быть в диапазоне от 1 до 12).
    В случае успеха вызывает функцию из файла api.py в зависимости от того, какой командой пользователь
    попал в check_value. Отправляет пользователю запрашиваемую конечную информацию.
    Сразу после вызывает функцию help_command для удобства пользователя."""
    try:
        user_input = int(message.text)
        if 0 < user_input <= 12:
            user_id = message.from_user.id
            user_choice = history[user_id][-1]

            if user_choice == "/high":
                big_dict_high.clear()
                bot.send_message(message.chat.id, "Лучшие игры текущего года:")
                api.high_api_check(user_input)
                for k, v in big_dict_high.items():
                    count += 1
                    msg = f"{count}. {k}: {v[1]} баллов"
                    photo_path = f"{PIC_URL}{v[0]}\n"
                    bot.send_photo(message.chat.id, photo=photo_path, caption=msg)

            elif user_choice == "/low":
                big_dict_low.clear()
                bot.send_message(message.chat.id, "Самые непопулярные игры текущего года:")
                api.low_api_check(user_input)
                for k, v in big_dict_low.items():
                    count += 1
                    msg = f"{count}. {k}: {round(v[0])} баллов"
                    photo_path = f"{PIC_URL}{v[1]}\n"
                    bot.send_photo(message.chat.id, photo=photo_path, caption=msg)

            elif user_choice == "/custom":
                big_dict_custom.clear()
                user_info = year_data.get(user_id, {})
                year = user_info.get('year')
                bot.send_message(message.chat.id, f"Самые крутые игры {year} года:")
                api.custom_api_check(user_input, year)
                for k, v in big_dict_custom.items():
                    count += 1
                    msg = f"{count}. {k}: {v[1]} баллов"
                    photo_path = f"{PIC_URL}{v[0]}\n"
                    bot.send_photo(message.chat.id, photo=photo_path, caption=msg)
            bot.set_state(message.from_user.id, States.base, message.chat.id)
            help_command(message)

        else:
            bot.send_message(message.chat.id, "Неверное число!")
            bot.send_message(message.chat.id, "Введите число от 1 до 12")
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Введите число вместо букв.")
