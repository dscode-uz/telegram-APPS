from aiogram import executor

from loader import dp,db
from data.config import ADMINS
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    try:
        db.create_table_users()
        db.create_table_categories()
        db.create_table_products()
        i=1
        for admin_id in ADMINS:
            name=f"Admin {i}"
            db.add_user(id=int(admin_id),name=name)
            i+=1
    except:
        pass


    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
