import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json # Tambahkan import json untuk parsing kredensial

# Token Telegram (Token Anda dari file asli)
[span_3](start_span)TOKEN = "8271976360:AAHnaM_9C3I_oLC-rXvY71tcZ8Lk6zXqXxM"[span_3](end_span)
bot = telebot.TeleBot(TOKEN)

# Hubungkan ke Google Sheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# --- BAGIAN PENTING: MEMUAT KREDENSIAL DARI VARIABEL LINGKUNGAN ---
# Cek apakah variabel lingkungan GOOGLE_CREDENTIALS tersedia
creds_json = os.environ.get('GOOGLE_CREDENTIALS')

if creds_json:
    # Memuat kredensial dari JSON string (digunakan saat deployment di Render)
    print("Memuat kredensial dari Variabel Lingkungan...")
    try:
        creds_info = json.loads(creds_json)
        # Menggunakan from_json_keyfile_dict untuk memuat dari dictionary Python
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    except Exception as e:
        print(f"ERROR: Gagal memuat kredensial dari variabel lingkungan: {e}")
        # Jika gagal, aplikasi mungkin akan crash, atau coba fallback (opsional)
        raise
else:
    # Fallback ke file credentials.json (digunakan saat testing lokal)
    print("WARNING: Variabel lingkungan GOOGLE_CREDENTIALS tidak ditemukan. Mencoba memuat dari file credentials.json...")
    # Menggunakan dari file seperti kode asli Anda
    try:
        [span_4](start_span)creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)[span_4](end_span)
    except FileNotFoundError:
        print("ERROR: credentials.json tidak ditemukan. Autentikasi gagal.")
        raise

client = gspread.authorize(creds)
# Membuka Google Sheet Anda
[span_5](start_span)sheet = client.open("pendaftaran smada run 2025").sheet1[span_5](end_span)

@bot.message_handler(commands=['start'])
def start(message):
    [span_6](start_span)bot.reply_to(message, "Halo! Silakan kirim nama kamu untuk pendaftaran Smada Run.")[span_6](end_span)

@bot.message_handler(func=lambda msg: True)
def daftar(message):
    nama = message.text
    # Menyimpan nama dan username ke Google Sheet
    [span_7](start_span)sheet.append_row([nama, message.from_user.username])[span_7](end_span)
    [span_8](start_span)bot.reply_to(message, f"Terima kasih {nama}! Data kamu sudah tercatat.")[span_8](end_span)

[span_9](start_span)print("Bot berjalan...")[span_9](end_span)
[span_10](start_span)bot.infinity_polling()[span_10](end_span)
