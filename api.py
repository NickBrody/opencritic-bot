import requests
from config import BASE_URL, UNPOPULAR_URL

"""Функция high - в зависимости от числа введённого пользователем (до 12) создает словарь
 из переменной response, в котором ключ это 'name', а значение - 'topCriticScore'.
Возвращает строку с указанным пользователем количеством пар"""


def high(user_input_high: int) -> str:
    response = requests.get(BASE_URL, headers=headers)
    items_with_name = {}
    string = ""
    data = response.json()
    count = 0
    for item in data[:user_input_high]:
        if 'name' in item:
            if 'topCriticScore' in item:
                items_with_name[item['name']] = item['topCriticScore']
    for k, v in items_with_name.items():
        count += 1
        string += f"{count}. {k} : {int(v)} баллов\n"
    return string


"""Функция custom - принимает 'year', значение которого вводит пользователь в диапазоне 2016-2023. 'year' передаётся 
в 'BASE_URL'. В зависимости от числа введённого пользователем в 'user_input_custom' (до 12) создает словарь из 
переменной response, в котором ключ это 'name', а значение - 'topCriticScore'. Возвращает строку с указанным 
пользователем количеством пар"""


def custom(user_input_custom: int, year: int) -> str:
    response = requests.get(f'{BASE_URL}{year}', headers=headers)
    items_with_name = {}
    string = ""
    data = response.json()
    count = 0
    for item in data[:user_input_custom]:
        if 'name' in item:
            if 'topCriticScore' in item:
                items_with_name[item['name']] = item['topCriticScore']
    for k, v in items_with_name.items():
        count += 1
        string += f"{count}. {k} : {int(v)} баллов\n"
    return string


"""Функция low - в зависимости от числа введённого пользователем (до 12) создает словарь
 из переменной response, в котором ключ это 'name', а значение - 'topCriticScore'.
Возвращает строку с указанным пользователем количеством пар"""


def low(user_input_low: int) -> str:
    response = requests.get(UNPOPULAR_URL, headers=headers)
    items_with_name = {}
    string = ""
    data = response.json()
    count = 0
    for item in data:
        if 'name' in item:
            if 'topCriticScore' in item:
                items_with_name[item['name']] = item['topCriticScore']
    sorted_items = sorted(items_with_name.items(), key=lambda x: x[1], reverse=False)
    for k, v in sorted_items[:user_input_low]:
        count += 1
        string += f"{count}. {k} : {int(v)} баллов\n"
    return string


headers = {
    "X-RapidAPI-Key": "e3a4326918mshca5791a432463abp11a615jsn8884f27bcd9f",
    "X-RapidAPI-Host": "opencritic-api.p.rapidapi.com"
}
