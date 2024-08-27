import requests
from bs4 import BeautifulSoup
from api.dicts.dicts import *  # noqa
from config.config import BASE_URL, UNPOPULAR_URL, headers
from handlers.help import help_command

URL_FOR_PARSING = "https://opencritic.com/game/"


def high_api_check(user_input: int) -> None:
    """Функция high_api_check - в зависимости от числа введённого пользователем в 'user_input_custom' (до 12)
    создает словарь из переменной response, в котором ключ это 'name', а значение - 'topCriticScore'.
    Также создаёт словарь со ссылками на jpeg-файлы, которые бот будет отправлять пользователю.
    Args:
    user_input (int): Объект, содержащий введённое пользователем число.
    Returns:
    None: Функция не возвращает значения."""
    response = requests.get(BASE_URL, headers=headers)
    items_with_image_high.clear()
    items_with_name_high.clear()
    data = response.json()
    try:
        for item in data[:user_input]:
            if "images" in item and item["images"]:
                if "box" in item["images"]:
                    items_with_image_high[item['name']] = item["images"]["box"]["og"]
                else:
                    items_with_image_high[item['name']] = item["images"]["banner"]["og"]
                items_with_name_high[item['name']] = item['topCriticScore']
                #items_with_image_high[item['name']] = item["images"]["box"]["og"]
            else:
                pass
    except:
        pass

    for k in dicts_high[0]:
        big_dict_high[k] = [d[k] for d in dicts_high]


def low_api_check(user_input: int) -> None:
    """Функция low_api_check - в зависимости от числа введённого пользователем (до 12) создает словарь
    из переменной response, в котором ключ это 'name', а значение - 'topCriticScore'.
    Также создаёт словарь со ссылками на jpeg-файлы, которые бот будет отправлять пользователю.
    Args:
    user_input (int): Объект, содержащий введённое пользователем число.
    Returns:
    None: Функция не возвращает значения."""
    global sorted_dict
    response = requests.get(UNPOPULAR_URL, headers=headers)
    items_with_image_low.clear()
    items_with_name_low.clear()
    try:
        data = response.json()
        for item in data:
            if "box" in item["images"]:
                items_with_image_low[item['name']] = item["images"]["box"]["og"]
            else:
                items_with_image_low[item['name']] = item["images"]["banner"]["og"]
            items_with_name_low[item['name']] = item['topCriticScore']
            # items_with_image_low[item['name']] = item["images"]["box"]["og"]
        sorted_items = (sorted(items_with_name_low.items(), key=lambda x: x[1], reverse=False))[:user_input]
        sorted_dict = {k: v for k, v in sorted_items}
        sorted_images_low.clear()
        for i in sorted_dict:
            if i in items_with_image_low:
                sorted_images_low[i] = items_with_image_low[i]
        dicts_low = [sorted_dict, sorted_images_low]
        for k in dicts_low[0]:
            big_dict_low[k] = [d[k] for d in dicts_low]
    except:
        pass

def custom_api_check(year: int, user_input: int) -> None:
    """Функция custom_api_check - принимает 'year', значение которого вводит пользователь в диапазоне 2016-2023. 'year' передаётся
    в 'BASE_URL'. В зависимости от числа введённого пользователем в 'user_input_custom' (до 12) создает словарь из
    переменной response, в котором ключ это 'name', а значение - 'topCriticScore'. Также создаёт словарь со ссылками
    на jpeg-файлы, которые бот будет отправлять пользователю.
    Args:
    year (int): Объект, содержащий введённое пользователем число.
    user_input (int): Объект, содержащий введённое пользователем число.
    Returns:
    None: Функция не возвращает значения."""
    response = requests.get(f'{BASE_URL}{year}', headers=headers)
    items_with_image_custom.clear()
    items_with_name_custom.clear()
    data = response.json()
    try:
        for item in data[:user_input]:
            if "images" in item and item["images"]:
                if "box" in item["images"]:
                    items_with_image_custom[item['name']] = item["images"]["box"]["og"]
                else:
                    items_with_image_custom[item['name']] = item["images"]["banner"]["og"]
                items_with_name_custom[item['name']] = item['topCriticScore']
                #items_with_image_custom[item['name']] = item["images"]["box"]["og"]
            else:
                pass
    except:
        pass
    for k in dicts_custom[0]:
        big_dict_custom[k] = [d[k] for d in dicts_custom]


def get_game_api(link):
    """Фукнция get_game_api ищет введённую игру, собирает необходимые данные и записывает в словарь.
    Args:
    user_input (int): Объект, содержащий введённое пользователем число.
    Returns:
    None: Функция не возвращает значения."""
    response = requests.get(URL_FOR_PARSING+link)
    soup = BeautifulSoup(response.text, 'html.parser')

    score = soup.find('div', class_='inner-orb')
    percent = score.find_next('div', class_='inner-orb')
    score_to_bot = score.text.strip() if score else None
    percent_to_bot = percent.text.strip() if score else None

    game_name_parsing = soup.find('h1', class_='mb-0')
    game_to_bot = game_name_parsing.text.strip()

    img_element = soup.find('img', attrs={'_ngcontent-serverapp-c92': ''})
    next_img_element = img_element.find_next('img')
    img_to_bot = next_img_element.get('src') if img_element else None

    game_dict['name'] = game_to_bot
    game_dict['score'] = score_to_bot
    game_dict['img'] = img_to_bot
    game_dict['percent'] = percent_to_bot
