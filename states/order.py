from aiogram.dispatcher.filters.state import StatesGroup, State


class Order(StatesGroup):
    P1 = State()
    P2 = State()
