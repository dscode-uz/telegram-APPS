from loader import db
def read_box(user_id):
    a=db.select_user(id=user_id)
    a=a[2]
    try:
        n=list(a.split(","))
    except:
        return []
    options=[]
    for i in n:
        m=int(i)
        me=int(i[-1])
        prd=(m-me)//10
        amount=int(i[-1])
        opt = []
        product=db.select_product(public_id=prd)

        opt.append(product[3])
        opt.append(product[4])
        opt.append(product[2])
        opt.append(amount)
        opt.append(product[1])
        options.append(opt)
    return options


def add_box(public_id,amount,user_id):
    k=str(public_id)
    a=db.select_user(id=user_id)
    a=a[2]
    if a==None:
        db.to_adding_box(savat=f"{k}{amount}",id=user_id)
    elif a!=None:
        o=f"{a},{k}{amount}"
        db.to_adding_box(savat=str(o),id=user_id)

def re_box(user_id):
    db.to_adding_box(savat=None,id=user_id)

def re_add_box(delete_products_index,user_id):
    savat=read_box(user_id)
    savat.remove(savat[delete_products_index])
    new_savat=""
    for opt in savat:
        if len(new_savat)==0:
            new_savat += f"{opt[4]}{opt[3]}"
        else:
            new_savat+=f",{opt[4]}{opt[3]}"
    db.to_adding_box(savat=new_savat,id=user_id)


def read_coin(user_id):
    products = read_box(user_id)
    amounts = 0
    caption = ""
    for option in products:
        name = option[1]
        coin = int(option[2])
        amount = int(option[3])
        caption += f"☑ {name}\n{amount}*{coin}={amount * coin}\n"
        amounts += amount * coin
    return [caption,amounts]


def read_category(category_id):
    product_lst = db.select_all_products()
    response = []
    for product in product_lst:
        ctg = int(product[2])
        if ctg == category_id:
            response.append(product)
    return response






def get_category(public_id):
    get_info = db.select_product(public_id=public_id)[2]
    return get_info
def read_products_in_next(category_publc_id):
    get_info=db.select_product(public_id=category_publc_id)
    all_products=read_category(get_info[2])
    next_product=all_products.index(get_info)+1
    return next_product
def read_products_in_back(category_publc_id):
    get_info=db.select_product(public_id=category_publc_id)
    all_products=read_category(get_info[2])
    back_product=all_products.index(get_info)-1
    return back_product