import telebot
from config import TOKEN, keys
from utils import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = ('Чтобы начать работу, введите команду боту в следующем формате:\n'
            '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n'
            'Увидеть список всех доступных валют: /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def handle_values(message):
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def handle_text(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров.')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.reply_to(message, text)

bot.polling(none_stop=True)

