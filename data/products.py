from aiogram import types
from aiogram.types import LabeledPrice

from utils.misc.product_payments import Product


def payment_ship_yes(name,amounts,ship):
    amounts*=100
    ship*=100
    product= Product(
        title="Kafega online to'lov",
        description=name,
        currency="UZS",
        prices=[
            LabeledPrice(
                label="Mahsulotlarning umumiy narxi",
                amount=amounts,
            ),
            LabeledPrice(
                label="Yetkazib berish masofasi bilan",
                amount=ship,
            ),
        ],
        start_parameter="create_invoice_products",
        need_name=True,
        need_phone_number=True,
    )
    return product





