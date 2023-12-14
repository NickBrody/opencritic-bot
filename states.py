from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    high = State()
    low = State()
    custom = State()
