from aiogram.types import Message,MediaGroup,CallbackQuery
from keyboards.inline import main_inline
from keyboards.inline import typeproduct
from data import add_box,is_yes_category,check_cancel
from loader import dp,db

@dp.callback_query_handler(text_contains="add")
async def adding_box(call:CallbackQuery):
    box=add_box.read_box(call.from_user.id)
    if len(box)>9:
        await call.answer("Ehh! savatingiz to'lib qolibdi")
    else:
        data=str(call.data)
        id=str(data[3:])
        inline_keyboard=main_inline.adding_box(id)
        await call.message.edit_caption(caption="Bu mahsulotdan savatga nechta qo'shmoqchisiz?",reply_markup=inline_keyboard)
@dp.callback_query_handler(text_contains="amt")
async def add_amount_box(call:CallbackQuery):
    datas=call.data
    product_id=int(datas[3:-1])
    amount=int(datas[-1])
    user_id=int(call.from_user.id)
    add_box.add_box(product_id,amount,user_id)
    name=db.select_product(public_id=product_id)
    await call.answer(f"✅ {amount} ta {name[3]} muvaffaqiyatli savatga qo'shildi.",show_alert=True)
    await call.message.answer("Bo'limlardan birini tanlang.",reply_markup=main_inline.shop_menu(db.select_all_categories()))
    await call.message.delete()

@dp.callback_query_handler(text_contains="nxt")
async def next_product(call:CallbackQuery):
    datas=call.data
    public_id=int(datas[3:])
    msg=typeproduct.view_products_db(add_box.get_category(public_id))
    product_index=add_box.read_products_in_next(public_id)
    optionst=msg[product_index]
    photo = optionst[0][0]
    name = optionst[0][1]
    coin = optionst[0][2]
    await call.message.answer_photo(photo=photo, caption=f"🔹{name}\n💵Narxi: {coin}so'm", reply_markup=optionst[1])
    await call.message.delete()

@dp.callback_query_handler(text_contains="bck")
async def back_product(call:CallbackQuery):
    datas=call.data
    public_id=int(datas[3:])
    msg=typeproduct.view_products_db(add_box.get_category(public_id))
    product_index=add_box.read_products_in_back(public_id)
    optionst=msg[product_index]
    photo = optionst[0][0]
    name = optionst[0][1]
    coin = optionst[0][2]
    await call.message.answer_photo(photo=photo, caption=f"🔹{name}\n💵Narxi: {coin}so'm", reply_markup=optionst[1])
    await call.message.delete()

@dp.callback_query_handler(text_contains="del")
async def delete_product(call:CallbackQuery):
    datas=call.data
    dels=int(datas[-1])
    lens=len(add_box.read_box(call.from_user.id))
    if lens==1:
        add_box.re_add_box(dels-1, call.from_user.id)
        await call.answer("🗑 Muvaffaqiyatli o'chirildi")
        await call.message.answer("Bo'limlardan birini tanlang.",reply_markup=main_inline.shop_menu(db.select_all_categories()))
        add_box.re_box(call.from_user.id)
    else:
        add_box.re_add_box(dels-1,call.from_user.id)
        await call.answer("🗑 Muvaffaqiyatli o'chirildi")
        await call.message.answer("Bo'limlardan birini tanlang.",
                                        reply_markup=main_inline.shop_menu(db.select_all_categories()))
    await call.message.delete()