import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Token Telegram
TOKEN = "8271976360:AAHnaM_9C3I_oLC-rXvY71tcZ8Lk6zXqXxM"
bot = telebot.TeleBot(TOKEN)

# Hubungkan ke Google Sheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# PENTING: KODE INI MENCARI FILE LOKAL BERNAMA "credentials.json"
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("pendaftaran smada run 2025").sheet1

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Halo! Silakan kirim nama kamu untuk pendaftaran Smada Run.")

@bot.message_handler(func=lambda msg: True)
def daftar(message):
    nama = message.text
    # Menyimpan nama dan username ke Google Sheet
    sheet.append_row([nama, message.from_user.username])
    bot.reply_to(message, f"Terima kasih {nama}! Data kamu sudah tercatat.")

print("Bot berjalan...")
bot.infinity_polling()
