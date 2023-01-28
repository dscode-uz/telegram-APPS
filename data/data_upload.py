def update_product_data(photo_id,category,name,narx):
    from loader import db
    products=db.select_all_products()
    if len(products)==0:
        db.add_product(photo_id=photo_id,public_id=100,category=category,product_name=name,coin=narx)
    else:
        end_public_id=products[-1][1]
        new_public_id=end_public_id+1
        db.add_product(photo_id=photo_id, public_id=new_public_id,
                                category=category, product_name=name, coin=narx)