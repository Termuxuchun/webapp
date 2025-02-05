import json
from datetime import datetime, timedelta
from telebot import TeleBot, types

# Bot tokeningizni bu yerga yozing
BOT_TOKEN = "7317303145:AAFhzdI7lAgHvmmvS1l92vz-oLnlVH9Mk4A"
bot = TeleBot(BOT_TOKEN)

# Admin ID (statistika va xabar yuborish uchun)
ADMIN_ID = 8157810564


# Ma'lumotlar bazasini o'qish va saqlash
def read_db():
    try:
        with open("database.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def write_db(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent=4)


# /start komandasi
@bot.message_handler(commands=["start"])
def send_welcome(message):
    data = read_db()
    user_id = message.from_user.id
    user = data.get(str(user_id))

    if user:
        show_main_menu(message.chat.id)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                           resize_keyboard=True)
        button = types.KeyboardButton("📱 Telefon raqamni yuborish",
                                      request_contact=True)
        markup.add(button)
        bot.send_message(
            message.chat.id,
            "Assalomu alaykum! Ro‘yxatdan o‘tish uchun telefon raqamingizni yuboring:",
            reply_markup=markup,
        )


# Raqam yuborilganda
@bot.message_handler(content_types=["contact"])
def save_contact(message):
    if message.contact is not None:
        user_id = message.from_user.id
        username = message.from_user.username or "Noma'lum"
        phone_number = message.contact.phone_number

        data = read_db()
        if str(user_id) in data:
            bot.send_message(message.chat.id,
                             "Siz allaqachon ro‘yxatdan o‘tgan ekansiz.")
        else:
            data[str(user_id)] = {
                "username": username,
                "phone_number": phone_number,
                "balance": 0.0,
                "rating": 0,  # Add rating field
                "last_bonus": None  # Add last bonus claim timestamp
            }
            write_db(data)
            bot.send_message(message.chat.id,
                             "Raqamingiz muvaffaqiyatli saqlandi! ✅")
            show_main_menu(message.chat.id)


# **Admin ID**
ADMIN_ID = 8157810564  # Adminning Telegram ID sini kiriting


# **UC ma'lumotlarini o'qish**
def read_uc_servis_db():
    try:
        with open("uc_servis.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# **Foydalanuvchi ma'lumotlarini o'qish**
def read_db():
    try:
        with open("database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# **Foydalanuvchi ma'lumotlarini yozish**
def write_db(data):
    with open("database.json", "w") as file:
        json.dump(data, file, indent=4)


# Admin ID (Sizning Telegram ID'ingizni yozing)
ADMINS = [8157810564]

# Ma'lumotlar bazasi
DB_FILE = "database.json"


# JSON'dan foydalanuvchilarni o‘qish
def read_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# JSON'ga ma'lumot yozish
def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


API_URL = "https://api.exchangerate-api.com/v4/latest/Uzs"  # O'zbekistondan foydalanish uchun kerakli valyutani o'zgartiring


# Hizmatlar bo'limi
@bot.callback_query_handler(func=lambda call: call.data == "hizmatlar")
def xizmatlar_menu(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💵 UC Servis", callback_data="uc_servis"))
    markup.add(types.InlineKeyboardButton("🌤 Ob-Havo",
                                          callback_data="hizmat1"))
    markup.add(
        types.InlineKeyboardButton("🛒 Online Shop",
                                   callback_data="online_shop"))
    markup.add(
        types.InlineKeyboardButton("👑 Telegram Premium olish",
                                   callback_data="telegram_premium"))
    markup.add(
        types.InlineKeyboardButton("📚 Bepul onlayn darsliklar",
                                   callback_data="free_courses"))
    markup.add(
        types.InlineKeyboardButton("💻 Dasturlash va texnologiya kurslari",
                                   callback_data="programming_courses"))
    markup.add(
        types.InlineKeyboardButton("💸 Valyuta kurslari va konvertatsiya",
                                   callback_data="currency_converter"))
    markup.add(
        types.InlineKeyboardButton("📖 Tavsiya etilgan kitoblar",
                                   callback_data="recommended_books"))
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="show_main_menu"))

    bot.edit_message_text("🛠 *Hizmatlar bo‘limi:*",
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=markup,
                          parse_mode="Markdown")


# **UC Servis bo'limi menyusi**
@bot.callback_query_handler(func=lambda call: call.data == "uc_servis")
def uc_servis_menu(call):
    uc_data = read_uc_servis_db()

    if not uc_data:
        try:
            bot.edit_message_text("❌ Hozircha UC xizmatlari mavjud emas.",
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
        except Exception as e:
            print(f"Xatolik: {e}")  # Xatolikni konsolga chiqarish
        return

    # **Inline keyboard yaratish**
    markup = types.InlineKeyboardMarkup()
    for uc_id, uc_item in uc_data.items():
        markup.add(
            types.InlineKeyboardButton(
                f"💵 {uc_item['name']} - {uc_item['price']} so'm",
                callback_data=f"buy_uc_{uc_id}"))

    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="hizmatlar"))

    try:
        bot.edit_message_text("💵 UC xizmatlari ro'yxati:",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        print(f"Xatolik: {e}")


# **UC sotib olish callback handler**
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_uc_"))
def confirm_uc_purchase(call):
    uc_id = call.data.split("_")[2]
    uc_data = read_uc_servis_db()
    user_data = read_db()
    user_id = str(call.message.chat.id)

    if uc_id not in uc_data:
        bot.send_message(call.message.chat.id, "❌ Ushbu UC xizmat topilmadi.")
        return

    uc_item = uc_data[uc_id]
    user_balance = user_data.get(user_id, {}).get("balance", 0)

    if user_balance < uc_item['price']:
        try:
            bot.edit_message_text(
                f"❌ Balansingiz yetarli emas! Balans: {user_balance} so'm, UC narxi: {uc_item['price']} so'm.",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id)
        except Exception as e:
            print(f"Xatolik: {e}")
        return

    # **Tasdiqlash va rad etish uchun tugmalar**
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Tasdiqlash",
                                   callback_data=f"confirm_{uc_id}"))
    markup.add(
        types.InlineKeyboardButton("❌ Rad etish", callback_data="uc_servis"))

    try:
        bot.edit_message_text(
            f"💵 Siz {uc_item['name']} xizmatini {uc_item['price']} so'mga sotib olmoqchisiz. Tasdiqlaysizmi?",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup)
    except Exception as e:
        print(f"Xatolik: {e}")


# **Tasdiqlash tugmasi callback handler**
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def ask_game_id(call):
    uc_id = call.data.split("_")[1]
    uc_data = read_uc_servis_db()

    if uc_id not in uc_data:
        bot.send_message(call.message.chat.id, "❌ Ushbu UC xizmat topilmadi.")
        return

    bot.send_message(call.message.chat.id,
                     "🆔 O'yindagi foydalanuvchi IDingizni kiriting:")

    # **Foydalanuvchi ID ni qabul qilish**
    bot.register_next_step_handler(call.message, handle_game_id, uc_id)


def handle_game_id(message, uc_id):
    game_id = message.text
    user_data = read_db()
    user_id = str(message.chat.id)
    uc_data = read_uc_servis_db()

    if uc_id not in uc_data:
        bot.send_message(message.chat.id, "❌ UC xizmat topilmadi.")
        return

    # **Foydalanuvchi balansini yangilash**
    if user_id in user_data:
        user_data[user_id]["balance"] -= uc_data[uc_id]["price"]
        write_db(user_data)

    # **Admin uchun xabar yuborish**
    bot.send_message(
        ADMIN_ID, f"🆕 *Yangi UC buyurtma kelib tushdi!*\n\n"
        f"💵 *UC:* {uc_data[uc_id]['name']} - {uc_data[uc_id]['price']} so‘m\n"
        f"🆔 *O'yin ID:* {game_id}\n"
        f"👤 *Foydalanuvchi:* @{message.chat.username if message.chat.username else 'Ismi yo‘q'} ({message.chat.id})",
        parse_mode="Markdown")

    bot.send_message(
        message.chat.id,
        "✅ *Buyurtma qabul qilindi!* Tez orada UC hisobingizga tushadi.",
        parse_mode="Markdown")


# **Premium olish menyusi**
@bot.callback_query_handler(func=lambda call: call.data == "telegram_premium")
def telegram_premium(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📅 1 Oylik - 60,000 so‘m",
                                   callback_data="buy_premium_1month"))
    markup.add(
        types.InlineKeyboardButton("📅 3 Oylik - 150,000 so‘m",
                                   callback_data="buy_premium_3months"))
    markup.add(
        types.InlineKeyboardButton("📆 1 Yillik - 650,000 so‘m",
                                   callback_data="buy_premium_1year"))
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="hizmatlar"))

    bot.edit_message_text(
        "👑 *Telegram Premium olish:* \n\n"
        "🔹 Reklamalarsiz Telegram\n"
        "🔹 Eksklyuziv stiker va emojilar\n"
        "🔹 Qo‘shimcha funksiyalar\n\n"
        "💰 *Narxlar:* \n"
        "📅 1 oylik - 60,000 so‘m\n"
        "📅 3 oylik - 150,000 so‘m\n"
        "📆 1 yillik - 650,000 so‘m\n\n"
        "✅ Istalgan variantni tanlang:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown")


# **To‘lov uchun bank rekvizitlarini ko‘rsatish**
@bot.callback_query_handler(
    func=lambda call: call.data.startswith("buy_premium_"))
def show_payment_info(call):
    user_id = str(call.message.chat.id)
    package = "1 oylik" if call.data == "buy_premium_1month" else "3 oylik" if call.data == "buy_premium_3months" else "1 yillik"
    price = "60,000 so‘m" if call.data == "buy_premium_1month" else "150,000 so‘m" if call.data == "buy_premium_3months" else "650,000 so‘m"

    # Ma'lumotlarni bazaga saqlash
    data = read_db()
    data[user_id] = {
        "package": package,
        "price": price,
        "waiting_for_confirmation": False  # Admin hali ko‘rib chiqmagan
    }
    write_db(data)

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📤 Chekni yuborish",
                                   callback_data="send_receipt"))
    markup.add(
        types.InlineKeyboardButton("❌ Bekor qilish",
                                   callback_data="telegram_premium"))

    bot.send_message(call.message.chat.id, f"💳 *To‘lov ma'lumotlari:* \n"
                     f"📦 *Tanlangan paket:* {package}\n"
                     f"💰 *Narxi:* {price}\n\n"
                     "📌 *To‘lov kartasi:* 9860 1701 1535 8567 (Humo/UzCard)\n"
                     "📌 *Izoh:* Telegram Premium sotib olish\n\n"
                     "✅ *To‘lovni amalga oshiring va chekingizni yuboring!*",
                     reply_markup=markup,
                     parse_mode="Markdown")


