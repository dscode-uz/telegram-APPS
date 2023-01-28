from aiogram.dispatcher.filters.state import StatesGroup,State

class new_shipping(StatesGroup):
    fio = State()
    location=State()
    phone_number=State()
    end_ship=State()