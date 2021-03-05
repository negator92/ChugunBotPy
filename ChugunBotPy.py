#! /usr/bin/python3
# -*- coding: utf-8 -*-

import json
import platform
import requests
import telebot

class Configuration(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

with open('TelegramConfiguration.json', 'r', encoding='utf-8') as tgConfigFile:
    data = tgConfigFile.read()

config = Configuration(data)

botToken = config.botToken
adminId = int(config.adminId)

bot = telebot.TeleBot(botToken)

keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row("/about", "/help", "/now", "/paw")
keyboard.row("/wttr", "/owm", "/cbr", "/ping")
keyboard.row("/mem", "/cpu", "/temp")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот.\n' +
                          f'Приятно познакомиться, {message.from_user.first_name}, {message.from_user.last_name}, {message.from_user.id}, {message.from_user.username}\n' +
                          f'Пульт управления: /keyboard')


@bot.message_handler(content_types=["text"])
def text_handler(message):
    text = message.text.upper()
    chat_id = message.chat.id
    if chat_id == adminId:
        if text == '/KEYBOARD':
            bot.send_message(
                chat_id,
                "Я могу:\nРассказать о себе: /about\nПомощь: /help\nДоступные команды: /keyboard",
                reply_markup=keyboard)
        elif text == '/PAW':
            response = requests.get(
                'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(username=config.pawUsername),
                headers={'Authorization': 'Token {token}'.format(token=config.pawToken)}
            )
            jResponse = response.json()
            msg = ''
            if response.status_code == 200:
                msg += f'{response.content}'
            else:
                msg += 'Got unexpected status code {}: {!r}'.format(response.status_code, response.json())
            bot.send_message(
                chat_id, msg, reply_markup=keyboard)
        elif text == '/OWM':
            s_city = "Moscow,RU"
            city_id = 524901
            lat = 55.716071
            lon = 37.790835
            owmtoken = config.owmToken
            response = ''
            try:
                res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                   params={'lat': lat,'lon': lon, 'units': 'metric', 'lang': 'ru', 'APPID': owmtoken})
                data = res.json()
                response += f'Осадки:{data["weather"][0]["description"]}\n'
                response += f'Температура:{data["main"]["temp"]}\n'
                response += f'Минимум:{data["main"]["temp_min"]}\n'
                response += f'Максимум:{data["main"]["temp_max"]}\n'
            except Exception as e:
                response += "Exception (weather):", e
                pass
            bot.send_message(chat_id, response, reply_markup=keyboard)
        elif text == '/ABOUT':
            bot.send_message(chat_id,
                             f'{platform.machine.__name__}: {platform.machine()}\n' +
                             f'{platform.node.__name__}: {platform.node()}\n' +
                             f'{platform.platform.__name__}: {platform.platform()}\n' +
                             f'{platform.processor.__name__}: {platform.processor()}\n' +
                             f'{platform.python_build.__name__}: {platform.python_build()}\n' +
                             f'{platform.python_branch.__name__}: {platform.python_branch()}\n' +
                             f'{platform.python_compiler.__name__}: {platform.python_compiler()}\n' +
                             f'{platform.python_implementation.__name__}: {platform.python_implementation()}\n' +
                             f'{platform.python_revision.__name__}: {platform.python_revision()}' +
                             f'{platform.python_version.__name__}: {platform.python_version()}\n' +
                             f'{platform.python_version_tuple.__name__}: {platform.python_version_tuple()}\n' +
                             f'{platform.release.__name__}: {platform.release()}\n' +
                             f'{platform.system.__name__}: {platform.system()}\n' +
                             f'{platform.uname.__name__}: {platform.uname()}\n' +
                             f'{platform.version.__name__}: {platform.version()}\n' +
                             f'{platform.win32_edition.__name__}: {platform.win32_edition()}\n' +
                             f'{platform.win32_is_iot.__name__}: {platform.win32_is_iot()}\n' +
                             f'{platform.win32_ver.__name__}: {platform.win32_ver()}\n' +
                             f'{platform._mac_ver_xml.__name__}: {platform._mac_ver_xml()}',
                             reply_markup=keyboard)
        elif text == 'как дела?':
            bot.send_message(chat_id, "Хорошо, а у тебя?")
        else:
            bot.send_message(chat_id, "Не понимаю, что это значит.")

print("Bot listening...")
bot.polling(none_stop=True)