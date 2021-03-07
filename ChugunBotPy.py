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
owmToken = config.owmToken

bot = telebot.TeleBot(botToken)

keyboardMarkup = telebot.types.ReplyKeyboardMarkup(True)
keyboardMarkup.row('/about', '/help', '/now', '/paw')
keyboardMarkup.row('/wttr', '/owm', '/cbr', '/ping')
keyboardMarkup.row('/mem', '/cpu', '/temp')


def keyboard(chat_id):
    bot.send_message(
        chat_id,
        'Я могу:\nРассказать о себе: /about\nПомощь: /help\nДоступные команды: /keyboard',
        reply_markup=keyboardMarkup)


def paw():
    response = requests.get(
        f'https://www.pythonanywhere.com/api/v0/user/{config.pawUsername}/cpu/',
        headers={'Authorization': 'Token {token}'.format(token=config.pawToken)})
    msg = ''
    j = response.json()
    if response.status_code == 200:
        msg += f'Dayli CPU limit seconds: {j["daily_cpu_limit_seconds"]}\n' \
               f'Daily cpu total usage seconds: {j["daily_cpu_total_usage_seconds"]}\n' \
               f'Next reset time: {j["next_reset_time"]}\n'
    else:
        msg += 'Got unexpected status code {}: {!r}'.format(response.status_code, response.json())
    return msg


def owm():
#    s_city = 'Moscow,RU'
#    city_id = 524901
    lat = 55.716071
    lon = 37.790835
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/weather',
                           params={'lat': lat, 'lon': lon, 'units': 'metric', 'lang': 'ru', 'APPID': owmToken})
        j_owm = res.json()
        response = f'Осадки:{j_owm["weather"][0]["description"]}\n'
        response += f'Температура:{j_owm["main"]["temp"]}\n'
        response += f'Минимум:{j_owm["main"]["temp_min"]}\n'
        response += f'Максимум:{j_owm["main"]["temp_max"]}\n'
        return response
    except Exception as e:
        return f'"Exception (weather):", {e}'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 f'Я бот.\n' +
                 f'Приятно познакомиться, {message.from_user.first_name}, ' +
                 f'{message.from_user.last_name}, ' +
                 f'{message.from_user.id}, ' +
                 f'{message.from_user.username}\n' +
                 f'Пульт управления: /keyboard')


def about(chat_id):
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
                     reply_markup=keyboardMarkup)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.upper()
    chat_id = message.chat.id
    if chat_id == adminId:
        if text == '/KEYBOARD':
            keyboard(chat_id)
        elif text == '/ABOUT':
            about(chat_id)
        elif text == '/PAW':
            msg = paw()
            bot.send_message(chat_id, msg, reply_markup=keyboardMarkup)
        elif text == '/OWM':
            msg = owm()
            bot.send_message(chat_id, msg, reply_markup=keyboardMarkup)
#"/help', '/now', '/paw', '/wttr', '/owm', '/cbr', '/ping', '/mem', '/cpu', '/temp'"
        else:
            bot.send_message(chat_id, 'Do not understand.')


print('Bot listening...')
bot.polling(none_stop=True)
