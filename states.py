from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    base = State()
    low = State()
    high = State()
    custom = State()
    custom_check_year = State()
