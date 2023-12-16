import telebot
from telebot import StateMemoryStorage

from config.config import BOT_TOKEN

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)