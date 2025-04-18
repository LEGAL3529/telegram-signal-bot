import telebot
import pandas as pd
import time

API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(API_TOKEN)

# Простая стратегия: если цена выше SMA — BUY, ниже — SELL
def generate_signal(price_series):
    sma = price_series.rolling(window=5).mean()
    if price_series.iloc[-1] > sma.iloc[-1]:
        return "BUY"
    elif price_series.iloc[-1] < sma.iloc[-1]:
        return "SELL"
    else:
        return "HOLD"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "📈 Welcome! Send /signal to get the latest trade signal.")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    try:
        df = pd.read_csv("data/sample_data.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        signal = generate_signal(df['close'])
        bot.reply_to(message, f"📊 Current Signal: {signal}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

bot.polling()