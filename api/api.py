import requests

from api.dicts.dicts import * #noqa
from config.config import BASE_URL, UNPOPULAR_URL, headers


def high_api_check(user_input: int) -> None:
    """Функция high_api_check - в зависимости от числа введённого пользователем в 'user_input_custom' (до 12)
    создает словарь из переменной response, в котором ключ это 'name', а значение - 'topCriticScore'.
    Также создаёт словарь со ссылками на jpeg-файлы, которые бот будет отправлять пользователю."""
    response = requests.get(BASE_URL, headers=headers)
    items_with_image_high.clear()
    items_with_name_high.clear()
    data = response.json()
    for item in data[:user_input]:
        items_with_name_high[item['name']] = item['topCriticScore']
        items_with_image_high[item['name']] = item["images"]["box"]["og"]
    for k in dicts_high[0]:
        big_dict_high[k] = [d[k] for d in dicts_high]


def low_api_check(user_input: int) -> None:
    """Функция low_api_check - в зависимости от числа введённого пользователем (до 12) создает словарь
    из переменной response, в котором ключ это 'name', а значение - 'topCriticScore'.
    Также создаёт словарь со ссылками на jpeg-файлы, которые бот будет отправлять пользователю."""
    global sorted_dict
    response = requests.get(UNPOPULAR_URL, headers=headers)
    items_with_image_low.clear()
    items_with_name_low.clear()
    data = response.json()
    for item in data:
        items_with_name_low[item['name']] = item['topCriticScore']
        items_with_image_low[item['name']] = item["images"]["box"]["og"]
    sorted_items = (sorted(items_with_name_low.items(), key=lambda x: x[1], reverse=False))[:user_input]
    sorted_dict = {k: v for k, v in sorted_items}
    sorted_images_low.clear()
    for i in sorted_dict:
        if i in items_with_image_low:
            sorted_images_low[i] = items_with_image_low[i]
    dicts_low = [sorted_dict, sorted_images_low]
    for k in dicts_low[0]:
        big_dict_low[k] = [d[k] for d in dicts_low]


def custom_api_check(user_input: int, year: int) -> None:
    """Функция custom_api_check - принимает 'year', значение которого вводит пользователь в диапазоне 2016-2023. 'year' передаётся
    в 'BASE_URL'. В зависимости от числа введённого пользователем в 'user_input_custom' (до 12) создает словарь из
    переменной response, в котором ключ это 'name', а значение - 'topCriticScore'. Также создаёт словарь со ссылками
     на jpeg-файлы, которые бот будет отправлять пользователю."""
    response = requests.get(f'{BASE_URL}{year}', headers=headers)
    items_with_image_custom.clear()
    items_with_name_custom.clear()
    data = response.json()
    for item in data[:user_input]:
        items_with_name_custom[item['name']] = item['topCriticScore']
        if "box" in item["images"]:
            items_with_image_custom[item['name']] = item["images"]["box"]["og"]
        else:
            items_with_image_custom[item['name']] = item["images"]["banner"]["og"]
    for k in dicts_custom[0]:
        big_dict_custom[k] = [d[k] for d in dicts_custom]

