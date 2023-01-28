from aiogram.types import Message,CallbackQuery
from keyboards.inline import main_inline,typeproduct
from aiogram.dispatcher import FSMContext
from data import add_box
from loader import dp,db


@dp.message_handler(text="🛒 Xarid qilish 🛍")
async def category(message:Message,state:FSMContext):
    await message.answer("Bo'limlardan birini tanlang.",reply_markup=main_inline.shop_menu(db.select_all_categories()))
@dp.callback_query_handler(text_contains="opt")
async def shopping_menu(call:CallbackQuery):
    datas=str(call.data[3:])
    if datas=="box":
        products_lst=db.select_user(id=int(call.from_user.id))[2]
        if products_lst==None:
            await call.answer("Sizning savatingiz bo'sh.\nEslatma! Savatga ko'pi bilan 10xil turdagi mahsulot qo'shish mumkin.",show_alert=True)
        else:
            products=add_box.read_box(int(call.from_user.id))
            amounts=0
            caption=""
            k=1
            for option in products:
                name=option[0]
                coin=int(option[1])
                amount=int(option[3])
                caption+=f"{k}. {name}\n{amount}*{coin}={amount*coin}\n\n"
                k+=1
                amounts+=amount*coin
            await call.message.answer(f"{caption}\n🛒 Sizning buyurtma savatingizdagi mahsulotlarning umumiy qiymati {amounts} so'm"
                                      ,reply_markup=main_inline.go_menu(call.from_user.id))
            await call.message.delete()
    else:
        category=int(datas)
        products_lst = add_box.read_category(category)
        if len(products_lst)==0:
            await call.answer("Kechirasiz ushbu bo'limda hali hech narsa yo'q edi.")
        else:
            msg=list(typeproduct.view_products_db(category))
            if len(msg)==1:
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