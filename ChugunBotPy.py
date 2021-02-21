import telebot
import json

with open('TelegramConfiguration.json', 'r', encoding='utf-8') as tgConfigFile:
    jsonText = json.load(tgConfigFile)

bot = telebot.TeleBot(jsonText['botToken'])
print(jsonText['adminId'])

keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('/about', '/help', '/now')
keyboard.row('/wttr', '/owm', '/cbr', '/ping')
keyboard.row('/mem', '/cpu', '/temp')

@bot.message_handler(commands=['start'])
def send_welcome(message):
         bot.reply_to(message, f'Я бот.\nПриятно познакомиться, {message.from_user.first_name}, {message.from_user.last_name}, {message.from_user.id}, {message.from_user.username}\nПульт управления: /keyboard')

@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.upper()
    chat_id = message.chat.id
    if chat_id == jsonText['adminId']:
        if text == "/KEYBOARD":
            bot.send_message(chat_id, 'Я могу:\nРассказать о себе: /about\nПомощь: /help\n', reply_markup=keyboard)
        elif text == "как дела?":
            bot.send_message(chat_id, 'Хорошо, а у тебя?')
        else:
            bot.send_message(chat_id, 'Не понимаю, что это значит.')

print('Bot start listening...')
bot.polling(none_stop=True)
