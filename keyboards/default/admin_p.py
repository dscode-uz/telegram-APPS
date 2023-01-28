from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


panel_menu_amin= ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="➕ Mahsulot qo'shish"),
            KeyboardButton(text="➕ Bo'lim qo'shish")
        ],
        [
            KeyboardButton(text='📊 Statistika'),
            KeyboardButton(text="📮 Xabar tarqatish")
        ],
        [
            KeyboardButton(text="🖊 Bazani boshqarish"),
            KeyboardButton(text="🎲 Tasodifiy foydalanuvchi")
        ],
        [
            KeyboardButton(text="🔝 Bosh menu")
        ],
    ],
    resize_keyboard=True
    )