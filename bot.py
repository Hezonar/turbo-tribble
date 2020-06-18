import config
import telebot
import random
from telebot import types
import Start
import time

bot = telebot.TeleBot(config.API_TOKEN)


@bot.message_handler(commands=['start'])
def start_script(message):
    bot.send_message(message.chat.id, "Скрипт успешно запущен")
    time.sleep(1)
    Start.main(1)


@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, "Долбоеб напиши /start")


if __name__ == "__main__":
    bot.polling(none_stop=True)