# **Foydalanuvchi cheki yuboradi**
@bot.callback_query_handler(func=lambda call: call.data == "send_receipt")
def ask_for_receipt(call):
    msg = bot.send_message(
        call.message.chat.id,
        "📤 *Iltimos, to‘lov chekini rasm sifatida yuboring:*",
        parse_mode="Markdown")
    bot.register_next_step_handler(msg, receive_receipt)


def receive_receipt(message):
    if message.content_type == "photo":
        user_id = str(message.chat.id)
        data = read_db()

        if user_id in data:
            user = data[user_id]
            user["receipt_photo"] = message.photo[-1].file_id
            user["waiting_for_confirmation"] = True
            write_db(data)

            # **Adminga xabar yuborish**
            for admin_id in ADMINS:
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton(
                        "✅ Tasdiqlash", callback_data=f"confirm_{user_id}"))
                markup.add(
                    types.InlineKeyboardButton(
                        "❌ Rad etish", callback_data=f"reject_{user_id}"))

                bot.send_photo(
                    chat_id=admin_id,
                    photo=message.photo[-1].file_id,
                    caption=f"📥 *Yangi to‘lov cheki kelib tushdi!*\n\n"
                    f"👤 *User ID:* {user_id}\n"
                    f"📱 *Tanlangan paket:* {user['package']}\n"
                    f"💰 *Narxi:* {user['price']}\n\n"
                    "✅ Tasdiqlash yoki ❌ Rad etish tugmalarini bosing:",
                    reply_markup=markup,
                    parse_mode="Markdown")

            bot.send_message(
                message.chat.id,
                "✅ *Chek qabul qilindi! To‘lovingizni tekshirib chiqamiz.*")
        else:
            bot.send_message(message.chat.id, "❌ *Foydalanuvchi topilmadi!*")
    else:
        bot.send_message(
            message.chat.id,
            "❌ *Iltimos, to‘lov chekini rasm sifatida yuboring!*")


# **Admin to‘lovni tasdiqlashi yoki rad etishi**
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_")
                            or call.data.startswith("reject_"))
def confirm_or_reject_payment(call):
    user_id = call.data.split("_")[1]
    data = read_db()

    if user_id in data and data[user_id].get("waiting_for_confirmation",
                                             False):
        if call.data.startswith("confirm_"):
            data[user_id]["waiting_for_confirmation"] = False
            data[user_id]["premium"] = True
            data[user_id]["premium_expiry"] = (datetime.now() +
                                               timedelta(days=30)).isoformat()
            write_db(data)

            bot.send_message(
                user_id,
                "✅ *Tabriklaymiz! Siz 20 daqiqada Telegram Premium olasiz!* 🎉",
                parse_mode="Markdown")
            bot.answer_callback_query(call.id, "✅ To‘lov tasdiqlandi!")
        else:
            data[user_id]["waiting_for_confirmation"] = False
            write_db(data)

            bot.send_message(
                user_id,
                "❌ *Chek tekshirildi va rad etildi!* \n\n📌 *Sabab:* Chekdagi ma'lumotlar noto‘g‘ri.",
                parse_mode="Markdown")
            bot.answer_callback_query(call.id, "❌ To‘lov rad etildi!")
    else:
        bot.answer_callback_query(
            call.id,
            "❌ Bu foydalanuvchining to‘lovi allaqachon ko‘rib chiqilgan!")


SHOP_DB_FILE = "shop_db.json"
USER_DB_FILE = "database.json"


# Mahsulotlar ro'yxatini yaratish yoki o'qish funksiyasi
def read_shop_db():
    try:
        with open(SHOP_DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def write_shop_db(data):
    with open(SHOP_DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Foydalanuvchi ma'lumotlar bazasini o'qish yoki yaratish
def read_db():
    try:
        with open(USER_DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def write_db(data):
    with open(USER_DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Dukon menyusi
@bot.callback_query_handler(func=lambda call: call.data == "online_shop")
def online_shop(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🛒 Dukon", callback_data="shop"))
    markup.add(
        types.InlineKeyboardButton("📦 Mahsulotlarim",
                                   callback_data="my_products"))
    markup.add(
        types.InlineKeyboardButton("✅ Belgilangan Mahsulotlar",
                                   callback_data="selected_products"))
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="hizmatlar"))

    bot.edit_message_text(
        "📦 Siz 'Online Dukon'ga kirdingiz. Quyidagi bo'limlardan birini tanlang:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


# Dukon ro'yxati
@bot.callback_query_handler(func=lambda call: call.data == "shop")
def shop_menu(call):
    shop_data = read_shop_db()
    markup = types.InlineKeyboardMarkup()

    for product_id, product in shop_data.items():
        markup.add(
            types.InlineKeyboardButton(
                f"{product['name']} - {product['price']} so'm",
                callback_data=f"choose_{product_id}"))

    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="hizmatlar"))

    bot.edit_message_text(
        "🛍 Mahsulotlar ro'yxati:\nQuyidagi mahsulotlardan birini tanlang:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


# Mahsulotni tanlash (Sotib olish / Belgilash tugmasi)
@bot.callback_query_handler(func=lambda call: call.data.startswith("choose_"))
def choose_product(call):
    product_id = call.data.split("_")[1]
    shop_data = read_shop_db()
    product = shop_data.get(product_id)

    if not product:
        bot.send_message(call.message.chat.id, "❌ Bu mahsulot mavjud emas!")
        return

    # Mahsulot ma'lumotlarini ko'rsatish
    message = f"📦 Mahsulot: {product['name']}\n"
    message += f"💰 Narxi: {product['price']} so'm\n"
    message += f"📏 O'lcham: {product.get('size', 'Malumot yoq')}\n"
    message += f"🌟 Reyting: {product.get('rating', 'Malumot yoq')}\n"
    message += f"🛠 Ishlab chiqaruvchi: {product.get('manufacturer', 'Malumot yoq')}\n"

    # Mahsulot ma'lumotlarini foydalanuvchiga yuborish
    bot.send_message(call.message.chat.id, message)

    # Sotib olish va belgilash tugmalarini ko'rsatish
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(f"💸 Sotib olish",
                                   callback_data=f"buy_{product_id}"))
    markup.add(
        types.InlineKeyboardButton(f"✅ Belgilash",
                                   callback_data=f"select_{product_id}"))
    markup.add(types.InlineKeyboardButton("🔙 Orqaga", callback_data="shop"))

    bot.edit_message_text(
        f"Siz {product['name']} mahsulotini tanladingiz. Iltimos, quyidagi variantlardan birini tanlang:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


# Sotib olish
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_product(call):
    product_id = call.data.split("_")[1]
    user_id = str(call.message.chat.id)

    shop_data = read_shop_db()
    user_data = read_db()

    if product_id not in shop_data:
        bot.send_message(call.message.chat.id, "❌ Bu mahsulot mavjud emas!")
        return

    product = shop_data[product_id]
    user_balance = user_data.get(user_id, {}).get("balance", 0)

    if user_balance < product["price"]:
        bot.send_message(
            call.message.chat.id,
            f"❌ Sizning balansingiz yetarli emas! Balans: {user_balance} so'm, mahsulot narxi: {product['price']} so'm."
        )
        return

    # Balansni kamaytirish va mahsulotni foydalanuvchiga qo'shish
    user_data[user_id]["balance"] -= product["price"]
    user_data[user_id].setdefault("products", []).append(product)

    write_db(user_data)

    bot.send_message(
        call.message.chat.id,
        f"✅ Siz {product['name']} mahsulotini {product['price']} so'mga sotib oldingiz!"
    )


# Mahsulotni belgilash
@bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
def select_product(call):
    product_id = call.data.split("_")[1]
    user_id = str(call.message.chat.id)

    shop_data = read_shop_db()
    user_data = read_db()

    if product_id not in shop_data:
        bot.send_message(call.message.chat.id, "❌ Bu mahsulot mavjud emas!")
        return

    product = shop_data[product_id]
    user_data[user_id].setdefault("selected_products", []).append(product)

    write_db(user_data)

    bot.send_message(call.message.chat.id,
                     f"✅ Siz {product['name']} mahsulotini belgiladingiz!")


# Foydalanuvchining mahsulotlari
@bot.callback_query_handler(func=lambda call: call.data == "my_products")
def my_products_menu(call):
    user_id = str(call.message.chat.id)
    user_data = read_db()
    products = user_data.get(user_id, {}).get("products", [])

    if not products:
        bot.send_message(
            call.message.chat.id,
            "📦 Sizda hozircha hech qanday mahsulot yo'q. Avval mahsulot sotib oling!"
        )
        return

    message = "📦 Sizning mahsulotlaringiz:\n"
    for product in products:
        message += f"🔹 {product['name']} - {product['price']} so'm\n"

    bot.send_message(call.message.chat.id, message)


# Belgilangan mahsulotlar
@bot.callback_query_handler(func=lambda call: call.data == "selected_products")
def selected_products_menu(call):
    user_id = str(call.message.chat.id)
    user_data = read_db()
    selected_products = user_data.get(user_id, {}).get("selected_products", [])

    if not selected_products:
        bot.send_message(
            call.message.chat.id,
            "📦 Hozircha belgilangan mahsulotlar yo'q. Keyinchalik ushbu funksiya qo'shiladi."
        )
        return

    message = "📦 Sizning belgilangan mahsulotlaringiz:\n"
    markup = types.InlineKeyboardMarkup()

    for product in selected_products:
        markup.add(
            types.InlineKeyboardButton(
                f"{product['name']} - {product['price']} so'm",
                callback_data=
                f"manage_selected_{product['name']}_{product['price']}"))

    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="show_main_menu"))

    bot.send_message(call.message.chat.id, message, reply_markup=markup)


# Mahsulotni sotib olish yoki belgilanishini olib tashlash
@bot.callback_query_handler(
    func=lambda call: call.data.startswith("manage_selected_"))
def manage_selected_product(call):
    product_info = call.data.split("_")
    product_name = product_info[2]
    product_price = int(product_info[3])
    user_id = str(call.message.chat.id)

    # Mahsulotni sotib olish yoki belgilanishini olib tashlash uchun tugmalar
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            f"💸 Sotib olish",
            callback_data=f"buy_selected_{product_name}_{product_price}"))
    markup.add(
        types.InlineKeyboardButton(
            f"❌ Belgilanishni olib tashlash",
            callback_data=f"remove_selected_{product_name}"))
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga",
                                   callback_data="selected_products"))

    bot.edit_message_text(
        f"📦 {product_name} - {product_price} so'm\nSiz ushbu mahsulotni sotib olish yoki belgilanishini olib tashlashni tanlashingiz mumkin.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


# Belgilangan mahsulotni sotib olish
@bot.callback_query_handler(
    func=lambda call: call.data.startswith("buy_selected_"))
def buy_selected_product(call):
    product_info = call.data.split("_")
    product_name = product_info[2]
    product_price = int(product_info[3])
    user_id = str(call.message.chat.id)

    user_data = read_db()
    shop_data = read_shop_db()

    # Foydalanuvchi balansini tekshirish
    user_balance = user_data.get(user_id, {}).get("balance", 0)

    if user_balance < product_price:
        bot.send_message(
            call.message.chat.id,
            f"❌ Sizning balansingiz yetarli emas! Balans: {user_balance} so'm, mahsulot narxi: {product_price} so'm."
        )
        return

    # Mahsulotni sotib olish
    product = {"name": product_name, "price": product_price}
    user_data[user_id]["balance"] -= product_price
    user_data[user_id].setdefault("products", []).append(product)
    write_db(user_data)

    bot.send_message(
        call.message.chat.id,
        f"✅ Siz {product_name} mahsulotini {product_price} so'mga sotib oldingiz!"
    )

    # Belgilangan mahsulotlar ro'yxatidan o'chirish
    selected_products = user_data.get(user_id, {}).get("selected_products", [])
    selected_products = [
        p for p in selected_products if p['name'] != product_name
    ]
    user_data[user_id]["selected_products"] = selected_products
    write_db(user_data)


# Belgilangan mahsulotni olib tashlash
@bot.callback_query_handler(
    func=lambda call: call.data.startswith("remove_selected_"))
def remove_selected_product(call):
    product_name = call.data.split("_")[2]
    user_id = str(call.message.chat.id)

    user_data = read_db()
    selected_products = user_data.get(user_id, {}).get("selected_products", [])

    # Belgilangan mahsulotni olib tashlash
    selected_products = [
        p for p in selected_products if p['name'] != product_name
    ]
    user_data[user_id]["selected_products"] = selected_products
    write_db(user_data)

    bot.send_message(
        call.message.chat.id,
        f"❌ {product_name} mahsuloti belgilangan mahsulotlar ro'yxatidan olib tashlandi."
    )


# Mahsulot haqida ma'lumotlarni ko'rsatish
@bot.callback_query_handler(func=lambda call: call.data.startswith("details_"))
def product_details(call):
    # Mahsulot ID sini callback ma'lumotlardan olish
    product_id = call.data.split("_")[1]

    # Dukon ma'lumotlar bazasidan shop ma'lumotlarini o'qish
    shop_data = read_shop_db()

    # Dukon ma'lumotlaridan mahsulotni olish
    product = shop_data.get(product_id)

    # Agar mahsulot topilmasa, foydalanuvchiga xatolik haqida xabar yuborish
    if not product:
        bot.send_message(call.message.chat.id,
                         "❌ Mahsulot ma'lumotlari topilmadi!")
        return

    # Mahsulot haqida ma'lumotlarni shakllantirish
    message = f"📦 Mahsulot: {product['name']}\n"
    message += f"💰 Narxi: {product['price']} so'm\n"
    message += f"📏 O'lcham: {product.get('size', 'Malumot yoq')}\n"
    message += f"🌟 Reyting: {product.get('rating', 'Malumot yoq')}\n"
    message += f"🛠 Ishlab chiqaruvchi: {product.get('manufacturer', 'Malumot yoq')}\n",


# **Bepul onlayn darsliklar**
@bot.callback_query_handler(func=lambda call: call.data == "free_courses")
def free_courses(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🌍 Xalqaro universitetlar kurslari",
                                   callback_data="international_courses"))
    markup.add(
        types.InlineKeyboardButton("🇺🇿 O‘zbek universitetlari kurslari",
                                   callback_data="uzbek_courses"))
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="hizmatlar"))

    bot.edit_message_text(
        "📚 *Bepul onlayn darsliklar:* \n\n"
        "🔹 Xalqaro va O‘zbek universitetlarining bepul darsliklari va kurslari bilan tanishing. \n"
        "🌍 Dunyodagi eng yaxshi universitetlardan bepul o‘quv materiallari va kurslar.\n"
        "🇺🇿 O‘zbekistondagi universitetlar va o‘quv markazlarining bepul onlayn kurslari.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown")


