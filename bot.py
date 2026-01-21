import os
import telebot
from flask import Flask

app = Flask(__name__)

TOKEN = "8589389763:AAGECiVQ5kIibPaVlDFiV1_DvqH3mC9e3x0"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Теперь ты можешь получать коды с сайта!")

@app.route('/')
def home():
    return "🤖 Бот работает"

def run_bot():
    print("Бот запущен...")
    bot.polling(non_stop=True)

if __name__ == '__main__':
    from threading import Thread
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)