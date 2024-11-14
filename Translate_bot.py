import telebot
from googletrans import Translator

# Bot tokeni - tokeningizni joylashtiring
TOKEN = "7755793322:AAEDdlIlHjnwQF5VHHWl-eVc_zV78sZchOU"

bot = telebot.TeleBot(TOKEN)
translator = Translator()

# Start komandasi va tugmalarni yaratish
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        telebot.types.KeyboardButton("O'zbek tiliga tarjima qilish"),
        telebot.types.KeyboardButton("Ingliz tiliga tarjima qilish")
    )
    bot.send_message(message.chat.id, "Salom! Tanlang qaysi tilga tarjima qilay?", reply_markup=markup)

# Tarjima qilish
@bot.message_handler(func=lambda message: message.text in ["O'zbek tiliga tarjima qilish", "Ingliz tiliga tarjima qilish"])
def choose_language(message):
    target_language = 'uz' if message.text == "O'zbek tiliga tarjima qilish" else 'en'
    bot.send_message(message.chat.id, f"Matnni yuboring, {message.text.split()[0]} tiliga tarjima qilaman.")
    bot.register_next_step_handler(message, lambda m: translate_text(m, target_language))

# Tarjima qilish funksiyasi
def translate_text(message, target_language):
    try:
        translated = translator.translate(message.text, dest=target_language)
        bot.reply_to(message, translated.text)
        send_welcome(message)  # Tarjima tugagach, yana tugmalarni ko'rsatish
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")

# Botni ishga tushirish
bot.polling(none_stop=True)
