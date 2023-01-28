from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
def create_menu_categories(db_all_caegories):
    category_menu= InlineKeyboardMarkup(row_width=1)
    category=db_all_caegories
    for i in category:
        category_menu.insert(InlineKeyboardButton(text=i[1],callback_data=i[0]))
    return category_menu

def repair_admin(db_all_categories):
    repair_menu= InlineKeyboardMarkup(row_width=2,resize_keyboard=True)
    category=db_all_categories
    for i in category:
        repair_menu.insert(InlineKeyboardButton(text=i[1],callback_data=f"recr{i[0]}"))
        repair_menu.insert(InlineKeyboardButton(text="🗑",callback_data=f"recd{i[0]}"))
    return repair_menu


def view_products_db(category_id):
    from data.add_box import read_category
    products_lst = read_category(category_id)
    if len(products_lst) == 1:
        prd = products_lst[0]
        product = prd[1]
        option = [prd[0], prd[3], prd[4]]
        box_inline_menu = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"clr{product}"),
                ]
            ]
        )
        return [[option, box_inline_menu]]
    else:
        options = []
        for pro in products_lst:
            lens = len(products_lst)
            index = products_lst.index(pro)
            product = pro[1]
            option = [pro[0], pro[3], pro[4]]
            box_inline_menus = 0
            if index == 0:
                box_inline_menus = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"clr{product}"),
                        ],
                        [
                            InlineKeyboardButton(text="➡ Keyingisi", callback_data=f"adn{product}"),
                        ]
                    ]
                )
            elif (index + 1) == lens:
                box_inline_menus = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"clr{product}"),
                        ],
                        [
                            InlineKeyboardButton(text="⬅ Oldingisi", callback_data=f"adb{product}"),
                        ]
                    ]
                )
            else:
                box_inline_menus = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"clr{product}"),
                        ],
                        [
                            InlineKeyboardButton(text="⬅ Oldingisi", callback_data=f"adb{product}"),
                            InlineKeyboardButton(text="➡ Keyingisi", callback_data=f"adn{product}"),
                        ]
                    ]
                )
            options.append([option, box_inline_menus])
        return options
