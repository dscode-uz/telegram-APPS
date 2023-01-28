import math
from aiogram import types

from data.cafe import Shops

def calc_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi_1) * math.cos(phi_2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    return meters / 1000.0  # output distance in kilometers

def calc_coin(lat2, lon2):
    lat1=Shops["lat"]
    lon1=Shops["lon"]
    k_meter=calc_distance(lat1, lon1, lat2, lon2)
    km1=Shops["1km"]
    d_coin=((k_meter*km1)//1000)*1000+1000
    return [k_meter,d_coin]
