from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from loader import db

def view_category_menu():
    category_menu= ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
    category=db.select_all_categories()
    for i in category:
        category_menu.insert(KeyboardButton(text=i[1]))
    return category

def view_shop_menu():
    shop_menu=view_category_menu()
    shop_menu.insert("🛒 Savatchadan buyurtma berish 🚚")
    shop_menu.insert(KeyboardButton(text="🔙 Ortga"))
    return shop_menu



break_menu=ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
break_menu.insert(KeyboardButton(text="❌ Bekor qilish"))

cancel_menu=ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
cancel_menu.insert(KeyboardButton(text="🔙 Ortga"))

start_menu= ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="🛒 Xarid qilish 🛍"),
        ],
        [
            KeyboardButton(text="📑 Yordam 🧾"),
        ],
    ],
    resize_keyboard=True
    )

start_menu_admin= ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="👤 Foydalanuvchi sifatida kirish")
        ],
        [
            KeyboardButton(text="💻 Admin panelga o'tish")
        ],
    ],
    resize_keyboard=True
    )

go_menu=ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
go_menu.insert(KeyboardButton(text="✅ Buyurtmani rasmiylashtirish"))
go_menu.insert(KeyboardButton(text="🗑 Savatni tozalash"))
go_menu.insert(KeyboardButton(text="🔙 Ortga"))

location=ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
location.insert(KeyboardButton(text="📍 Manzilni yuborish",request_location=True))
location.insert(KeyboardButton(text="🔙 Ortga"))

phone_num=ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
phone_num.insert(KeyboardButton(text="📞",request_contact=True))
phone_num.insert(KeyboardButton(text="🔙 Ortga"))