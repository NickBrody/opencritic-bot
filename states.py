from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    base = State()
    high = State()
    low = State()
    custom = State()
