from utils.misc.get_distance import calc_coin
from states.client_reg import new_shipping
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.inline.typeproduct import view_location
from keyboards.default import mainmenu
from keyboards.inline.typeproduct import notf_user
from data.add_box import add_box,re_box,read_box,read_coin
from data.products import *
from keyboards.inline import main_inline
from aiogram.types import Message,ContentTypes,ReplyKeyboardRemove,CallbackQuery
from loader import dp,db

@dp.callback_query_handler(text_contains="shop")
async def box_shop(call:CallbackQuery,state:FSMContext):
    data=str(call.data)
    stat=int(data[4:])
    if stat==0:
        re_box(int(call.from_user.id))
        await call.answer("🗑 Savatingiz tozalab yuborildi",show_alert=True)
        await call.message.answer("Bo'limlardan birini tanlang.",reply_markup=main_inline.shop_menu(db.select_all_categories()))
        await call.message.delete()
    elif stat==1:
        await call.message.edit_text("OK! Mahsulotlarga hozir to'lov qilasizmi yoki buyurtma bajarilgandami?",reply_markup=main_inline.is_ship)
    else:
  
        await call.message.answer("Bo'limlardan birini tanlang.",
                                        reply_markup=main_inline.shop_menu(db.select_all_categories()))
        await call.message.delete()
@dp.callback_query_handler(text_contains="ship")
async def box_ship(call:CallbackQuery,state:FSMContext):
    data = str(call.data)
    stat = int(data[4:])
    if stat == 0:
        await call.message.answer("Unday bo'lsa bizga ma'lumotlaringizni taqdim eting. Ism va familiyangiz kiritng",reply_markup=mainmenu.cancel_menu)
        await call.message.delete()
        await new_shipping.fio.set()
    elif stat == 1:
        await call.message.answer("Menga yetkazib berish kerak bo'lgan manzilni yuboring.",reply_markup=mainmenu.location)
        await call.message.delete()
        await state.set_state("location")


@dp.message_handler(state=new_shipping.fio)
async def shp1(message:Message,state:FSMContext):
    if message.text == "🔙 Ortga":
        await message.answer("Bosh menu", reply_markup=mainmenu.start_menu)
        await state.finish()
    else:
        await state.update_data(
            {
                "name_cl":message.text
            }
        )
        await message.answer("Iltimos mobil internet va joylashuv xizmatlari yoqilganiga ishonch hosil"
                             " qilib haqiqiy joylashuv o'rningizni yuboring",reply_markup=mainmenu.location)
        await new_shipping.next()
@dp.message_handler(state=new_shipping.location,content_types=ContentTypes.ANY)
async def shp2(message:Message,state:FSMContext):
    try:
        location=message.location
        latitude=location.latitude
        longitude=location.longitude
        ad_coin=calc_coin(latitude,longitude)
        await message.answer("Endi esa telefon raqamingizni yuboring.",reply_markup=mainmenu.phone_num)
        await state.update_data(
            {
                "lat":latitude,
                "lon":longitude,
                "adcoins":ad_coin[1],
                "dist":ad_coin[0]
            }
        )
        await new_shipping.next()
    except:
        try:
            if message.text == "🔙 Ortga":
                await message.answer("Bosh menu", reply_markup=mainmenu.start_menu)
                await state.finish()
        except:
            await message.answer("Joylashuv yuboring yoki orqaga chiqing.")
@dp.message_handler(state=new_shipping.phone_number,content_types=ContentTypes.ANY)
async def shp3(message:Message,state:FSMContext):
    try:
        call_phone=message.contact.phone_number
        await state.update_data(
            {
                "phone":call_phone
            }
        )
        a=await message.answer("Qabul qilindi",reply_markup=ReplyKeyboardRemove())
        await a.delete()
        await message.answer("Sizning barcha ma'lumotlaringiz qabul qilindi. Buyurtma bermoqchimisiz?",reply_markup=notf_user)
        await new_shipping.next()
    except:
        try:
            if message.text == "🔙 Ortga":
                await message.answer("Bosh menu", reply_markup=mainmenu.start_menu)
                await state.finish()
        except:
            await message.answer("Kontakt yuboring yoki orqaga chiqing.")

@dp.callback_query_handler(state=new_shipping.end_ship,text_contains="shipping")
async def ship_wh(call:CallbackQuery,state:FSMContext):
    hw=str(call.data)
    hw=int(hw[-1])
    if hw==0:
        await call.message.answer("Buyurtma qoldirildi.",reply_markup=mainmenu.start_menu)
        await call.message.delete()
    elif hw==1:
        data=await state.get_data()
        product_names=str(data.get("products"))
        orginal_coin=read_coin(call.from_user.id)[1]
        description=read_coin(call.from_user.id)[0]
        client_info=str(data.get("name_cl"))
        location_lat=float(data.get("lat"))
        location_lon = float(data.get("lon"))
        added_coin=int(data.get("adcoins"))
        distance=float(data.get("dist"))
        phone_number=str(data.get("phone"))
        await call.message.answer_location(latitude=location_lat,longitude=location_lon)
        await call.message.answer(f"Buyurtma qilmoqchi bo'lgan narsalaringiz.\n"
                         f"{description}\n"
                         f"Haqiqiy narx: {orginal_coin} so'm.\n"
                         f"Sizning manzilingiz {distance} km uchun yana {added_coin} so'm.\n"
                         f"Jami {orginal_coin+added_coin} so'm. Tez orada adminlarimiz siz bilan bog'lanishadi.",reply_markup=mainmenu.start_menu)
        await dp.bot.send_message(chat_id=ADMINS[0],text=f"Buyurtma keldi.\n"
                                                         f"Puli buyurtma bajarilganda olinadi.\n"
                         f"{product_names}\n"
                         f"Haqiqiy narxi: {orginal_coin} so'm.\n"
                         f"{distance} km yo'l uchun yana {added_coin} so'm.\n"
                         f"Jami {orginal_coin+added_coin} so'm.\n"
                              f"Buyurtmachi {client_info}\n"
                              f"Telefon raqami +{phone_number}",reply_markup=view_location(str(location_lat),str(location_lon)))
        re_box(call.message.from_user.id)
    await state.finish()
@dp.callback_query_handler(user_id=ADMINS)
async def sndlc(call:CallbackQuery):
    location=str(call.data)
    bre=location.index("_")
    lat=location[:bre]
    lon=location[bre+1:]
    await call.message.reply_location(latitude=float(lat),longitude=float(lon))