import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get('TOKEN')  
SPEACKERGROUP = os.environ.get('SPEACKERGROUP')  
URLCHAT = os.environ.get('URLCHAT')
URLSITE = os.environ.get('URLSITE')
AFTERPARTY = os.environ.get('AFTERPARTY')

bot = telebot.TeleBot(TOKEN)       


# Клавиатуры для пользователя
keyboardStart = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardCancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardRedirect = types.InlineKeyboardMarkup()
keyboardGoIt = types.InlineKeyboardMarkup()
keyboardGoAffter = types.InlineKeyboardMarkup()

# Кнопки на клавиатурах
btnQuestion = types.KeyboardButton("📢 Задать вопрос спикеру")
btnOrder = types.KeyboardButton("🆘 Обратиться за помощью")
btnGoIt = types.KeyboardButton("🦾 Стать Айтишником")
btnAffter = types.KeyboardButton("🍾 AfterParty")
btnCancel = types.KeyboardButton("🚫 Отменить")
btnGroup = types.InlineKeyboardButton(text="Чат с поддержкой", url=URLCHAT)
btnIt = types.InlineKeyboardButton(text="Наш сайт", url=URLSITE)
btnLinkAfter = types.InlineKeyboardButton(text="Регистрация на AfterParty", url=AFTERPARTY)

keyboardStart.row(btnQuestion)
keyboardStart.row(btnOrder)
keyboardStart.row(btnGoIt)
keyboardStart.row(btnAffter)
keyboardCancel.add(btnCancel)
keyboardRedirect.add(btnGroup)
keyboardGoIt.add(btnIt)
keyboardGoAffter.add(btnLinkAfter)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "{0}, рад приветствовать Вас на конференции!🥳".format(message.from_user.first_name))
    bot.send_message(message.from_user.id, "Сделайте выбор с помощью кнопок внизу☺", reply_markup=keyboardStart)

@bot.message_handler(content_types=['text'])
def getMessages(message):
    if message.text == "📢 Задать вопрос спикеру":
        bot.send_message(message.from_user.id, "Напишите мне свой вопрос и я отправлю его спикеру", reply_markup=keyboardCancel)
        bot.register_next_step_handler(message, sendQuestion) 
    elif message.text == "🆘 Обратиться за помощью":
        bot.send_message(message.from_user.id, "Прошу вас перейти по ссылке ниже:", reply_markup=keyboardRedirect)

    elif message.text == "🦾 Стать Айтишником":
        bot.send_message(message.from_user.id, "Присоединяйся к нам!", reply_markup=keyboardGoIt)
    elif message.text == "🍾 AfterParty":
        bot.send_message(message.from_user.id, "Проведи вечер с нами!", reply_markup=keyboardGoAffter)
    else:
        bot.send_message(message.from_user.id, "Извините, я Вас не понимаю... Воспользуйтесь кнопками", reply_markup=keyboardStart)

def sendQuestion(message):
    """Отправка сообщения в канал спикеров"""
    if message.text == "🚫 Отменить":
        """Если пользователь передумал отправлять сообщение в канал"""
        bot.send_message(message.from_user.id, "Дайте знать если еще что то понадобится", reply_markup=keyboardStart)
        bot.register_next_step_handler(message, getMessages)
    else:
        """Отправка и зануление переменных"""
        user_message = f'Вопрос от {message.from_user.username}:\n{message.text}\nСсылка на его TG: https://t.me/{message.from_user.username}'
        bot.send_message(SPEACKERGROUP, user_message)
        bot.send_message(message.from_user.id, "Ваше сообщение отправлено спикеру", reply_markup=keyboardStart)
        bot.register_next_step_handler(message, getMessages)



if __name__ == '__main__':
    print('Run bot ....')
    bot.infinity_polling()
