import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.mainmenu import start_menu,start_menu_admin
from data.config import ADMINS
from data import bot_sparvka
from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message:types.Message):
    name = message.from_user.full_name
    is_admin=False
    for admin in ADMINS:
        ids=message.from_user.id
        if str(ids)==str(admin):
            is_admin=True
            break
    if is_admin:
        await message.answer("Xush kelibsiz admin.", reply_markup=start_menu_admin)
        try:
            db.add_user(id=message.from_user.id,name=name)
        except:
            pass
    else:
        try:
            db.add_user(id=message.from_user.id,name=name)
            await message.answer(f"Assalomu alaykum. Xush kelibsiz! {name} siz bizning "
                                 f"Virtual Kafemiz botiga obuna bo'ldingiz. "
                                 f"Bizning menularimizdan bahramand bo'ling.\n\n"
                                 f"Ushbu bot @Cafe_uz_bot ni takomillashtirilgan versiyasi.",reply_markup=start_menu)
            await message.answer(bot_sparvka.qollanma)
        except sqlite3.IntegrityError:
            await message.answer(f"Yana bir bor salom {name}",reply_markup=start_menu)
