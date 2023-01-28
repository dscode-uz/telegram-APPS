from aiogram.types import Message
from keyboards.default.admin_p import panel_menu_amin
from aiogram.dispatcher import FSMContext
from keyboards.default import mainmenu
from data.check_cancel import is_break
from loader import dp,db


@dp.message_handler(text="➕ Bo'lim qo'shish")
async def new_category(message:Message,state:FSMContext):
    await message.answer("Yaxshi menga yangi bo'limning nomini yuboring.",reply_markup=mainmenu.break_menu)
    await state.set_state("new_category")
@dp.message_handler(state="new_category")
async def category_name(message:Message,state:FSMContext):
    is_stop=is_break(message.text)
    if not is_stop:
        categories=db.select_all_categories()
        if len(categories)==0:
            db.add_category(id=1,name=str(message.text))
        else:
            end_category_id=categories[-1][0]
            new_category_id=end_category_id+1
            db.add_category(id=new_category_id, name=str(message.text))
        await message.answer(f"✅ {message.text} mahsulot kategoriyasi muvaffaqiyatli qo'shildi.",reply_markup=panel_menu_amin)
        await state.finish()
    else:
        await message.answer("Bekor qilindi.",reply_markup=panel_menu_amin)
        await state.finish()