import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os # Pertahankan import os untuk membaca variabel sistem Render
import json # Pertahankan import json (walaupun tidak digunakan)

# Token Telegram
TOKEN = "8271976360:AAHnaM_9C3I_oLC-rXvY71tcZ8Lk6zXqXxM"
bot = telebot.TeleBot(TOKEN)

# Hubungkan ke Google Sheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Cek lokasi file rahasia yang ditetapkan Render
# Render akan menempatkan Secret File di /etc/secrets/<filename>
# Atau di root jika kita menggunakan fitur Secret File Render.
# Kita akan gunakan nama file credentials.json
FILE_NAME = "credentials.json"

# Kode asli Anda (diasumsikan file ada)
creds = ServiceAccountCredentials.from_json_keyfile_name(FILE_NAME, scope)
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
