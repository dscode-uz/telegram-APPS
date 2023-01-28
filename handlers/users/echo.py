from aiogram import types
from keyboards.default import mainmenu,admin_p
from data.config import ADMINS
from loader import dp


@dp.message_handler(text="🔝 Bosh menu")
async def bot_echo(message:types.Message):
    await message.answer("Bosh admin menu",reply_markup=mainmenu.start_menu_admin)

@dp.message_handler(text="🔙 Ortga")
async def bot_cancel(message: types.Message):
    await message.answer("Bosh menu.",reply_markup=mainmenu.start_menu)

@dp.message_handler(text="👤 Foydalanuvchi sifatida kirish")
async def bot_cuser(message: types.Message):
    await message.answer("Bosh menu.",reply_markup=mainmenu.start_menu)

@dp.message_handler(text="💻 Admin panelga o'tish",user_id=ADMINS)
async def bot_admin(message: types.Message):
    await message.answer("Admin menu.",reply_markup=admin_p.panel_menu_amin)

@dp.message_handler()
async def echo_bot(message:types.Message):
    await message.reply("❌ Noto'g'ri xabar")