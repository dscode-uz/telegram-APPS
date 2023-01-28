def read_category(category_id):
    from loader import db
    category_lst = db.select_all_categories()
    for product in category_lst:
        ctg = int(product[0])
        if ctg == category_id:
            return True
    return False

