from aiogram.types import Message
from data import cafe
from loader import dp

@dp.message_handler(text="📑 Yordam 🧾")
async def help(message:Message):
    await message.answer("Bizning kafemiz manzili 👇")
    lat=cafe.Shops["lat"]
    lon=cafe.Shops["lon"]
    await message.answer_location(latitude=lat,longitude=lon)
    await message.answer("Bot yaratuvchisi: @cpyjava +998883832907")