# **Xalqaro universitetlar kurslari**
@bot.callback_query_handler(
    func=lambda call: call.data == "international_courses")
def international_courses(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="free_courses"))

    bot.edit_message_text(
        "🌍 *Xalqaro universitetlar kurslari:* \n\n"
        "📌 *Harvard University* - [Kurslar ro‘yxati](https://online-learning.harvard.edu/)\n"
        "📌 *MIT OpenCourseWare* - [Kurslar ro‘yxati](https://ocw.mit.edu/index.htm)\n"
        "📌 *Coursera* - [Bepul kurslar](https://www.coursera.org/courses?query=free)\n"
        "📌 *edX* - [Bepul kurslar](https://www.edx.org/)\n"
        "📌 *Stanford University* - [Stanford Online](https://online.stanford.edu/)\n\n"
        "📚 Yuqoridagi saytlar orqali turli xil sohalarda bepul kurslar va materiallarga ega bo‘ling.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown")


# **O‘zbek universitetlari kurslari**
@bot.callback_query_handler(func=lambda call: call.data == "uzbek_courses")
def uzbek_courses(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="free_courses"))

    bot.edit_message_text(
        "🇺🇿 *O‘zbek universitetlari kurslari:* \n\n"
        "📌 *Tashkent University of Information Technologies* - [Kurslar ro‘yxati](https://www.tuit.uz/en)\n"
        "📌 *National University of Uzbekistan* - [Kurslar ro‘yxati](http://www.nuuz.uz/en)\n"
        "📌 *Samarkand State University* - [Onlayn kurslar](https://www.sdu.uz/en/)\n"
        "📌 *Uzbekistan State World Languages University* - [Onlayn kurslar](https://www.uzswlu.uz/en/)\n\n"
        "📚 O‘zbekistondagi universitetlarning bepul kurslarini ushbu saytlar orqali toping.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown")


# **Dasturlash va texnologiya kurslari**
@bot.callback_query_handler(
    func=lambda call: call.data == "programming_courses")
def programming_courses(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🐍 Python kurslari",
                                   callback_data="python_courses"))
    markup.add(
        types.InlineKeyboardButton("🖥️ JavaScript kurslari",
                                   callback_data="javascript_courses"))
    markup.add(
        types.InlineKeyboardButton("🎨 UI/UX dizayn kurslari",
                                   callback_data="uiux_courses"))
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="hizmatlar"))

    bot.edit_message_text(
        "💻 *Dasturlash va texnologiya kurslari:* \n\n"
        "🔹 Python, JavaScript, UI/UX dizayn va boshqa kurslar.\n"
        "🌐 Dunyodagi eng yaxshi platformalardan bepul va to‘lovli kurslar.\n"
        "📚 Tanlang va kursni boshlang.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown")


# **Python kurslari**
@bot.callback_query_handler(func=lambda call: call.data == "python_courses")
def python_courses(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga",
                                   callback_data="programming_courses"))

    bot.edit_message_text(
        "🐍 *Python dasturlash tilida kurslar:* \n\n"
        "📌 *Harvard's CS50's Introduction to Computer Science* - [Kurs linki](https://online-learning.harvard.edu/course/cs50-introduction-computer-science)\n"
        "📌 *Python for Everybody* - [Kurs linki](https://www.coursera.org/specializations/python)\n"
        "📌 *Python Programming Essentials* - [Kurs linki](https://www.coursera.org/learn/python-programming)\n\n"
        "📚 Yuqoridagi kurslar Python dasturlash tilini o‘rganish uchun mukammal resurslardir.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown")


# **JavaScript kurslari**
@bot.callback_query_handler(
    func=lambda call: call.data == "javascript_courses")
def javascript_courses(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga",
                                   callback_data="programming_courses"))

    bot.edit_message_text(
        "🖥️ *JavaScript dasturlash tilida kurslar:* \n\n"
        "📌 *JavaScript for Beginners* - [Kurs linki](https://www.udemy.com/course/the-complete-javascript-course/)\n"
        "📌 *JavaScript Basics* - [Kurs linki](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Introduction)\n"
        "📌 *Modern JavaScript From The Beginning* - [Kurs linki](https://www.udemy.com/course/modern-javascript-from-the-beginning/)\n\n"
        "📚 Yuqoridagi kurslar JavaScript tilini o‘rganish uchun eng yaxshi manbalar.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown")


# **UI/UX dizayn kurslari**
@bot.callback_query_handler(func=lambda call: call.data == "uiux_courses")
def uiux_courses(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga",
                                   callback_data="programming_courses"))

    bot.edit_message_text(
        "🎨 *UI/UX dizayn kurslari:* \n\n"
        "📌 *Introduction to UX Design* - [Kurs linki](https://www.coursera.org/learn/ux-design)\n"
        "📌 *UI/UX Design with Figma* - [Kurs linki](https://www.udemy.com/course/ui-ux-web-design-using-figma/)\n"
        "📌 *User Experience Design Essentials* - [Kurs linki](https://www.udemy.com/course/user-experience-design-essentials/)\n\n"
        "📚 Yuqoridagi kurslar UI/UX dizaynini o‘rganish uchun foydalidir.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown")


    # **Valyuta kurslari va konvertatsiya**
@bot.callback_query_handler(
    func=lambda call: call.data == "currency_converter")
def currency_converter(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔄 Valyuta konvertatsiyasi",
                                   callback_data="currency_conversion"))
    markup.add(
        types.InlineKeyboardButton("📊 Valyuta kurslarini ko‘rish",
                                   callback_data="view_currency_rates"))
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="hizmatlar"))

    bot.edit_message_text(
        "💸 *Valyuta kurslari va konvertatsiya:* \n\n"
        "🔹 Valyutalar o‘rtasidagi kursni ko‘rish yoki konvertatsiya qilish uchun quyidagi variantni tanlang.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown")


import requests

# Replace with your actual API URL and API key
API_URL = "https://v6.exchangerate-api.com/v6/e1c7dcfc23f9d541d4402ee6/latest/USD"


