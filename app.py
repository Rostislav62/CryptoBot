import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


# Decorator for processing the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = ('Hello!\n'
            'I am a bot assistant in currency conversion.\n'
            '\nTo get instructions, click: /help\n'
            '\nTo see a list of available currencies, click: /values'
            )
    bot.reply_to(message, text)


# Decorator for processing the /help command
@bot.message_handler(commands=['help'])
def help_(message: telebot.types.Message):
    text = ('Hello!\n'
            '\nTo get the exchange rate of two currencies relative to each other you must:\n'
            'enter the name of the currency whose price you want to know (base currency),\n'
            'enter the name of the currency in which you want to know the price of the first currency '
            '(quote currency), separated by a space,\n'
            'and the amount of the first currency, separated by a space.\n'
            '\n<base currency> <quote currency> <amount of base currency> \n'
            '\nFor example:\n '
            'bitcoin dollar 1'
            '\nTo see a list of available currencies, click: /values'
            )

    bot.reply_to(message, text)


# Decorator for processing the /values command
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'

    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# Decorator to handle all text messages
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        currencies_and_amount = message.text.split(' ')
        quote, base, amount = currencies_and_amount
        total_base = CryptoConverter.get_price(quote, base, amount)

        if len(currencies_and_amount) != 3:
            raise ConvertionException('To many parameters')

    except ConvertionException as e:
        bot.reply_to(message, f'User error\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Failed to process command (server error)\n{e}')
    else:
        val_total = float(total_base) * float(amount)
        text = f'Price of {amount} {quote} in {base} = {val_total}'
        bot.send_message(message.chat.id, text)


bot.polling()
