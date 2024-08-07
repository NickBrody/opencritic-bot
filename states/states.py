from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    """Класс States состоит из нескольких состояний
    base: Основное начальное состояние диалога
    low: Состояние, использовано для представления самых непопулярных игр
    high: Состояние, использовано для представления самых популярных игр
    custom_check_year: Состояние для проверки года
    custom: Состояние, использовано для представления самых популярных игр в определённом году"""
    base = State()
    low = State()
    high = State()
    custom = State()
    custom_check_year = State()
    game = State()
