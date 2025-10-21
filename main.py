import os
import telebot
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Send me any Instagram Reel link and I'll download it for you!")

@bot.message_handler(func=lambda message: 'instagram.com/reel/' in message.text)
def download_reel(message):
    url = message.text.strip()
    bot.reply_to(message, "⏳ Downloading your reel... please wait.")
    try:
        ydl_opts = {
            'outtmpl': 'reel.%(ext)s',
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        with open(file_name, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(file_name)
    except Exception as e:
        bot.reply_to(message, f"❌ Failed to download: {e}")

bot.infinity_polling()