# **Valyuta kurslarini ko‘rish**
@bot.callback_query_handler(
    func=lambda call: call.data == "view_currency_rates")
def view_currency_rates(call):
    # API orqali valyuta kurslarini olish
    response = requests.get(API_URL)
    data = response.json()

    if response.status_code == 200:
        rates = data.get('rates', {})
        message = "💰 *Valyuta kurslari (USD asosida):*\n\n"
        for currency, rate in rates.items():
            message += f"{currency}: {rate:.2f}\n"

        bot.edit_message_text(message,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              parse_mode="Markdown")
    else:
        bot.edit_message_text(
            "❌ Valyuta kurslarini olishda xatolik yuz berdi.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id)


# **Valyuta konvertatsiyasi**
@bot.callback_query_handler(
    func=lambda call: call.data == "currency_conversion")
def ask_currency_conversion(call):
    msg = bot.send_message(
        call.message.chat.id,
        "💸 *Valyuta konvertatsiyasi:* \n\nIltimos, USD miqdorini kiriting (masalan: 1)."
    )
    bot.register_next_step_handler(msg, perform_currency_conversion)


# **Valyuta konvertatsiyasini amalga oshirish**
def perform_currency_conversion(message):
    try:
        # Kirilgan miqdorni olish
        amount = float(message.text)  # User input will be converted to a float

        # API orqali valyuta kursini olish
        response = requests.get(API_URL)

        # Checking if the response is successful
        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates', {})

            # If UZS rate is available
            if "UZS" in rates:
                # Convert the entered USD amount to UZS
                usd_to_uzs_rate = rates["UZS"]
                converted_amount = amount * usd_to_uzs_rate  # Convert entered amount from USD to UZS
                bot.send_message(
                    message.chat.id,
                    f"💰 *Konvertatsiya natijasi:*\n\n{amount} USD -> {converted_amount:.2f} UZS",
                    parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id,
                                 "❌ UZS valyutasi kursi topilmadi!")
        else:
            bot.send_message(
                message.chat.id,
                "❌ Valyuta kurslarini olishda xatolik yuz berdi.")
    except ValueError:
        # Catching errors if the input is not a valid number
        bot.send_message(message.chat.id,
                         "❌ Iltimos, faqat raqam kiriting (masalan: 1).")
    except Exception as e:
        # Catching any other unexpected errors
        bot.send_message(message.chat.id, f"❌ Xatolik yuz berdi: {str(e)}")


        # **Tavsiya etilgan kitoblar bo‘limi**
@bot.callback_query_handler(func=lambda call: call.data == "recommended_books")
def recommended_books(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📚 Eng yaxshi kitoblar",
                                   callback_data="best_books"))
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="hizmatlar"))

    bot.edit_message_text(
        "📖 *Tavsiya etilgan kitoblar:* \n\n"
        "🔹 O‘qish uchun eng yaxshi kitoblar ro‘yxatini ko‘rish.\n"
        "📚 Foydalanuvchilarga o‘qish uchun foydali va motivatsion kitoblar.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown")


# **Eng yaxshi kitoblar**
@bot.callback_query_handler(func=lambda call: call.data == "best_books")
def best_books(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga",
                                   callback_data="recommended_books"))

    bot.edit_message_text(
        "📚 *Eng yaxshi kitoblar:* \n\n"
        "📌 *Atomic Habits* - James Clear\n"
        "📌 *The Power of Now* - Eckhart Tolle\n"
        "📌 *The Lean Startup* - Eric Ries\n"
        "📌 *Sapiens: A Brief History of Humankind* - Yuval Noah Harari\n"
        "📌 *Thinking, Fast and Slow* - Daniel Kahneman\n\n"
        "📚 Bu kitoblar o‘zini rivojlantirish, biznes va psixologiya haqida eng yaxshi tavsiyalarni beradi.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown")


import requests
from telebot import TeleBot, types

# Bot tokenini kiriting

# Weatherstack API kaliti
WEATHERSTACK_API_KEY = "9203864ca64c588e595e0cef3c25bedc"

# Viloyatlar ro'yxati
regions = [
    "Toshkent", "Samarqand", "Buxoro", "Farg'ona", "Namangan", "Andijon",
    "Qashqadaryo", "Surxondaryo", "Jizzax", "Sirdaryo", "Xorazm", "Navoiy"
]


@bot.callback_query_handler(func=lambda call: call.data == "hizmat1")
def show_regions(call):
    # Viloyatlar tugmalarini yaratish
    markup = types.InlineKeyboardMarkup()
    for region in regions:
        markup.add(
            types.InlineKeyboardButton(region,
                                       callback_data=f"weather_{region}"))
    markup.add(
        types.InlineKeyboardButton(
            "🔙 Orqaga", callback_data="hizmatlar"))  # Orqaga tugmasi

    # Foydalanuvchiga viloyatlar ro'yxatini ko'rsatish
    bot.edit_message_text("O'zbekiston viloyatlaridan birini tanlang:",
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("weather_"))
def send_weather(call):
    region = call.data.split("_")[1]  # Viloyat nomini olish
    weather_data = get_weather(region)  # Ob-havo ma'lumotini olish

    if weather_data:
        # Ob-havo ma'lumotini formatlash va jo'natish
        response_text = (
            f"🌤 Ob-havo ma'lumotlari: {region}\n\n"
            f"🌡 Harorat: {weather_data['temperature']}°C\n"
            f"🌪 Shamol tezligi: {weather_data['wind_speed']} km/soat\n"
            f"💧 Namlik: {weather_data['humidity']}%\n"
            f"⛅️ Tavsif: {weather_data['weather_descriptions'][0]}")
    else:
        response_text = "❌ Ob-havo ma'lumotlari topilmadi. Iltimos, viloyat nomini tekshirib ko'ring."

    # Foydalanuvchiga javob yuborish
    bot.send_message(call.message.chat.id, response_text)


@bot.callback_query_handler(func=lambda call: call.data == "hizmatlar")
def go_back_to_services(call):
    # Hizmatlar menyusiga qaytish
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🌤 Ob-havo ma'lumotlari",
                                   callback_data="hizmat1"))
    bot.edit_message_text(
        "Hizmatlar bo'limiga xush kelibsiz! Quyidagi bo'limlardan birini tanlang:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup)


def get_weather(region):
    # Weatherstack API'ga so'rov yuborish
    url = f"http://api.weatherstack.com/current?access_key={WEATHERSTACK_API_KEY}&query={region}"
    try:
        response = requests.get(url)
        data = response.json()
        if "current" in data:
            return data["current"]
        else:
            return None
    except Exception as e:
        print(f"API xatolik: {str(e)}")
        return None


# Botni ishga tushirish

# Weatherstack API kaliti
# Viloyatlar ro'yxati

import json
from datetime import datetime, timedelta
from telebot import types

# Ma'lumotlar bazasi
DB_FILE = "database.json"


# JSON'dan foydalanuvchilarni o‘qish
def read_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# JSON'ga ma'lumot yozish
def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# **Bloklangan foydalanuvchilarni tekshirish**
def check_if_blocked(user_id):
    users = read_db()
    user = users.get(str(user_id), None)
    if user and user.get("blocked", False):
        return True
    return False


# **Asosiy menyu ko‘rsatish**
@bot.callback_query_handler(func=lambda call: call.data == "show_main_menu")
def show_main_menu(call):
    user_id = call.from_user.id
    data = read_db()
    user = data.get(str(user_id))

    # Agar foydalanuvchi bloklangan bo‘lsa
    if user and user.get("blocked", False):
        blocked_until = datetime.fromisoformat(user["blocked_until"])
        remaining_time = blocked_until - datetime.now()
        bot.edit_message_text(
            f"🚫 Siz bloklangansiz!\n⏳ Blokdan chiqarilish vaqti: {blocked_until.strftime('%Y-%m-%d %H:%M:%S')}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id)
        return

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👤 Kabinet",
                                          callback_data="kabinet"))
    markup.add(
        types.InlineKeyboardButton("📊 Statistika",
                                   callback_data="show_statistics"))
    markup.add(
        types.InlineKeyboardButton("📩 Admin bilan bog‘lanish",
                                   callback_data="contact_admin"))
    markup.add(types.InlineKeyboardButton("⭐️ Reyting",
                                          callback_data="rating"))
    markup.add(
        types.InlineKeyboardButton("🎁 Kunlik bonus",
                                   callback_data="daily_bonus"))
    markup.add(
        types.InlineKeyboardButton("🛠 Hizmatlar", callback_data="hizmatlar"))
    # **Web-App tugmachasi**
    web_app_url = "https://webapp-git-main-termuxuchuns-projects.vercel.app/"  # Web ilovangiz URL manzilini shu yerga kiriting
    markup.add(
        types.InlineKeyboardButton("🌐 Web App",
                                   web_app=types.WebAppInfo(url=web_app_url)))

    bot.edit_message_text("📍 Asosiy Menyu:",
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=markup)


# **Kabinet menyusi**
@bot.callback_query_handler(func=lambda call: call.data == "kabinet")
def cabinet_menu(call):
    user_id = call.from_user.id
    data = read_db()
    user = data.get(str(user_id))

    if check_if_blocked(user_id):
        bot.send_message(
            call.message.chat.id,
            "🚫 Siz bloklangansiz! Iltimos, admin bilan bog‘laning.")
        return

    if user:
        balance = user.get("balance", 0)
        formatted_balance = f"{balance:,.2f} so‘m"  # Balansni formatlash

        stats_message = (
            f"📋 *Sizning hisobingiz:*\n\n"
            f"📱 *Telefon raqami:* {user.get('phone_number', 'N/A')}\n"
            f"👤 *Username:* {user.get('username', 'N/A')}\n"
            f"💰 *Balans:* {formatted_balance}\n"
            f"⭐️ *Reyting:* {user.get('rating', 'N/A')} ball\n")

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("📊 Kirim va chiqimlar",
                                       callback_data="view_transactions"))
        markup.add(
            types.InlineKeyboardButton("📝 Username-ni tahrirlash",
                                       callback_data="edit_username"))
        markup.add(
            types.InlineKeyboardButton("➕ Hisobni to‘ldirish",
                                       callback_data="add_balance"))
        markup.add(
            types.InlineKeyboardButton("💸 Pul yechish",
                                       callback_data="withdraw_money"))
        markup.add(
            types.InlineKeyboardButton("❌ Hisobni o‘chirish",
                                       callback_data="delete_account"))
        markup.add(
            types.InlineKeyboardButton("🔙 Orqaga",
                                       callback_data="show_main_menu"))

        bot.edit_message_text(stats_message,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup,
                              parse_mode="Markdown")
    else:
        bot.edit_message_text(
            "❌ Sizning hisobingiz mavjud emas. Iltimos, qaytadan urinib ko‘ring.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "rating")
def rating_menu(call):
    user_id = call.from_user.id
    data = read_db()

    user = data.get(str(user_id))

    if user:
        # Foydalanuvchilarni balansga qarab tartiblash
        sorted_users = sorted(data.items(),
                              key=lambda x: x[1]["balance"],
                              reverse=True)

        ranking_message = "📊 Reyting:\n\n"
        for idx, (user_id, user_data) in enumerate(
                sorted_users[:10]
        ):  # Eng yuqori 10 ta foydalanuvchini ko‘rsatish
            balance = user_data["balance"]
            # Print user_data to check its structure
            print(user_data
                  )  # This will help you debug the structure of user_data

            # Check if 'user_id' key exists in user_data, otherwise fall back to another key
            user_name = user_data.get(
                "user_id",
                "Unknown")  # Use a fallback key if 'user_id' is not found

            # Formating balance to show in either millions or regular currency
            if balance >= 1_000_000:
                formatted_balance = f"{balance / 1_000_000:.2f} mln"
            else:
                formatted_balance = f"{balance:.2f} so‘m"
            ranking_message += f"{idx + 1}. @{user_name} - {formatted_balance}\n"

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🔙 Orqaga",
                                       callback_data="show_main_menu"))

        bot.edit_message_text(ranking_message,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup)
    else:
        bot.edit_message_text("Siz hali ro‘yxatdan o‘tmagansiz.",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)


