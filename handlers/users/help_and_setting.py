from aiogram.types import Message
from data import config
from loader import dp

@dp.message_handler(text="📑 Yordam 🧾")
async def help(message:Message):
    await message.answer("Bizning kafemiz manzili 👇")
    lat=config.Shops["lat"]
    lon=config.Shops["lon"]
    await message.answer_location(latitude=lat,longitude=lon)
    await message.answer("Bot yaratuvchisi: @cpyjava +998883832907")
