import os
import requests
from dotenv import load_dotenv
import telebot
from telebot import types

url_coin = 'https://api.coingecko.com/api/v3/coins/bitcoin'
load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEAPI'))


@bot.message_handler(commands=['start'])
def welcome_message(message):
    """
    welcome message for user
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #create reply button
    reply_button = types.KeyboardButton('Узнать курс')
    markup.add(reply_button)
    reply = f'Привет, <b>{message.from_user.first_name}</b>. ' \
            'Я бот, который показывает нынешний курс биткоина. Нажми "Узнать курс"'
    bot.send_message(message.chat.id, reply, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def start_bot(message):
    """bot's main function"""
    if message.text == 'Узнать курс':
        markup_inline = types.InlineKeyboardMarkup(row_width=3) #сreate 3 buttons to select currencies
        item1 = types.InlineKeyboardButton('USD', callback_data='usd')
        item2 = types.InlineKeyboardButton('EUR', callback_data='eur')
        item3 = types.InlineKeyboardButton('ETH', callback_data='eth')
        markup_inline.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Выбери валюту:', reply_markup=markup_inline)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю, попробуй нажать кнопку')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    reply = requests.get(url_coin).json()['market_data']['current_price'][call.data]
    try:
        if call.message:
            if call.data == 'usd':
                bot.send_message(call.message.chat.id, f'Курс BTC/{call.data.upper()}: <b>{reply}</b>',
                                 parse_mode='html')
            elif call.data == 'eur':
                bot.send_message(call.message.chat.id, f'Курс BTC/{call.data.upper()}: <b>{reply}</b>',
                                 parse_mode='html')
            elif call.data == 'eth':
                bot.send_message(call.message.chat.id, f'Курс BTC/{call.data.upper()}: <b>{reply}</b>',
                                 parse_mode='html')
    except Exception:
        print(repr(Exception))


# run bot
bot.polling(none_stop=True)