# Hisobni o‘chirish tasdiqlash
@bot.callback_query_handler(func=lambda call: call.data == "delete_account")
def confirm_account_deletion(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("❌ Bekor qilish",
                                   callback_data="cancel_deletion"))
    markup.add(
        types.InlineKeyboardButton("✅ O‘chirish",
                                   callback_data="delete_confirm"))
    markup.add(types.InlineKeyboardButton("🔙 Orqaga", callback_data="kabinet"))

    bot.edit_message_text(
        "⚠️ Diqqat! Akkauntingiz va hisobingiz butunlay o‘chiriladi. Rozimisiz?",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
    )


# Orqaga tugmasi ishlashi
@bot.callback_query_handler(func=lambda call: call.data == "show_main_menu")
def go_back_to_main_menu(call):
    show_main_menu(call.message.chat.id, call.message.message_id)


# Hisobni o‘chirishni bekor qilish
@bot.callback_query_handler(func=lambda call: call.data == "cancel_deletion")
def cancel_account_deletion(call):
    bot.edit_message_text("❌ Hisobni o‘chirish bekor qilindi.",
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id)


# Akkauntni o‘chirishni tasdiqlash
@bot.callback_query_handler(func=lambda call: call.data == "delete_confirm")
def delete_account(call):
    user_id = call.from_user.id

    # Foydalanuvchi ma'lumotlarini o‘chirish
    data = read_db()
    data.pop(str(user_id), None)
    write_db(data)

    bot.edit_message_text(
        "✅ Akkauntingiz va hisobingiz muvaffaqiyatli o‘chirildi.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id)


ADMIN_ID = 8157810564
# Foydalanuvchi ma'lumotlarini saqlash uchun fayl nomi
DB_FILE = "database.json"


# Ma'lumotlar bazasini o'qish funksiyasi
def read_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Ma'lumotlar bazasini yozish funksiyasi
def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Hisobni to‘ldirish bo‘limi
@bot.callback_query_handler(func=lambda call: call.data == "add_balance")
def add_balance_menu(call):
    msg = bot.send_message(
        call.message.chat.id, "Hisobingizni nechpul deposit qilmoqchisiz?\n"
        "Iltimos, 2000 dan 10 000 000 gacha bo‘lgan summani kiriting:")
    bot.register_next_step_handler(msg, process_balance_addition)


def process_balance_addition(message):
    try:
        user_id = message.from_user.id
        amount = int(message.text)

        # Minimal va maksimal miqdorni tekshirish
        if amount < 2000 or amount > 10000000:
            bot.send_message(
                message.chat.id,
                "❌ Iltimos, to‘g‘ri miqdorni kiriting (2000 dan 10 000 000bo‘lishi kerak)."
            )
            return

        # To‘lov uchun karta ma'lumotlarini ko‘rsatish
        bot.send_message(
            message.chat.id,
            f"✅ {amount} so‘m miqdorini hisobingizga deposit qilmoqchisiz.\n\n"
            "Iltimos, ushbu karta raqamiga pul o‘tkazing:\n"
            "9860 1701 1535 8567\n\n"
            "To‘lovni amalga oshirgandan so‘ng, chekning fotosuratini yuboring.",
            parse_mode="Markdown")
        # Chekni qabul qilishni kutish
        bot.register_next_step_handler(message, verify_payment, amount)

    except ValueError:
        bot.send_message(
            message.chat.id,
            "❌ Iltimos, to‘g‘ri summani kiriting (raqam ko‘rinishida).")


# To‘lovni tasdiqlashdan so‘ng adminga xabar yuborish
def verify_payment(message, amount):
    if message.content_type == "photo":
        user_id = message.from_user.id
        username = message.from_user.username or "Noma'lum"

        # Admin uchun xabarni tayyorlash
        caption = (
            f"💵 **Yangi to‘lov tekshiruvi:**\n\n"
            f"👤 Foydalanuvchi: @{username} (ID: {user_id})\n"
            f"💰 Miqdor: {amount} so‘m\n\n"
            f"✅ Tasdiqlash yoki ❌ Rad etish uchun quyidagi tugmalardan foydalaning."
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                "✅ Tasdiqlash", callback_data=f"approve_{user_id}_{amount}"),
            types.InlineKeyboardButton(
                "❌ Rad etish", callback_data=f"reject_{user_id}_{amount}"))

        # Admin ID-ga xabarni yuborish
        bot.send_photo(ADMIN_ID,
                       message.photo[-1].file_id,
                       caption=caption,
                       reply_markup=markup)

        bot.send_message(
            message.chat.id,
            "✅ Chek qabul qilindi. To‘lov tekshirilmoqda. Admin tasdiqlashi kerak."
        )
    else:
        bot.send_message(
            message.chat.id,
            "❌ To‘lovni tasdiqlash uchun chekning fotosuratini yuboring.")


# Admin tomonidan tasdiqlash yoki rad etish
@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_")
                            or call.data.startswith("reject_"))
def handle_payment_approval(call):
    action, user_id, amount = call.data.split("_")
    user_id = int(user_id)
    amount = int(amount)

    data = read_db()
    if action == "approve":
        # Foydalanuvchi ma'lumotlarini tekshirish va hisobni yangilash
        if str(user_id) not in data:
            data[str(user_id)] = {"balance": 0}
        data[str(user_id)]["balance"] += amount
        write_db(data)

        new_balance = data[str(user_id)]["balance"]

        # Foydalanuvchiga tasdiqlash xabarini yuborish
        bot.send_message(
            user_id, f"✅ Admin tomonidan to‘lovingiz tasdiqlandi.\n"
            f"💰 Hisobingizga {amount} so‘m qo‘shildi.\n"
            f"Yangi balans: {new_balance} so‘m")

        # Adminga tasdiqlash haqida xabar
        bot.send_message(
            call.message.chat.id,
            f"✅ Foydalanuvchi ID: {user_id} uchun to‘lov tasdiqlandi.")

    elif action == "reject":
        # Foydalanuvchiga rad etilganligini bildirish
        bot.send_message(
            user_id,
            "❌ Admin tomonidan to‘lovingiz rad etildi. Iltimos, ma'lumotlarni tekshirib, qayta yuboring."
        )

        # Adminga rad etish haqida xabar
        bot.send_message(
            call.message.chat.id,
            f"❌ Foydalanuvchi ID: {user_id} uchun to‘lov rad etildi.")


