from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def view_products_db(category_id):
    from data.add_box import read_category
    products_lst=read_category(category_id)
    if len(products_lst)==1:
        prd=products_lst[0]
        product=prd[1]
        option=[prd[0],prd[3],prd[4]]
        box_inline_menu = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🛒 Savatchaga qo'shish 📦",callback_data=f"add{product}"),
                ],
                [
                    InlineKeyboardButton(text="🔙 Ortga", callback_data="shop3"),
                ],
            ]
        )
        return [[option,box_inline_menu]]
    else:
        options = []
        for pro in products_lst:
            lens=len(products_lst)
            index=products_lst.index(pro)
            product=pro[1]
            option = [pro[0], pro[3], pro[4]]
            box_inline_menus=0
            if index==0:
                box_inline_menus = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="🛒 Savatchaga qo'shish 📦", callback_data=f"add{product}"),
                        ],
                        [
                            InlineKeyboardButton(text="➡ Keyingisi",callback_data=f"nxt{product}"),
                        ],
                        [
                            InlineKeyboardButton(text="🔙 Ortga", callback_data="shop3"),
                        ],
                    ]
                )
            elif (index+1)==lens:
                box_inline_menus = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="🛒 Savatchaga qo'shish 📦", callback_data=f"add{product}"),
                        ],
                        [
                            InlineKeyboardButton(text="⬅ Oldingisi",callback_data=f"bck{product}"),
                        ],
                        [
                            InlineKeyboardButton(text="🔙 Ortga", callback_data="shop3"),
                        ],
                    ]
                )
            else:
                box_inline_menus = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="🛒 Savatchaga qo'shish 📦", callback_data=f"add{product}"),
                        ],
                        [
                            InlineKeyboardButton(text="⬅ Oldingisi", callback_data=f"bck{product}"),
                            InlineKeyboardButton(text="➡ Keyingisi", callback_data=f"nxt{product}"),
                        ],
                        [
                            InlineKeyboardButton(text="🔙 Ortga", callback_data="shop3"),
                        ],
                    ]
                )
            options.append([option,box_inline_menus])
        return options



def view_location(lat,lon):
    view_gps=InlineKeyboardMarkup(row_width=1)
    view_gps.insert(InlineKeyboardButton(text="📍Manzilni ko'rish",callback_data=f"{lat}_{lon}"))
    return view_gps


def ntfid(user_id):
    user_id=user_id
    notf_user = InlineKeyboardMarkup(row_width=2)
    notf_user.insert(InlineKeyboardButton(text="✅ Ha", callback_data=f"id={user_id}1"))
    notf_user.insert(InlineKeyboardButton(text="❌ Yo'q", callback_data=f"id={user_id}0"))
    return notf_user

notf_user=InlineKeyboardMarkup(row_width=2)
notf_user.insert(InlineKeyboardButton(text="✅ Ha",callback_data=f"shipping1"))
notf_user.insert(InlineKeyboardButton(text="❌ Yo'q",callback_data=f"shipping0"))