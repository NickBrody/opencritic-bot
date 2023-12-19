import os
from dotenv import load_dotenv, find_dotenv
if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

headers = {
    "X-RapidAPI-Key": os.getenv("API_KEY"),
    "X-RapidAPI-Host": os.getenv("API_HOST")
}

BASE_URL = 'https://opencritic-api.p.rapidapi.com/game/hall-of-fame/'

UNPOPULAR_URL = "https://opencritic-api.p.rapidapi.com/game/popular"

PIC_URL = "https://img.opencritic.com/"
