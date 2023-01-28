from aiogram.types import Message,CallbackQuery,ContentTypes
from keyboards.default.admin_p import panel_menu_amin
from data import data_upload
from states.adding_products_reg import new_products_registiration
from aiogram.dispatcher import FSMContext
from keyboards.default import mainmenu
from keyboards.inline import main_inline
from data.check_cancel import is_cancel,is_break
from loader import dp,db


@dp.message_handler(state=new_products_registiration.recent_category)
async def cancel_new_product(message:Message,state:FSMContext):
    canceling=is_break(message.text)
    if canceling:
        await message.answer("Bekor qilindi.",reply_markup=panel_menu_amin)
        await state.finish()


@dp.message_handler(text="➕ Mahsulot qo'shish")
async def bot_new_product(message: Message):
    is_category_yes= len(db.select_all_categories())!=0
    if is_category_yes:
        await message.answer("Mahsulotni qaysi bo'limga qo'shasiz?",reply_markup=mainmenu.break_menu)
        await message.answer("Sizdagi bo'limlar.",reply_markup=main_inline.create_menu_categories(db.select_all_categories()))
        await new_products_registiration.recent_category.set()
    else:
        await message.answer("Mahsulot qo'shishdan avval yangi mahsulotlar bo'limini yarating!")



@dp.callback_query_handler(state=new_products_registiration.recent_category)
async def product_category(call:CallbackQuery,state:FSMContext):
    await state.update_data(
        {
            "ctg":call.data,
        }
    )
    user_id=call.from_user.id
    await call.message.delete()
    await dp.bot.send_message(text="Endi menga ushbu mahsulotning rasmini yuboring.",chat_id=user_id)
    await new_products_registiration.next()
@dp.message_handler(state=new_products_registiration.recent_photo,content_types=ContentTypes.ANY)
async def product_photo(message:Message,state:FSMContext):
    canceling = is_break(message.text)
    if canceling:
        await message.answer("Bekor qilindi.", reply_markup=panel_menu_amin)
        await state.finish()
    else:
        try:
            photo_id=message.photo[-1].file_id
            await state.update_data(
                {
                "photo":photo_id,
                }
            )
            await message.answer("Yaxshi endi menga bu mahsulotning nomini yuboring.")
            await new_products_registiration.next()
        except:
            await message.answer("Men hozir sizdan faqat rasm qabul qilishim kerak...")
@dp.message_handler(state=new_products_registiration.recent_name)
async def product_name(message:Message,state:FSMContext):
    canceling = is_break(message.text)
    if canceling:
        await message.answer("Bekor qilindi.", reply_markup=panel_menu_amin)
        await state.finish()
    else:
        await message.answer("OK! Faqat endi menga ushbu mahsulotning narxini yuborsangiz bo'ldi.")
        await state.update_data(
            {
                "name":message.text
            }
        )
        await new_products_registiration.next()
@dp.message_handler(state=new_products_registiration.recent_coin)
async def product_coin(message:Message,state:FSMContext):
    canceling = is_break(message.text)
    if canceling:
        await message.answer("Bekor qilindi.", reply_markup=panel_menu_amin)
        await state.finish()
    else:
        try:
            narx=int(message.text)
            await state.update_data(
                {
                    "narx":narx
                }
            )
            data=await state.get_data()
            pro_category=str(data.get("ctg"))
            photo_file=str(data.get("photo"))
            nom=str(data.get("name"))
            narx=int(data.get("narx"))
            data_upload.update_product_data(photo_file,pro_category,nom,narx)
            cap=f"🔹{nom}\n💵Narxi: {narx}so'm"
            await message.answer_photo(photo=photo_file,caption=cap)
            await message.answer("✅ Mahsulotni muvaffaqiyatli qo'shdingiz.",reply_markup=mainmenu.start_menu_admin)
            await state.finish()
        except ValueError:
            await message.reply(f"Iltimos narxni to'gri kiriting.")

