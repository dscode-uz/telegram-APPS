import asyncio
from random import choice
from aiogram.types import Message,CallbackQuery,ContentTypes
from keyboards.default.admin_p import panel_menu_amin
from data.config import ADMINS
from data import add_box
from aiogram.dispatcher import FSMContext
from keyboards.default import mainmenu
from keyboards.inline import typeproduct,admin_inline
from data.check_cancel import is_break
from loader import dp,db


@dp.message_handler(text="/all")
async def view_database(message:Message):
    await message.answer(db.select_all_users())
    await message.answer(db.select_all_categories())
    await message.answer(db.select_all_products())

@dp.message_handler(text="📊 Statistika")
async def admin_command(message:Message):
    users=db.select_all_users()
    categories=db.select_all_categories()
    products=db.select_all_products()
    await message.answer(f"📊 Statistika\n"
                         f"Jami foydalanuvchilar soni {len(users)} ta.\n\n"
                         f"Bo'limlar soni {len(categories)} ta.\n"
                         f"Mahsulotlar soni {len(products)} ta.\n")


@dp.message_handler(text="📮 Xabar tarqatish")
async def admin_command(message:Message,state:FSMContext):
    await message.answer("Xabar tarqitish uchun meng matn yuboring.",reply_markup=mainmenu.break_menu)
    await state.set_state("post")
@dp.message_handler(state="post")
async def post(message:Message,state:FSMContext):
    post=message.text
    is_stop=is_break(post)
    if is_stop:
        await message.answer("Bekor qilindi",reply_markup=panel_menu_amin)
        await state.finish()
    else:
        users=db.select_all_users()
        for user in users:
            try:
                await dp.bot.send_message(chat_id=user[0],text=post)
            except:
                db.delete_user(id=user[0])
            await asyncio.sleep(0.1)
            await state.finish()


@dp.message_handler(text="🎲 Tasodifiy foydalanuvchi")
async def rand(message:Message):
    rand = choice(db.select_all_users())
    randu = f"ID={rand[0]}\nNick={rand[1]}"
    await message.answer(f"Botga shu vaqtgacha /start bosgan foydalanuvchilar orasidan tasodifiy foydalanuvchi aniqlandi."
                         f"\nFoydalanuvchi:\n{randu}")
    user=int(rand[0])
    await message.answer(f"Ushbu foydalanuvchi ogohlantirilsinmi?",reply_markup=typeproduct.ntfid(user))
@dp.callback_query_handler(text_contains="id=")
async def notf_user(call:CallbackQuery):
    datas=str(call.data)
    chk=int(datas[-1])
    if chk==1:
        id = int(datas[3:-1])
        try:
            await dp.bot.send_message(chat_id=id,text="Assalomu alaykum siz bizning tasodifiy generatorimizdan aniqlandingiz."
                                                   "Iltimos adminga murojaat orqali biz bilan aloqaga chiqing.")
        except:
            await call.answer("Ushbu foydalanuvchi botni bloklagan!")
            db.delete_user(id=id)
        await call.answer("Ushbu foydalanuvchi ogohlantirildi")
    else:
        await call.message.answer("Ushbu foydalanuvchi ogohlantirilmadi.")
    await call.message.delete()

@dp.message_handler(text="🖊 Bazani boshqarish",user_id=ADMINS)
async def admin_command(message:Message):
    if len(db.select_all_categories())==0:
        await message.reply("Baza hali bo'm-bo'sh")
    else:
        await message.answer("Kerakli tugmalar orqali bazani nazorat qilishingiz mumkin",
                             reply_markup=admin_inline.repair_admin(db.select_all_categories()))

@dp.callback_query_handler(text_contains="rec")
async def shopping_menu(call:CallbackQuery):
    datas=str(call.data[3:])
    category=int(datas[1:])
    msg=list(admin_inline.view_products_db(category))
    is_delete=datas[0]
    if is_delete=="d":
        db.delete_category(category)
        for pr in db.select_all_products():
            if pr[2]==category:
                pr_photo=db.select_product(category=category)[0]
                db.delete_product(photo_id=pr_photo)
        await call.answer("Muvaffaqiyatli o'chirildi")
        await call.message.answer("Kerakli tugmalar orqali bazani nazorat qilishingiz mumkin",
                             reply_markup=admin_inline.repair_admin(db.select_all_categories()))
        for i in db.select_all_users():
            user_id = i[0]
            add_box.re_box(user_id)
        await call.message.answer("Barcha foydalanuvchilar savtlari o'chirildi.")
        await call.message.delete()
    else:
        if len(msg)==0:
            await call.answer("Bu yer bo'm bo'sh edi")
        elif len(msg)==1:
            msg=msg[0]
            photo=msg[0][0]
            name=msg[0][1]
            coin=msg[0][2]
            await call.message.answer_photo(photo=photo,caption=f"🔹{name}\n💵Narxi: {coin}so'm",reply_markup=msg[1])
            await call.message.delete()
        else:
            optionst=msg[0]
            photo = optionst[0][0]
            name = optionst[0][1]
            coin = optionst[0][2]
            await call.message.answer_photo(photo=photo, caption=f"🔹{name}\n💵Narxi: {coin}so'm", reply_markup=optionst[1])
            await call.message.delete()

@dp.callback_query_handler(text_contains="adn")
async def next_product(call:CallbackQuery):
    datas=call.data
    public_id=int(datas[3:])
    msg=admin_inline.view_products_db(add_box.get_category(public_id))
    product_index=add_box.read_products_in_next(public_id)
    optionst=msg[product_index]
    photo = optionst[0][0]
    name = optionst[0][1]
    coin = optionst[0][2]
    await call.message.answer_photo(photo=photo, caption=f"🔹{name}\n💵Narxi: {coin}so'm", reply_markup=optionst[1])
    await call.message.delete()

@dp.callback_query_handler(text_contains="adb")
async def back_product(call:CallbackQuery):
    datas=call.data
    public_id=int(datas[3:])
    msg=admin_inline.view_products_db(add_box.get_category(public_id))
    product_index=add_box.read_products_in_back(public_id)
    optionst=msg[product_index]
    photo = optionst[0][0]
    name = optionst[0][1]
    coin = optionst[0][2]
    await call.message.answer_photo(photo=photo, caption=f"🔹{name}\n💵Narxi: {coin}so'm", reply_markup=optionst[1])
    await call.message.delete()

@dp.callback_query_handler(text_contains="clr")
async def delete_product(call:CallbackQuery):
    datas=call.data
    dels=int(datas[3:])
    ind = db.select_product(public_id=dels)
    photo_id = db.select_all_products().index(ind)
    photo_id = db.select_all_products()[photo_id][0]
    db.delete_product(photo_id=photo_id)
    await call.answer("🗑 Muvaffaqiyatli o'chirildi")
    for i in db.select_all_users():
        user_id=i[0]
        add_box.re_box(user_id)
    await call.message.answer("Barcha foydalanuvchilar savtlari o'chirildi.")
    await call.message.answer("Kerakli tugmalar orqali bazani nazorat qilishingiz mumkin",
                              reply_markup=admin_inline.repair_admin(db.select_all_categories()))
    await call.message.delete()