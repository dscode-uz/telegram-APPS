from sqlite import Database
from products import Database2


def test_product():
    db = Database2(path_to_db='test.db')
    #db.create_table_products()
    db.add_product("sdfd",100, 1,"salat", 50)
    db.add_product("sdfr",101,0,"lawash",70)
    users = db.select_all_products()
    print(f"Barcha fodyalanuvchilar: {users}")

    user = db.select_product(category=0)
    db.delete_product(photo_id="sdfd")
    db.delete_product(photo_id="sdfr")
    print(f"Bitta foydalanuvchini ko'rish: {user}")
    print(db.select_all_products())


def test_user():
    from data.add_box import re_box,read_box,add_box
    db = Database(path_to_db='test01.db')
    db.create_table_users()


test_user()