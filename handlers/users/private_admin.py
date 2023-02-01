from aiogram.types import Message
from data.config import ADMINS
from data import add_box
from loader import dp,db

@dp.message_handler(text="/all",user_id=ADMINS)
async def view_database(message:Message):
    await message.answer(db.select_all_users())
    await message.answer(db.select_all_categories())
    await message.answer(db.select_all_products())

@dp.message_handler(text="/clear_db",user_id=ADMINS)
async def admin_command(message:Message):
    db.delete_users()
    await message.reply("OK")

@dp.message_handler(text="/clear_sv",user_id=ADMINS)
async def admin_command(message:Message):
    for i in db.select_all_users():
        user_id = i[0]
        add_box.re_box(user_id)
    await message.answer("OK")

@dp.message_handler(text="/clear_pr",user_id=ADMINS)
async def admin_command(message:Message):
    db.delete_products()
    await message.reply("OK")

@dp.message_handler(text="/clear_ct",user_id=ADMINS)
async def admin_command(message:Message):
    db.delete_categories()
    await message.reply("OK")

@dp.message_handler(text="/clear",user_id=ADMINS)
async def admin_command(message:Message):
    db.delete_users()
    db.delete_products()
    db.delete_categories()
    await message.reply("OK")


