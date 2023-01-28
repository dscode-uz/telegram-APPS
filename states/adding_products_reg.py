from aiogram.dispatcher.filters.state import StatesGroup,State

class new_products_registiration(StatesGroup):
    recent_category=State()
    recent_photo=State()
    recent_name=State()
    recent_coin=State()