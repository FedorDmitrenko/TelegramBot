import telebot
import webbrowser
from telebot import types
import sqlite3

# Токен
bot = telebot.TeleBot("6093499792:AAH8hV3zVAMGgee7GnJ4ZU0JVLQp_yKtRuI")
name = None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('itproger.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), pass VARCHAR(50))')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем,введите логин')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()


    conn = sqlite3.connect('itproger.sql')
    cur = conn.cursor()

    cur.execute(f'INSERT INTO users (name, pass) VALUES ("{name}", "{password}")')
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='user'))
    bot.send_message(message.chat.id, 'Вы зарегестрированы !',reply_markup=markup)

    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com')
    markup.row(bt1)
    bt2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    bt3 = types.InlineKeyboardButton('Изменить фото', callback_data='edit')
    markup.row(bt2, bt3)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'Website is open')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'delete')

# Перекидывание на сайт
@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://youtube.com')

# Команда Help
@bot.message_handler(commands=['help', 'Help'])
def help(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')

# Ответ на фото
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com')
    markup.row(bt1)
    bt2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    bt3 = types.InlineKeyboardButton('Изменить фото', callback_data='edit')
    markup.row(bt2,bt3)
    bot.reply_to(message, 'Какое красивое фото!', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data =='delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data  == 'edit':
        bot.edit_message_text('Edit text',callback.message.chat.id, callback.message.message_id)


bot.polling(none_stop=True)