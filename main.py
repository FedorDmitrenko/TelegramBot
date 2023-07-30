import telebot
import webbrowser
#Токен
bot = telebot.TeleBot("6093499792:AAH8hV3zVAMGgee7GnJ4ZU0JVLQp_yKtRuI")
#старт
@bot.message_handler(commands=['start', 'main', 'hello'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')

#Перекидывание на сайт
@bot.message_handler(commands=['site', 'website'])
def site (message):
    webbrowser.open('https://youtube.com')



#Комманда Help
@bot.message_handler(commands=['help','Help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')

#Ответ на фото
@bot.message_handler(content_types='photo')
def get_photo(message):
    bot.reply_to(message, 'Какое красивое фото !')

bot.polling(none_stop=True)