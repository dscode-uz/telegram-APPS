#Bu yerdagi izohlardan oldin sqlite.py ni tushunib chiqing

#Kerakli kutubxonalarni import qilamiz
import asyncio
from datetime import datetime,timedelta
import logging
from pyrogram import Client, filters
from sqlite import Database

#Ma'lumotlar bazasini yaratamiz
db = Database()
try:
    print("Create")
    db.create_table_contacts()
    db.create_table_passwords()
except:
    pass

#Foydalanuvchining kerakli ma'lumotlari. API ID va API HASH ni googledan qidirib ko'ring yoki
senior_user_id=12345678 #Profil egasi ID raqami
control_time=15 #Boshqaruv vaqtini belgilash (minutlarda)
api_id = 12345 #API ID
api_hash = 'qwertyuiop' #API HASH
phone_code="+998" #mamlakat kodi
phone_number="+998919191999" #Telefon raqam
app = Client("my_account", api_id, api_hash,phone_code=phone_code,phone_number=phone_number) #mijoz kontrolleri
logging.basicConfig(level=logging.INFO) #Bo'layotgan holatlar haqida


@app.on_message(filters=filters.private) #Shaxsiydan keluvchi xabarlarni olish
async def my_handler(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    text = message.text

    #Shaxsiyga yozgan foydalanuvchini bazaga qo'shish
    try:
        db.add_contact(id=user_id, username=user_name)
    except:
        pass

    #Buyruqni oddiy xabardan ajratish
    if "/" in message.text:

        #Buyruq yozgan foydalanuvchi boshqarish huquqini tekshirish
        user_check = False
        is_control = db.select_contact(id=user_id)[3]
        if is_control != None or user_id == senior_user_id: #Va profilning egasi doimo boshqara oladi
            user_check = True

        #Start ya'ni boshqarish komandasi /start,1-parol,2-parol shaklida yoziladi (orasida vergul bilan)
        if "/start" in text:
            try:
                passwords = list(text.split(",")) #parollarni ajratib olish
                pass1 = passwords[1] #1-parol
                pass2 = passwords[2] #2-parol

                # 1-parol parollar ichida takrorlanmas bo'lgani uchun u orqali ma'lumotlarni olish. Parol mavjud bo'lmasa None qaytaradi
                check_pass = db.select_password(pass1=pass1)

                #2-parolni tekshirish
                if check_pass != None and check_pass[1] == pass2:
                    now_control=db.select_contact(is_control=1) #Agar boshqa odam profilni boshqarayotgan bo'lsa uni chetlatish
                    if now_control!=None:
                        await app.send_message(chat_id=now_control[0],text="Siz muddatidan oldin chetlashtirildingiz")
                        db.all_control_break() #Hammani uzish
                        db.all_wirter_break() #Barcha profil orqali yozuvchilarni o'chirish

                    #Boshqaruvni ulash
                    db.add_controller(id=user_id)

                    #Muvaffaqiyatli ulanganlikni bildirish
                    msg = await app.send_message(chat_id=user_id, text="15 daqiqa muddatga muvaffaqiyatli ulanish")

                    #Ishlatilgan parolni o'chirib yuborish
                    db.delete_password(pass1=pass1)

                    #Foydalanuvchini avto uzishni rejalashtirsh
                    now_date = datetime.now() #Hozirgi vaqt
                    new_date = now_date + timedelta(minutes=control_time) #Uzish vaqti

                    # Profilga boshqaruvni uzish haqidagi xabarni rejalashtirib jo'natish
                    await app.send_message("me", f"/clear,{user_id}", schedule_date=new_date)

                    # 3 sekund kutib xabarlarni o'chirish
                    await asyncio.sleep(3)
                    await msg.delete()
                    await message.delete()
                else:
                    #Parol xato bo'lganda
                    msg = await app.send_message(chat_id=user_id, text="Hmm Chota yoqmayabsan")
                    await asyncio.sleep(3)
                    await msg.delete()
                    await message.delete()
            except:
                pass
        #View ya'ni telegramning bildirishnomasidagi oxirgi xabarni yuborish (odatda telegram ochish uchun kelgan kod jo'natiladi)
        elif "/view" in text and user_check:
            await message.delete() #Xabar parolni o'chirish
            try:
                passwords = list(text.split(",")) #parollarni ajratib olish
                pass1 = passwords[1]
                pass2 = passwords[2]

                #parolni tekshirish
                passes = db.select_password(pass1=pass1)
                if passes != None and passes[1] == pass2:
                    db.delete_password(pass1=pass1)

                    #Chat tarixidan so'ngi xabarni olish
                    async for texts in app.get_chat_history(chat_id=777000, limit=1):
                        await app.send_message(chat_id=user_id, text=texts.text)
                else:
                    #Parol xato bo'lganda
                    msg = await app.send_message(chat_id=user_id, text="Hozir uchasan!")
                    await asyncio.sleep(3)
                    await msg.delete()
                    await message.delete()
            except:
                pass

        #2ta akkount orasida shu mijoz orqali yozishma olib borish /connect,foydalanuvchi idisi yoki /connect,kontakt nomi
        elif "/connect" in text and user_check:
            await message.delete()
            try:
                writer_id = text.split(",")[-1] #Id raqam yoki kontakt nomini olish
                if str(writer_id).isnumeric(): #Bu id raqam bo'lganda
                    db.connect_write(user_id, int(writer_id))
                else:
                    contact_id = db.select_contact(contact_name=writer_id) #kontakt nomi bo'lsa uni tekshirish
                    if contact_id != None:
                        db.connect_write(user_id, int(contact_id[0])) #kontakt idisini olish
                        msg = await app.send_message(chat_id=user_id, text="Sizga xabarlashishni boshladingiz.")
                    else: #kontakt mavjud emas
                        msg = await app.send_message(chat_id=user_id, text="Noto'g'ri kontakt nomi")
                    await asyncio.sleep(3)
                    await msg.delete()
                    await message.delete()
            except: #Xato id raqami yoki foydalanuvchi ushbu mijozni bloklagan
                msg = await app.send_message(chat_id=user_id, text="ID raqam xato yoki ushbu odam meni bloklagan.")
                await asyncio.sleep(3)
                await msg.delete()
                await message.delete()

        #Kontakt qo'shish /add_c,foydalanuvchi idisi,kontakt nomi holda kiritiladi
        elif "/add_c" in text and user_check:
            user_info = text.split(",") #kontakt nomini va id raqamini ajratib olish
            user = db.select_contact(id=user_info[1]) #foydalanuvchi mijozga yozganmi yo'qmi tekshirish
            user_succes=True
            msg=message
            if user == None:
                user_contact=db.select_contact(contact_name=user_info) #shu nom bilan bo'lgan odam bormi yo'qmi tekshirish
                if user_contact==None:
                    db.add_contact(id=int(user_info[1]), username=user_info[-1], contact_name=user_info[-1])
                else:
                    msg=await message.reply("Bu nom bilan kontakt mavjud iltimos boshqa nom bilan yozing")
                    user_succes=False
            else:
                db.add_contact_name(contact_name=user_info[-1], id=int(user_info[1]))
            if user_succes:
                msg = await message.reply("Kontakt muvaffaqiyatli qo'shildi")
            await asyncio.sleep(3)
            await msg.delete()
            await message.delete()

        #Parol qo'shish /add_p,1-parol,2-parol. 2-parol berilmasa u "1234" bo'lib saqlandi
        elif "/add_p" in text:
            passwords = text.split(",") #parollarni ajratish

            #Parolni mijoz qo'shsa
            if user_id == senior_user_id:
                #2-parol berilganligini tekshirish
                if len(passwords) == 2:
                    db.add_password(passwords[1])
                    msg = await app.send_message(chat_id=user_id, text="Parol qo'shildi")
                    await asyncio.sleep(3)
                    await msg.delete()
                elif len(passwords) == 3:
                    db.add_password(passwords[1], passwords[2])
                    msg = await app.send_message(chat_id=user_id, text="Parol qo'shildi")
                    await asyncio.sleep(3)
                    await msg.delete()
                else:
                    msg = await app.send_message(chat_id=user_id, text="Xatolik")
                    await asyncio.sleep(3)
                    await msg.delete()

            #agar parolni favqulodda boshqa akkountdan qo'shsih kerak bo'lsa 2-parolni 0890 deb kiritish kerak
            elif passwords[-1] == "0890":
                # 2-parol berilganligini tekshirish
                if len(passwords) == 3:
                    db.add_password(passwords[1])
                    msg = await app.send_message(chat_id=user_id, text="Parol qo'shildi")
                    await asyncio.sleep(3)
                    await msg.delete()
                elif len(passwords) == 4:
                    db.add_password(passwords[1], passwords[2])
                    msg = await app.send_message(chat_id=user_id, text="Parol qo'shildi")
                    await asyncio.sleep(3)
                    await msg.delete()
                else:
                    msg = await app.send_message(chat_id=user_id, text="Xatolik")
                    await asyncio.sleep(3)
                    await msg.delete()
            await message.delete()

        #Bazani ko'rish
        elif text == "/select" and user_id == senior_user_id:
            passwords = db.select_all_passwords()
            try:
                m1 = await message.reply(passwords)
            except:
                m1 = await message.reply("Parollar bo'sh")
            users = db.select_all_contacts()
            m2 = await message.reply(users)
            await asyncio.sleep(5)
            await message.delete()
            await m1.delete()
            await m2.delete()

        #foydalanuvchini boshqaruvdan uzish start komandasiga qarang buni faqat dasturni o'zi jo'natadi
        elif "/clear" in text:
            ban_id=int(list(text.split(","))[1])
            state=db.select_contact(id=ban_id)[3]
            if state==1:
                db.control_break(ban_id)
                await app.send_message(ban_id,"Boshqaruv vaqtingiz tugadi.")

        #Hammani boshqaruvdan uzish
        elif text=="/clean" and user_id==senior_user_id:
            db.all_control_break()
            db.all_wirter_break()
            msg=await app.send_message(senior_user_id,"Hamma chetlatildi")
            await asyncio.sleep(3)
            await msg.delete()
            await message.delete()
    #/connect vaziyatida bo'lganlarni xabarlarini rostlash
    else:
        recivors = db.select_contact(is_control=1) #boshqarayotgan bormi yoq'mi tekshirish
        okey = recivors!=None
        if okey:
            recivor_user=recivors #recivor_user[0] hamda recivor_user[-1] da bog'langanlar bo'ladi
            if okey and recivor_user[0] == user_id: #1-odam xabar yozsa 2-odamga jo'natadi
                await app.copy_message(chat_id=recivor_user[-1],from_chat_id=recivor_user[0],message_id=message.id)
            elif okey and recivor_user[-1] == user_id: #2-odam xabar yozsa 1-odamga jo'natadi
                await app.copy_message(chat_id=recivor_user[0],from_chat_id=recivor_user[-1],message_id=message.id)
app.run()
