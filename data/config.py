from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
PROVIDER_TOKEN=env.str("PROVIDER_TOKEN")
MAP=env.list("MAP")
DELIVERY=env.int("DELIVERY_TO_KM")
IP = env.str("ip")

Shops={"lat":float(MAP[0]),
       "lon":float(MAP[1]),
       "1km":int(DELIVERY)
       }