# Kirim va chiqimlarni ko‘rish
@bot.callback_query_handler(func=lambda call: call.data == "view_transactions")
def view_transactions(call):
    user_id = call.from_user.id
    data = read_db()
    user = data.get(str(user_id))

    if user:
        # Kirim va chiqimlar ma'lumotlari
        transactions = user.get("transactions", [])

        if not transactions:
            bot.edit_message_text(
                "📊 Sizda hali hech qanday kirim yoki chiqim qayd etilmagan.",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
            return

        # Tranzaktsiyalarni formatlash
        transactions_message = "📊 Sizning kirim va chiqimlaringiz:\n\n"
        for idx, transaction in enumerate(transactions, start=1):
            transaction_type = "➕ Kirim" if transaction[
                "type"] == "deposit" else "➖ Chiqim"
            transactions_message += (
                f"{idx}. {transaction_type}\n"
                f"   💰 Miqdor: {transaction['amount']:.2f} so‘m\n"
                f"   📅 Sana: {transaction['date']}\n\n")

        # Orqaga qaytish tugmasi
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🔙 Orqaga", callback_data="kabinet"))

        bot.edit_message_text(
            transactions_message,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup,
        )
    else:
        bot.edit_message_text(
            "❌ Ma'lumotlar topilmadi.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )


@bot.callback_query_handler(func=lambda call: call.data == "withdraw_money")
def withdraw_money(call):
    user_id = call.from_user.id
    data = read_db()

    user = data.get(str(user_id))

    if user:
        balance = user["balance"]

        # Check if the user has enough balance to withdraw
        if balance > 0:
            bot.send_message(
                call.message.chat.id,
                "Iltimos, yechmoqchi bo‘lgan miqdorni kiriting (so‘m):")
            bot.register_next_step_handler(call.message, ask_payment_method,
                                           user_id, balance)
        else:
            bot.send_message(
                call.message.chat.id,
                "Sizning hisobingizda yechish uchun pul mavjud emas.")
    else:
        bot.send_message(call.message.chat.id,
                         "Siz hali ro‘yxatdan o‘tmagansiz.")


def ask_payment_method(message, user_id, balance):
    try:
        amount = float(message.text.strip())

        if amount <= 0:
            bot.send_message(message.chat.id,
                             "Iltimos, ijobiy miqdor kiriting.")
        elif amount > balance:
            bot.send_message(
                message.chat.id,
                f"Sizda faqat {balance} so‘m mavjud. Kichikroq miqdor kiriting."
            )
        else:
            # Provide inline buttons for Paynet/Karta with a Cancel option
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton(
                    "💳 Karta",
                    callback_data=f"withdraw_card_{user_id}_{amount}"))
            markup.add(
                types.InlineKeyboardButton(
                    "💰 Paynet",
                    callback_data=f"withdraw_paynet_{user_id}_{amount}"))
            bot.send_message(message.chat.id,
                             "Iltimos, pulni qanday to'lashni tanlang:",
                             reply_markup=markup)
    except ValueError:
        bot.send_message(message.chat.id,
                         "Iltimos, to‘g‘ri miqdorni kiriting.")


# Assuming your database file is called 'database.json'
DB_FILE = 'database.json'
ADMIN_ID = '8157810564'  # Replace this with your admin ID


# Function to read from the database
def read_db():
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Function to save to the database
def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# Handle withdrawal request for card or paynet
@bot.callback_query_handler(
    func=lambda call: call.data.startswith("withdraw_"))
def handle_payment_method(call):
    data = call.data.split("_")

    # Check if the data is in the expected format
    if len(data) < 4:
        bot.send_message(
            call.message.chat.id,
            "Ma'lumotlar noto'g'ri formatda. Iltimos, qaytadan urinib ko'ring."
        )
        return

    method = data[1]  # 'card' or 'paynet'
    user_id = int(data[2])  # user ID
    amount = float(data[3])  # requested withdrawal amount

    # Get user data from database
    user_data = read_db().get(str(user_id), None)

    if user_data:
        balance = user_data.get("balance", 0)

        # Check if the user has enough balance
        if balance >= amount:
            # Proceed with requesting the card or Paynet number
            if method == "card":
                bot.send_message(
                    call.message.chat.id,
                    "Iltimos, 16 raqamli kartangizni kiriting (8600 0000 0000 0000 formatida):"
                )
                bot.register_next_step_handler(call.message,
                                               process_card_number, user_id,
                                               amount, balance)
            elif method == "paynet":
                bot.send_message(call.message.chat.id,
                                 "Iltimos, Paynet raqamingizni kiriting:")
                bot.register_next_step_handler(call.message,
                                               process_paynet_number, user_id,
                                               amount, balance)
        else:
            # If balance is insufficient
            bot.send_message(
                call.message.chat.id,
                f"Sizning hisobingizda {balance} so‘m mavjud. Yechmoqchi bo‘lgan summa {amount} so‘mga teng. Iltimos, kichikroq summa kiriting."
            )
    else:
        bot.send_message(
            call.message.chat.id,
            "Sizning hisobingiz mavjud emas. Iltimos, qaytadan urinib ko‘ring."
        )


# Process card number and update the balance
def process_card_number(message, user_id, amount, balance):
    card_number = message.text.strip()

    # Validate the card number (it should be 16 digits)
    if len(card_number) == 16 and card_number.isdigit():
        # Deduct the amount from the balance
        new_balance = balance - amount

        # Update the database with the new balance
        data = read_db()
        data[str(user_id)]["balance"] = new_balance
        save_db(data)

        # Notify the admin with the user's request
        bot.send_message(
            ADMIN_ID, f"Yangi pul yechish so'rovi:\n\n"
            f"👤 Foydalanuvchi ID: {user_id}\n"
            f"💰 Yechmoqchi bo‘lgan summa: {amount} so‘m\n"
            f"🗄 To'lov usuli: Karta\n"
            f"💳 Karta raqami: {card_number}\n"
            f"💸 Hisobdan yechilgan summa: {amount} so‘m\n"
            f"💳 Yangi balans: {new_balance} so‘m")

        # Notify the user
        bot.send_message(
            message.chat.id,
            f"✅ Surovingiz qabul qilindi. Hisobingizdan {amount} so‘m yechildi. Yangi balans: {new_balance} so‘m.",
        )

        # Edit the message to inform that the request has been processed
        bot.edit_message_text("Pul yechish so'rovi yuborildi!",
                              chat_id=message.chat.id,
                              message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,
                         "Iltimos, 16 raqamli kartangizni to‘g‘ri kiriting.")


# Process Paynet number and update the balance
def process_paynet_number(message, user_id, amount, balance):
    paynet_number = message.text.strip()

    # Validate Paynet number (simple validation here, you can add more rules if needed)
    if paynet_number.isdigit():
        # Deduct the amount from the balance
        new_balance = balance - amount

        # Update the database with the new balance
        data = read_db()
        data[str(user_id)]["balance"] = new_balance
        save_db(data)

        # Notify the admin with the user's request
        bot.send_message(
            ADMIN_ID, f"Yangi pul yechish so'rovi:\n\n"
            f"👤 Foydalanuvchi ID: {user_id}\n"
            f"💰 Yechmoqchi bo‘lgan summa: {amount} so‘m\n"
            f"🗄 To'lov usuli: Paynet\n"
            f"📱 Paynet raqami: {paynet_number}\n"
            f"💸 Hisobdan yechilgan summa: {amount} so‘m\n"
            f"📱 Yangi balans: {new_balance} so‘m")

        # Notify the user
        bot.send_message(
            message.chat.id,
            f"✅ Surovingiz qabul qilindi. Hisobingizdan {amount} so‘m yechildi. Yangi balans: {new_balance} so‘m.",
        )

        # Edit the message to inform that the request has been processed
        bot.edit_message_text("Pul yechish so'rovi yuborildi!",
                              chat_id=message.chat.id,
                              message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,
                         "Iltimos, Paynet raqamingizni to‘g‘ri kiriting.")


from datetime import datetime
from telebot import types


# Kunlik bonus callback handler
@bot.callback_query_handler(func=lambda call: call.data == "daily_bonus")
def daily_bonus(call):
    user_id = call.from_user.id
    data = read_db()
    user = data.get(str(user_id))

    # "Orqaga" tugmasini yaratish
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="show_main_menu"))

    if user:
        last_bonus = user.get("last_bonus")
        now = datetime.now()

        if last_bonus and (now - datetime.fromisoformat(last_bonus)).days < 1:
            bot.edit_message_text("❌ Siz bugungi bonusni allaqachon oldingiz.",
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=markup)
        else:
            # Bonusni qo‘shish
            user["balance"] += 1000  # Add 1000 to balance as the bonus
            user["last_bonus"] = now.isoformat()  # Update last bonus timestamp
            write_db(data)

            bot.edit_message_text(
                "🎁 Kunlik bonusingiz muvaffaqiyatli qo‘shildi! 1000 so‘m.",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=markup)
    else:
        bot.edit_message_text("❌ Siz hali ro‘yxatdan o‘tmagansiz.",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup)


import json
from telebot import types

# Adminlar ro‘yxati
ADMINS = [8157810564]  # O'zingizning Telegram ID'ingizni yozing

# Ma'lumotlar bazasi
DB_FILE = "database.json"


# JSON'dan foydalanuvchilarni o‘qish
def read_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# JSON'ga ma'lumot yozish
def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# **Bloklangan foydalanuvchilarni tekshirish**
def check_if_blocked(user_id):
    users = read_db()
    user = users.get(str(user_id), None)
    if user and user.get("blocked", False):
        return True
    return False


# **Asosiy menyu ko‘rsatish (Kabinet, Statistika, Hizmatlar va boshqalar)**
@bot.callback_query_handler(func=lambda call: call.data == "show_main_menu")
def show_main_menu_handler(call):
    show_main_menu(chat_id=call.message.chat.id,
                   message_id=call.message.message_id)


# **Asosiy menyu funksiyasi**
def show_main_menu(chat_id, message_id=None):
    # Bloklangan foydalanuvchi uchun xabar yuborish
    if check_if_blocked(
            chat_id):  # call.from_user.id o‘rniga chat_id qo‘llanadi
        bot.send_message(
            chat_id, "🚫 Siz bloklangansiz! Iltimos, admin bilan bog‘laning.")
        return

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👤 Kabinet",
                                          callback_data="kabinet"))
    markup.add(
        types.InlineKeyboardButton("📊 Statistika",
                                   callback_data="show_statistics"))
    markup.add(
        types.InlineKeyboardButton("📩 Admin bilan bog‘lanish",
                                   callback_data="contact_admin"))
    markup.add(types.InlineKeyboardButton("⭐️ Reyting",
                                          callback_data="rating"))
    markup.add(
        types.InlineKeyboardButton("🎁 Kunlik bonus",
                                   callback_data="daily_bonus"))
    markup.add(
        types.InlineKeyboardButton("🛠 Hizmatlar", callback_data="hizmatlar"))

    web_app_url = "https://webapp-git-main-termuxuchuns-projects.vercel.app/"  # Web ilovangiz URL manzilini shu yerga kiriting
    markup.add(
        types.InlineKeyboardButton("🌐 Web App",
                                   web_app=types.WebAppInfo(url=web_app_url)))

    bot.send_message(chat_id, "Asosiy Menyu:", reply_markup=markup)


# **Menyu (Kabinet, Statistika, Hizmatlar va boshqalar)**
@bot.callback_query_handler(
    func=lambda call: call.data in ["kabinet", "daily_bonus", "hizmatlar"])
def handle_menu_selection(call):
    # Foydalanuvchi bloklanganligini tekshirish
    if check_if_blocked(call.from_user.id):
        bot.send_message(
            call.message.chat.id,
            "🚫 Siz bloklangansiz! Iltimos, admin bilan bog‘laning.")
        return

    # Menyudagi bo‘limlar
    if call.data == "kabinet":
        # Kabinet bo‘limi uchun kod
        pass

    elif call.data == "daily_bonus":
        # Kunlik bonus bo‘limi uchun kod
        pass
    elif call.data == "hizmatlar":
        # Hizmatlar bo‘limi uchun kod
        pass


import json

# Kichik adminlar ro'yxatini faylga saqlash
SUB_ADMINS_FILE = "sub_admins.json"


