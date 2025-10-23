import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json 

# Token Telegram
TOKEN = "8271976360:AAHnaM_9C3I_oLC-rXvY71tcZ8Lk6zXqXxM"
bot = telebot.TeleBot(TOKEN)

# Hubungkan ke Google Sheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# --- Memuat Kredensial dari Variabel Lingkungan ---
creds_json = os.environ.get('GOOGLE_CREDENTIALS')

if creds_json:
    # Memuat kredensial dari JSON string (saat deployment di Render)
    print("Memuat kredensial dari Variabel Lingkungan...")
    try:
        creds_info = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    except Exception as e:
        print(f"ERROR: Gagal memuat kredensial dari variabel lingkungan: {e}")
        # Hentikan eksekusi jika gagal
        raise
else:
    # Fallback ke file credentials.json (saat testing lokal)
    print("WARNING: Variabel lingkungan GOOGLE_CREDENTIALS tidak ditemukan. Mencoba memuat dari file credentials.json...")
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    except FileNotFoundError:
        print("ERROR: credentials.json tidak ditemukan. Autentikasi gagal.")
        raise

client = gspread.authorize(creds)
# Membuka Google Sheet Anda
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
