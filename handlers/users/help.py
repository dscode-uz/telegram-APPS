from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from data.config import ADMINS
from data import config
from loader import dp


@dp.message_handler(CommandHelp(),user_id=ADMINS)
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/all - Bazani ko'rish",
            "/clear_db - Odamlar saqlanadigan bazani tozalash",
            "/clear_sv - Odamlarning savatalarini tozalash"
            "/clear_pr - Mahsulotlar saqlanadigan bazani tozalash",
            "/clear_ct - Kategoriyalar saqlanadigan bazani tozalash",
            "/clear - Barcha ma'lumotlar bazasini tozalash tozalash"
            )
    await message.answer("\n".join(text))

@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = await message.answer("Bizning kafemiz manzili 👇")
    lat=config.Shops["lat"]
    lon=config.Shops["lon"]
    await message.answer_location(latitude=lat,longitude=lon)
    await message.answer("Bot yaratuvchisi: @pycyberuz +998883832907")