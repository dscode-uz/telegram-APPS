from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.add_box import read_box
def create_menu_categories(db_all_caegories):
    category_menu= InlineKeyboardMarkup(row_width=1)
    category=db_all_caegories
    for i in category:
        category_menu.insert(InlineKeyboardButton(text=i[1],callback_data=i[0]))
    return category_menu


def shop_menu(db_all_categories):
    shop_menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    for i in db_all_categories:
        shop_menu.insert(InlineKeyboardButton(text=i[1], callback_data=f"opt{i[0]}"))

    shop_menu.insert(InlineKeyboardButton(text="🛒 Savatchadan buyurtma berish 🚚", callback_data="optbox"))
    return shop_menu

def go_menu(user_id):
    lenses=len(read_box(user_id))
    if lenses==0:
        return 0
    go_menu=InlineKeyboardMarkup(row_width=1)
    for i in range(lenses):
        go_menu.insert(InlineKeyboardButton(text=f"{i+1} 🗑",callback_data=f"del{i+1}"))
    go_menu.insert(InlineKeyboardButton(text="✅ Buyurtmani rasmiylashtirish",callback_data=f"shop1"))
    go_menu.insert(InlineKeyboardButton(text="🗑 Savatni tozalash",callback_data="shop0"))
    go_menu.insert(InlineKeyboardButton(text="🔙 Ortga",callback_data="shop3"))
    return go_menu

is_ship=InlineKeyboardMarkup(row_width=1)
is_ship.insert(InlineKeyboardButton(text="💳 Hozir to'lov qilaman",callback_data=f"ship1"))
is_ship.insert(InlineKeyboardButton(text="💴 Buyurtma bajarilganda",callback_data="ship0"))

def adding_box(prd_id):
    numkeyboard=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1",callback_data=f"amt{prd_id}1"),
                InlineKeyboardButton(text="2", callback_data=f"amt{prd_id}2"),
                InlineKeyboardButton(text="3", callback_data=f"amt{prd_id}3"),
            ],
            [
                InlineKeyboardButton(text="4", callback_data=f"amt{prd_id}4"),
                InlineKeyboardButton(text="5", callback_data=f"amt{prd_id}5"),
                InlineKeyboardButton(text="6", callback_data=f"amt{prd_id}6"),
            ],
            [
                InlineKeyboardButton(text="7", callback_data=f"amt{prd_id}7"),
                InlineKeyboardButton(text="8", callback_data=f"amt{prd_id}8"),
                InlineKeyboardButton(text="9", callback_data=f"amt{prd_id}9"),
            ],
            [
                InlineKeyboardButton(text="🔙 Ortga", callback_data="shop4"),
            ]
        ]
    )
    return numkeyboard

