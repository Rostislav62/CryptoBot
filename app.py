import telebot

# Токен, который вы получили от BotFather
TOKEN = '7160813775:AAEMBRCqmujyumtZTXTwEEswcPGLNu7iOdY'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler()
def echo_test(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Hello man!')

keys ={
    'bitcoin': 'BTC',
    'efirium': 'ETH',
    'dollar': 'USD'
}
# Декоратор для обработки команды /start and help
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am FatherBot.")
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = ('Для начала работы бота необходимо ввести команду в формате:\n<currency name> \
            <name of the currency to which you want to convert> \
            <amount of currency transferred> \n Чтобы увидеть список доступных валют нажмите /values'
            )
    text1 = 'For example:'
    text2 = 'bitcoin dollar 1'

    bot.reply_to(message, text)
    bot.reply_to(message, text1)
    bot.reply_to(message, text2)


# Декоратор для обработки команды /values
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text= 'Available currencies:'

    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


#
# # Декоратор для обработки всех текстовых сообщений
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


# Запуск бота
bot.polling()
