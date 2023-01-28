import logging
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from keyboards import *
from config import *

#Telegramdan bot tokenini joylashtiramiz
API_TOKEN = 'Your Bot Token'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN,parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def bot_start(message: types.Message):
    await message.answer("Assalomu alaykum Film qidirish botiga xush kelibsiz!!"
                         " Kino topish uchun pastdagi tugmani bosib kino nomini yozing "
                         "va kerakli kinoni ustiga bosing.\nAgar botdan qanday foydalanishni bilmayotgan bo'lsangiz /help ni bosing",reply_markup=start_menu)
@dp.message_handler(commands=["help"])
async def echo(message: types.Message):
    url="https://telegra.ph/Kino-qidiruvchi-botdan-filmni-qidirish-01-06"
    await message.answer("To'liq qo'llanmani ushbu saytda ko'rishingiz mumkin",reply_markup=enter_web(url))

@dp.message_handler(commands=["t_help"])
async def echo(message: types.Message):
    text="Buning uchun video ostidagi yuklab olish tugmalarini bosib turing va url manzildan nusxa olib" \
         " https://t.me/urluploadxbot botiga yuboring shu yerdan siz keyin yuklab olishingiz mumkin"
    await message.answer(text)


@dp.inline_handler()
async def bot_search(query: types.InlineQuery):
    text=query.query
    response=search(query.query)
    i=1

    if len(text)==0:
        await query.answer(results=[types.InlineQueryResultArticle(
            id="full",title="Biror narsa qidiring!!",
            input_message_content=types.InputTextMessageContent("Biror narsa haqida qidiring!!"),
        )
        ])

    queries=[]
    for res in response[0]:
        if len(response[0]) == 0:
            break
        url=f"http://www.taronatv.com{res['href']}"
        photo_url=f"http://www.taronatv.com{response[1][i-1]['href']}"
        txt=f"{i}.{res.get_text()}"

        queries.append(types.InlineQueryResultArticle(
            id=str(i),
            title=txt,
            input_message_content=types.InputTextMessageContent(
                message_text=f"{txt}^{url}",
            ),
            thumb_url=photo_url,
            ))
        i+=1
    if len(response[0])!=0:
        await query.answer(queries)



@dp.message_handler()
async def search_movie(message:types.Message):
    via=message.via_bot
    if via!=None:
        await message.delete()
        text=list(message.text.split("^"))
        url=text[1]
        # print(url,text)
        response=result_search(url)
        msg = await dp.bot.send_message(chat_id=message.from_user.id,text="⏳ Iltimos biroz kuting...")
        if len(response[1])>0:
            txt = "⏳Diqqat havola yuborilmoqda"
            await msg.edit_text("⏳Kino yuklash manzili topldi...")
            await asyncio.sleep(2)
            await msg.edit_text("⏳Tayyorlanmoqda...")
            await asyncio.sleep(2)
            await msg.edit_text(txt)
            i=0
            k=6
            j=1
            while k!=0:
                i += j
                dot_nik = "." * i
                await msg.edit_text(f"{txt}{dot_nik}")
                await asyncio.sleep(0.1)
                if i==6:
                    j=-1
                    k-=1
                elif i==1:
                    j=1
                    k-=1
            photo=get_photo(url)
            await msg.delete()
            try:
                await dp.bot.send_photo(chat_id=message.from_user.id,photo=photo,
                                        caption=f"<b>{text[0]}</b>\n\n{response[0]}\n\n"
                                                f"Telegramning o'zidan yuklab olmoqchi bo'lsangiz qo'llanma uchun /t_help ni bosing.",
                                        reply_markup=download_video(response[1]))
            except:
                await dp.bot.send_photo(chat_id=message.from_user.id,
                                        photo=photo,
                                        caption="Bu yerda qismlar kop ekan yaxshisi saytda ko'ra qoling!",
                                          reply_markup=enter_web(url))
        else:
            await asyncio.sleep(2)
            await msg.edit_text("Ushbu film saytga hali toliq yuklanmagan! Noqulaylik uchun uzr!")
    else:
        await message.answer("Agar botdan foydalanishni bilmayotgan bo'lsangiz /help ni bosing.")








if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
