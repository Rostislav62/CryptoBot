import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


# Декоратор для обработки команды /start and help
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am your own bot.")


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = ('Для начала работы бота необходимо ввести команду в формате:\n<currency name>\
            <name of the currency to which you want to convert>\
            <amount of currency transferred> \n For example: \nbitcoin dollar 1 \n'
            'To see a list of available currencies, click: /values'
            )

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'

    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# Декоратор для обработки всех текстовых сообщений
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('To many parametres')
        quote, base, amount = values

        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'User error\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Failed to process command (server error)\n{e}')
    else:
        text = f'Price {amount} {quote} in {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