def load_sub_admins():
    try:
        with open(SUB_ADMINS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_sub_admins():
    with open(SUB_ADMINS_FILE, "w") as file:
        json.dump(SUB_ADMINS, file)


SUB_ADMINS = load_sub_admins()


@bot.message_handler(commands=["panel"])
def open_admin_panel(message):
    if message.chat.id not in ADMINS and message.chat.id not in SUB_ADMINS:
        bot.send_message(message.chat.id, "🚫 Siz admin emassiz!")
        return

    markup = types.InlineKeyboardMarkup()

    if message.chat.id in ADMINS:
        markup.add(
            types.InlineKeyboardButton("👥 Foydalanuvchilar",
                                       callback_data="view_users"))
        markup.add(
            types.InlineKeyboardButton("👨‍💻 Fake obunachilar yaratish",
                                       callback_data="create_fake_users"))
        markup.add(
            types.InlineKeyboardButton("📊 Statistika",
                                       callback_data="view_stats"))
        markup.add(
            types.InlineKeyboardButton("📈 Botning statistikasi",
                                       callback_data="view_bot_stats"))
        markup.add(
            types.InlineKeyboardButton("🛠 Kichik admin qo'shish",
                                       callback_data="add_sub_admin"))
        markup.add(
            types.InlineKeyboardButton("❌ Adminlikni olib tashlash",
                                       callback_data="remove_sub_admin"))

    markup.add(
        types.InlineKeyboardButton("💰 Balanslar",
                                   callback_data="view_balances"))
    markup.add(
        types.InlineKeyboardButton("💵 Botning ulushi",
                                   callback_data="view_total_balance"))
    markup.add(
        types.InlineKeyboardButton("🚫 Foydalanuvchini bloklash",
                                   callback_data="block_user"))
    markup.add(
        types.InlineKeyboardButton("✅ Foydalanuvchini blokdan chiqarish",
                                   callback_data="unblock_user"))
    markup.add(
        types.InlineKeyboardButton("📩 Foydalanuvchiga xabar",
                                   callback_data="send_user_message"))
    markup.add(
        types.InlineKeyboardButton("📢 Ommaviy xabar",
                                   callback_data="send_broadcast"))
    markup.add(
        types.InlineKeyboardButton("🔙 Paneldan chiqish",
                                   callback_data="exit_panel"))

    bot.send_message(message.chat.id,
                     "👮 Admin panelga xush kelibsiz!",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "send_user_message")
def send_user_message(call):
    bot.send_message(call.message.chat.id,
                     "✉️ Foydalanuvchi ID sini yuboring:")
    bot.register_next_step_handler(call.message, get_user_message)


def get_user_message(message):
    try:
        user_id = int(message.text)
        bot.send_message(message.chat.id, "📨 Yuboriladigan xabarni kiriting:")
        bot.register_next_step_handler(
            message, lambda msg: send_message_to_user(msg, user_id))
    except ValueError:
        bot.send_message(message.chat.id,
                         "❌ Noto'g'ri ID! Iltimos, faqat raqam kiriting.")


def send_message_to_user(message, user_id):
    try:
        bot.send_message(user_id, message.text)
        bot.send_message(message.chat.id, "✅ Xabar muvaffaqiyatli yuborildi!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik yuz berdi: {str(e)}")


@bot.callback_query_handler(func=lambda call: call.data == "add_sub_admin")
def add_sub_admin(call):
    bot.send_message(call.message.chat.id,
                     "🔢 Kichik adminning ID sini yuboring:")
    bot.register_next_step_handler(call.message, save_sub_admin)


def save_sub_admin(message):
    try:
        sub_admin_id = int(message.text)
        if sub_admin_id not in SUB_ADMINS:
            SUB_ADMINS.append(sub_admin_id)
            save_sub_admins()
            bot.send_message(message.chat.id,
                             f"✅ Kichik admin qo'shildi: {sub_admin_id}")
            bot.send_message(
                sub_admin_id,
                "✅ Siz admin etib tayinlandingiz! \n/panel ustiga bosib panelga kirishingiz mumkin."
            )
        else:
            bot.send_message(
                message.chat.id,
                "⚠️ Bu ID allaqachon kichik adminlar ro'yxatida mavjud!")
    except ValueError:
        bot.send_message(message.chat.id,
                         "❌ Noto'g'ri ID! Iltimos, faqat raqam kiriting.")


@bot.callback_query_handler(func=lambda call: call.data == "remove_sub_admin")
def remove_sub_admin(call):
    bot.send_message(
        call.message.chat.id,
        "🔢 Olib tashlanadigan kichik adminning ID sini yuboring:")
    bot.register_next_step_handler(call.message, delete_sub_admin)


def delete_sub_admin(message):
    try:
        sub_admin_id = int(message.text)
        if sub_admin_id in SUB_ADMINS:
            SUB_ADMINS.remove(sub_admin_id)
            save_sub_admins()
            bot.send_message(message.chat.id,
                             f"❌ Kichik admin o'chirildi: {sub_admin_id}")
        else:
            bot.send_message(message.chat.id,
                             "⚠️ Bu ID kichik adminlar ro'yxatida topilmadi!")
    except ValueError:
        bot.send_message(message.chat.id,
                         "❌ Noto'g'ri ID! Iltimos, faqat raqam kiriting.")


import json

# Kichik adminlar ro'yxatini faylga saqlash
SUB_ADMINS_FILE = "sub_admins.json"


def load_sub_admins():
    try:
        with open(SUB_ADMINS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_sub_admins():
    with open(SUB_ADMINS_FILE, "w") as file:
        json.dump(SUB_ADMINS, file)


SUB_ADMINS = load_sub_admins()


@bot.message_handler(commands=["panel"])
def open_admin_panel(message):
    if message.chat.id not in ADMINS and message.chat.id not in SUB_ADMINS:
        bot.send_message(message.chat.id, "🚫 Siz admin emassiz!")
        return

    markup = types.InlineKeyboardMarkup()

    if message.chat.id in ADMINS:
        markup.add(
            types.InlineKeyboardButton("👥 Foydalanuvchilar",
                                       callback_data="view_users"))
        markup.add(
            types.InlineKeyboardButton("👨‍💻 Fake obunachilar yaratish",
                                       callback_data="create_fake_users"))
        markup.add(
            types.InlineKeyboardButton("📊 Statistika",
                                       callback_data="view_stats"))
        markup.add(
            types.InlineKeyboardButton("📈 Botning statistikasi",
                                       callback_data="view_bot_stats"))
        markup.add(
            types.InlineKeyboardButton("🛠 Kichik admin qo'shish",
                                       callback_data="add_sub_admin"))
        markup.add(
            types.InlineKeyboardButton("❌ Adminlikni olib tashlash",
                                       callback_data="remove_sub_admin"))

    markup.add(
        types.InlineKeyboardButton("💰 Balanslar",
                                   callback_data="view_balances"))
    markup.add(
        types.InlineKeyboardButton("💵 Botning ulushi",
                                   callback_data="view_total_balance"))
    markup.add(
        types.InlineKeyboardButton("🚫 Foydalanuvchini bloklash",
                                   callback_data="block_user"))
    markup.add(
        types.InlineKeyboardButton("✅ Foydalanuvchini blokdan chiqarish",
                                   callback_data="unblock_user"))
    markup.add(
        types.InlineKeyboardButton("📩 Foydalanuvchiga xabar",
                                   callback_data="send_user_message"))
    markup.add(
        types.InlineKeyboardButton("📢 Ommaviy xabar",
                                   callback_data="send_broadcast"))
    markup.add(
        types.InlineKeyboardButton("🔙 Paneldan chiqish",
                                   callback_data="exit_panel"))

    bot.send_message(message.chat.id,
                     "👮 Admin panelga xush kelibsiz!",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "view_bot_stats")
def view_bot_stats(call):
    with open("database.json", "r") as file:
        data = json.load(file)

    total_users = len(data.keys())
    total_balance = sum(user.get("balance", 0) for user in data.values())
    total_rating = sum(user.get("rating", 0) for user in data.values())
    average_rating = round(total_rating /
                           total_users, 2) if total_users > 0 else "Noma'lum"

    bot_share = total_balance / 2
    server_fee = bot_share * 0.15
    admin_share = bot_share * 0.3
    sub_admin_share = bot_share * 0.05

    def format_currency(value):
        if value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f} mlrd so'm"
        elif value >= 1_000_000:
            return f"{value / 1_000_000:.2f} mln so'm"
        else:
            return f"{value:.2f} so'm"

    stats_message = (
        f"📈 *Botning statistikasi:*\n"
        f"👥 Foydalanuvchilar soni: {total_users}\n"
        f"💰 Botning umumiy ulushi: {format_currency(bot_share)}\n"
        f"🖥 Server Fee: {format_currency(server_fee)}\n"
        f"👨‍💼 Admin ulushi: {format_currency(admin_share)}\n"
        f"👨‍💻 Kichik admin ulushi: {format_currency(sub_admin_share)}\n"
        f"⭐ Bot reytingi: {average_rating}")

    bot.send_message(call.message.chat.id,
                     stats_message,
                     parse_mode="Markdown")


# Ma'lumotlar bazasi fayli
DB_FILE = "database.json"


# **JSON'dan foydalanuvchilarni o‘qish**
def read_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# **Ommaviy xabar yuborish**
@bot.callback_query_handler(func=lambda call: call.data == "send_broadcast")
def send_broadcast(call):
    # Adminni xabar yuborish uchun xabar matnini kiritishga chaqiramiz
    msg = bot.send_message(call.message.chat.id,
                           "📢 Ommaviy xabar yuborish uchun xabarni kiriting:")
    bot.register_next_step_handler(msg, process_broadcast)


def process_broadcast(message):
    # Xabar matnini olish
    broadcast_message = message.text.strip()

    # Barcha foydalanuvchilarga xabar yuborish
    data = read_db()  # Foydalanuvchilar ma'lumotlari
    for user_id in data.keys():
        try:
            bot.send_message(user_id,
                             f"📢 Ommaviy xabar:\n\n{broadcast_message}")
        except:
            continue  # Agar xabar yuborishda xatolik yuz bersa, uni o'tkazib yuboradi

    # Adminga xabar yuborish
    bot.send_message(message.chat.id,
                     "✅ Ommaviy xabar barcha foydalanuvchilarga yuborildi!")


@bot.callback_query_handler(
    func=lambda call: call.data == "view_total_balance")
def view_total_balance(call):
    data = read_db()

    total_balance = sum(user.get("balance", 0)
                        for user in data.values())  # Umumiy balansni hisoblash

    bot.send_message(call.message.chat.id,
                     f"💰 *Umumiy balans:* {total_balance:,.2f} so‘m",
                     parse_mode="Markdown")


# **Balanslarni ko‘rish**
@bot.callback_query_handler(func=lambda call: call.data == "view_balances")
def view_balances(call):
    data = read_db()
    if not data:
        bot.send_message(call.message.chat.id,
                         "🚫 Hech qanday foydalanuvchi yo‘q!")
        return

    balance_list = "\n".join([
        f"👤 @{info.get('username', 'Noma’lum')} - 💰 {info.get('balance', 0):,.2f} so‘m"
        for uid, info in data.items()
    ])
    bot.send_message(call.message.chat.id,
                     f"💰 *Foydalanuvchilar balanslari:*\n\n{balance_list}",
                     parse_mode="Markdown")


import sqlite3
import random


def read_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    data = {}
    for row in rows:
        user_id, username, phone_number, balance, rating, last_bonus, blocked, blocked_until = row
        data[str(user_id)] = {
            "username": username,
            "phone_number": phone_number,
            "balance": balance,
            "rating": rating,
            "last_bonus": last_bonus,
            "blocked": blocked,
            "blocked_until": blocked_until
        }
    return data


def write_db(data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for user_id, user_data in data.items():
        cursor.execute(
            '''
            INSERT OR REPLACE INTO users
            (user_id, username, phone_number, balance, rating, last_bonus, blocked, blocked_until)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (int(user_id), user_data.get('username'),
              user_data.get('phone_number'), user_data.get('balance', 0.0),
              user_data.get('rating', 0), user_data.get('last_bonus'),
              user_data.get('blocked', False), user_data.get('blocked_until')))
    conn.commit()
    conn.close()


# **Fake obunachilar yaratish (Hack bo‘limi)**
@bot.callback_query_handler(func=lambda call: call.data == "create_fake_users")
def create_fake_users(call):
    msg = bot.send_message(call.message.chat.id,
                           "🔢 Nechta fake obunachi yaratishni xohlaysiz?")
    bot.register_next_step_handler(msg, process_fake_user_count)


def process_fake_user_count(message):
    try:
        fake_user_count = int(message.text.strip())
        if fake_user_count <= 0:
            bot.send_message(message.chat.id,
                             "❌ Iltimos, 1 dan katta son kiriting.")
            return

        data = read_db()

        # Yangi fake foydalanuvchilarni yaratish
        for _ in range(fake_user_count):
            fake_user_id = str(random.randint(1000000000, 9999999999))

            # ID unikal ekanligini tekshirish
            while fake_user_id in data:
                fake_user_id = str(random.randint(1000000000, 9999999999))

            data[fake_user_id] = {
                "username": f"User{random.randint(1000, 9999)}",
                "phone_number": f"99891{random.randint(1000000, 9999999)}",
                "balance": round(random.uniform(0, 1000), 2),
                "rating": random.randint(10, 100),
                "last_bonus": None,
                "blocked": False,
                "blocked_until": None
            }

        # Ma'lumotlarni bazaga yozish
        write_db(data)
        bot.send_message(message.chat.id,
                         f"✅ {fake_user_count} ta fake obunachi yaratildi!")

    except ValueError:
        bot.send_message(message.chat.id, "❌ Iltimos, son kiriting.")


# **Foydalanuvchini bloklash**
@bot.callback_query_handler(func=lambda call: call.data == "block_user")
def block_user(call):
    msg = bot.send_message(call.message.chat.id,
                           "🚫 Bloklash uchun foydalanuvchi ID sini kiriting:")
    bot.register_next_step_handler(msg, process_block_user)


def process_block_user(message):
    user_id = message.text.strip()
    users = read_db()

    if user_id in users:
        users[user_id]["blocked"] = True
        write_db(users)
        bot.send_message(message.chat.id,
                         f"✅ @{users[user_id]['username']} bloklandi!")
    else:
        bot.send_message(message.chat.id, "❌ Bunday foydalanuvchi topilmadi!")


# **Foydalanuvchini blokdan chiqarish**
@bot.callback_query_handler(func=lambda call: call.data == "unblock_user")
def unblock_user(call):
    msg = bot.send_message(
        call.message.chat.id,
        "✅ Blokdan chiqarish uchun foydalanuvchi ID sini kiriting:")
    bot.register_next_step_handler(msg, process_unblock_user)


def process_unblock_user(message):
    user_id = message.text.strip()
    users = read_db()

    if user_id in users and users[user_id].get("blocked", False):
        users[user_id]["blocked"] = False
        write_db(users)
        bot.send_message(
            message.chat.id,
            f"✅ @{users[user_id]['username']} blokdan chiqarildi!")
    else:
        bot.send_message(
            message.chat.id,
            "❌ Bunday foydalanuvchi topilmadi yoki u bloklangan emas!")


# **Foydalanuvchilar ro‘yxatini ko‘rish**
@bot.callback_query_handler(func=lambda call: call.data == "view_users")
def view_users(call):
    if check_if_blocked(call.from_user.id):
        bot.send_message(call.message.chat.id, "🚫 Siz bloklangansiz!")
        return

    users = read_db()
    if not users:
        bot.answer_callback_query(call.id, "🚫 Hech qanday foydalanuvchi yo‘q!")
        return

    user_list = "\n".join(
        [f"👤 @{users[uid]['username']} (ID: {uid})" for uid in users])
    bot.send_message(call.message.chat.id,
                     f"👥 *Foydalanuvchilar ro‘yxati:*\n\n{user_list}",
                     parse_mode="Markdown")


# **Statistika**
@bot.callback_query_handler(func=lambda call: call.data == "view_stats")
def view_stats(call):
    if check_if_blocked(call.from_user.id):
        bot.send_message(call.message.chat.id, "🚫 Siz bloklangansiz!")
        return

    users = read_db()
    bot.send_message(
        call.message.chat.id,
        f"📊 *Statistika:*\n👥 Umumiy foydalanuvchilar: {len(users)}",
        parse_mode="Markdown")


# **Paneldan chiqish**
@bot.callback_query_handler(func=lambda call: call.data == "exit_panel")
def exit_panel(call):
    bot.send_message(call.message.chat.id,
                     "🔙 *Admin paneldan chiqdingiz.*",
                     parse_mode="Markdown")


DB_FILE = "database.json"


# **Ma'lumotlar bazasini o‘qish**
def read_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
        }  # Agar fayl mavjud bo‘lmasa yoki xato bo‘lsa, bo‘sh lug‘at qaytarish


#Statistika bo‘limi
@bot.callback_query_handler(func=lambda call: call.data == "show_statistics")
def show_statistics(call):
    data = read_db()  # Bazani o‘qish
    user_count = len(data)  # Foydalanuvchilar soni
    current_time = datetime.now().strftime("%H:%M:%S")  # Hozirgi vaqt
    current_date = datetime.now().strftime("%Y-%m-%d")  # Sana

    # Statistika xabari
    stats_message = (f"📊 *Bot statistikasi:*\n\n"
                     f"🕒 *Vaqt:* `{current_time}` (`{current_date}`)\n"
                     f"👥 *Foydalanuvchilar soni:* `{user_count}`\n")

    # **Orqaga qaytish tugmasi**
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 Orqaga", callback_data="show_main_menu"))

    # Xabarni yangilash
    try:
        bot.edit_message_text(stats_message,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup,
                              parse_mode="Markdown")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ Xatolik: {e}")


@bot.callback_query_handler(func=lambda call: call.data == "rating")
def rating_menu(call):
    user_id = call.from_user.id
    data = read_db()

    user = data.get(str(user_id))

    if user:
        # Foydalanuvchilarni balansga qarab tartiblash
        sorted_users = sorted(data.items(),
                              key=lambda x: x[1]["balance"],
                              reverse=True)

        ranking_message = "📊 Reyting:\n\n"
        for idx, (user_id, user_data) in enumerate(
                sorted_users[:10]
        ):  # Eng yuqori 10 ta foydalanuvchini ko‘rsatish
            balance = user_data["balance"]
            # Print user_data to check its structure
            print(user_data
                  )  # This will help you debug the structure of user_data

            # Check if 'user_id' key exists in user_data, otherwise fall back to another key
            user_name = user_data.get(
                "user_id",
                "Unknown")  # Use a fallback key if 'user_id' is not found

            # Formating balance to show in either millions or regular currency
            if balance >= 1_000_000:
                formatted_balance = f"{balance / 1_000_000:.2f} mln"
            else:
                formatted_balance = f"{balance:.2f} so‘m"
            ranking_message += f"{idx + 1}. @{user_name} - {formatted_balance}\n"

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🔙 Orqaga",
                                       callback_data="show_main_menu"))

        bot.edit_message_text(ranking_message,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup)
    else:
        bot.edit_message_text("Siz hali ro‘yxatdan o‘tmagansiz.",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)


DB_FILE = "database.json"


# **Ma'lumotlar bazasini o‘qish**
def read_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# **Ma'lumotlar bazasiga yozish**
def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# **Reyting berish tugmasi**
@bot.callback_query_handler(func=lambda call: call.data == "rate_user")
def rate_user(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=True)
    markup.add("1", "2", "3", "4", "5")

    msg = bot.send_message(
        call.message.chat.id,
        "⭐ Iltimos, reytingni 1 dan 5 gacha raqamda tanlang yoki kiriting:",
        reply_markup=markup)
    bot.register_next_step_handler(msg, process_rating)


# **Reytingni qabul qilish va saqlash**
def process_rating(message):
    try:
        user_id = str(message.from_user.id)
        rating = int(message.text.strip())

        if rating < 1 or rating > 5:
            msg = bot.send_message(
                message.chat.id,
                "❌ Iltimos, 1 dan 5 gacha bo‘lgan raqamni tanlang.")
            bot.register_next_step_handler(msg, process_rating)
            return

        data = read_db()
        if user_id in data:
            data[user_id]["rating"] = rating
            write_db(data)

            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("🔙 Orqaga",
                                           callback_data="show_main_menu"))

            bot.send_message(message.chat.id,
                             f"✅ Sizning reytingingiz {rating} ball bo‘ldi.",
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id,
                             "❌ Siz hali ro‘yxatdan o‘tmagansiz.")
    except ValueError:
        msg = bot.send_message(message.chat.id,
                               "❌ Iltimos, faqat raqam kiriting.")
        bot.register_next_step_handler(msg, process_rating)


from telebot import types, TeleBot

ADMIN_BOT_USERNAME = "Xlv_helpcenterbot"  # Admin botingiz username


@bot.callback_query_handler(func=lambda call: call.data == "contact_admin")
def contact_admin(call):
    bot.send_message(
        call.message.chat.id,
        f"📩 Admin bilan bog‘lanish uchun quyidagi botga yozing:\n\n"
        f"👉 @{ADMIN_BOT_USERNAME}")


bot.polling()


# Reytingni ko‘rsatish
def show_rating(call):
    user_id = call.from_user.id
    data = read_db()

    user = data.get(str(user_id))

    if user:
        rating = user["rating"]
        bot.send_message(
            call.message.chat.id,
            f"⭐️ Sizning reytingingiz: {rating} ball",
        )
    else:
        bot.send_message(
            call.message.chat.id,
            "Siz hali ro‘yxatdan o‘tmadingiz.",
        )


if __name__ == "__main__":
    print("Bot ishga tushdi ...")
    # Botni ishga tushirish
    bot.infinity_polling()
