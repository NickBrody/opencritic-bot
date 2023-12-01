import requests
from typing import List, Dict

from config import API_KEY, BASE_URL, UNPOPULAR_URL



# def api_request(endpoint: str, params={}) -> requests.Response:
#     params['key'] = API_KEY
#     return requests.get(
#         f'{BASE_URL}/{endpoint}',
#         params=params
#     )
#


def high(user_input_high):
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


def custom(user_input_custom, year):
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



def low(user_input_low):
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