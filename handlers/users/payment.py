from utils.misc.get_distance import calc_coin
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.inline.typeproduct import view_location
from keyboards.default import mainmenu
from data.add_box import re_box,read_box
from data.products import *
from aiogram.types import Message,ContentTypes
from loader import dp,db

@dp.message_handler(state="location",content_types=ContentTypes.ANY)
async def get_dictance(message:Message,state:FSMContext):
    try:
        location = message.location
        latitude = location.latitude
        longitude = location.longitude
        ad_coin = calc_coin(latitude, longitude)
        products = read_box(int(message.from_user.id))
        amounts = 0
        caption = "Sizning olmoqchi bo'lgan mahsulotlaringiz\n"
        for option in products:
            name = option[0]
            coin = int(option[1])
            amount = int(option[3])
            caption += f"{name}\n{amount}*{coin}={amount * coin}\n"
            amounts += amount * coin
        ad_coins=int(ad_coin[1])
        caption+=f"{ad_coin[0]} km uchun yana {ad_coins} so'm."
        schet_invoice = payment_ship_yes(caption, amounts, ad_coins)
        await dp.bot.send_invoice(chat_id=message.from_user.id,
                                  **schet_invoice.generate_invoice(),
                                  payload="payload:schet")
        db.update_location(location=f"{latitude}_{longitude}",id=message.from_user.id)
        await state.finish()
    except:
        try:
            if message.text == "🔙 Ortga":
                await message.answer("Bosh menu", reply_markup=mainmenu.start_menu)
                await state.finish()
        except:
            await message.answer("Joylashuv yuboring yoki orqaga chiqing.")


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await dp.bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    await dp.bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Xaridingiz uchun rahmat! Adminstratorlarimiz sizga tez orada aloqaga chiqishadi. Kelishganda to'lov chekini ko'rsatasiz."
                              ,reply_markup=mainmenu.start_menu)
    # re_box(pre_checkout_query.from_user.id)

@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def succesfully_pyment(message:Message):
    cliet_name=message.successful_payment.order_info.name
    phone_number=message.successful_payment.order_info.phone_number
    products = read_box(int(message.from_user.id))
    amounts = 0
    caption = ""
    for option in products:
        name = option[0]
        coin = int(option[1])
        amount = int(option[3])
        caption += f"{name}\n{amount}*{coin}={amount * coin}\n"
        amounts += amount * coin

    location = db.select_user(id=message.from_user.id)[3]
    bre = location.index("_")
    lat = location[:bre]
    lon = location[bre + 1:]


    distance=calc_coin(float(lat),float(lon))



    txt=f"Buyurtma keldi.\n\n{caption}\n" \
        f"Puli to'langan.\n" \
        f"Haqiqiy narxi: {amounts} so'm." \
        f"\n{distance[0]} km yo'l uchun yana {distance[1]} so'm.\n" \
        f"Jami {amounts+distance[1]} so'm.\n" \
        f"Buyurtmachi:\nTo'liq ismi {cliet_name}\n" \
        f"Telefon raqami +{phone_number}"
    for admin in ADMINS:
        await dp.bot.send_message(chat_id=admin,text=txt,reply_markup=view_location(str(lat),str(lon)))
    re_box(message.from_user.id)