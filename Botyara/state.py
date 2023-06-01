from aiogram.dispatcher.filters.state import State, StatesGroup

class MainState(StatesGroup):
    first_message = State()
    second_message = State()
    third_message = State()
    fourth_message = State()
    bot_save_end = State()