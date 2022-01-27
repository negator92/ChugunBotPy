#! /usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import platform
import uuid
from datetime import datetime
import requests
import telebot


class Configuration(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)


tg_config = 'TelegramConfiguration.json'

with open(tg_config, 'r', encoding='utf-8') as tgConfigFile:
    data = tgConfigFile.read()

config = Configuration(data)


def update_config():
    with open(tg_config, 'r', encoding='utf-8') as tgConfFile:
        d = tgConfFile.read()
    c = Configuration(d)
    config.botToken = c.botToken
    config.adminId = c.adminId
    config.owmToken = c.owmToken
    config.pawUsername = c.pawUsername
    config.pawToken = c.pawToken
    config.lon = c.lon
    config.lat = c.lat
    config.cgImageURL = c.cgImageURL


bot = telebot.TeleBot(config.botToken)

keyboardMarkup = telebot.types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False)
keyboardMarkup.row('/about', '/help', '/paw')
keyboardMarkup.row('/wttr', '/owm', '/cbr')
keyboardMarkup.row('/cgimage', '/2gis')


def keyboard(chat_id):
    bot.send_message(
        chat_id,
        'Я могу:\nРассказать о себе: /about\nПомощь: /help\nДоступные команды: /keyboard',
        reply_markup=keyboardMarkup, parse_mode='markdown')


def paw(chat_id):
    try:
        response = requests.get(
            f'https://www.pythonanywhere.com/api/v0/user/{config.pawUsername}/cpu/',
            headers={'Authorization': 'Token {token}'.format(token=config.pawToken)})
        if response.status_code == 200:
            j_paw = response.json()
            msg = f'Dayli CPU limit seconds: *{j_paw["daily_cpu_limit_seconds"]}*\n' \
                  f'Daily cpu total usage seconds: *{j_paw["daily_cpu_total_usage_seconds"]}*\n' \
                  f'Next reset time: *{j_paw["next_reset_time"]}*\n'
            bot.send_message(
                chat_id, msg, reply_markup=keyboardMarkup, parse_mode='markdown')
        else:
            msg = 'Got unexpected status code {}: {!r}'.format(
                response.status_code, response.json())
            bot.send_message(
                chat_id, msg, reply_markup=keyboardMarkup, parse_mode='markdown')
    except Exception as e:
        msg = f'Exception: {e}'
        bot.send_message(
            chat_id, msg, reply_markup=keyboardMarkup, parse_mode='markdown')


def owm(chat_id, lat=config.lat, lon=config.lon):
    #    s_city = 'Moscow,RU'
    #    city_id = 524901
    # keyboard.add(types.KeyboardButton(text="Запросить геолокацию", request_lon=True))
    # keybd = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    # button_ = telebot.types.KeyboardButton(text="Отправить местоположение", request_lon=True)
    # keybd.add(button_)
    try:
        response = requests.get('http://api.openweathermap.org/data/2.5/weather',
                                params={
                                    'lat': lat,
                                    'lon': lon,
                                    'units': 'metric',
                                    'lang': 'ru',
                                    'appId': config.owmToken})
        if response.status_code == 200:
            j_owm = response.json()
            msg = f'Погода в *{j_owm["sys"]["country"]} {j_owm["name"]}*:\n' \
                  f'Температура: *{j_owm["main"]["temp"]}*\n' \
                  f'Ощущается как: *{j_owm["main"]["feels_like"]}*\n' \
                  f'Осадки: *{j_owm["weather"][0]["description"]}*\n' \
                  f'Влажность: *{j_owm["main"]["humidity"]}%*\n' \
                  f'Давление: *{round(j_owm["main"]["pressure"] * 0.75006375541921)}mmHg*\n' \
                  f'Ветер: *{j_owm["wind"]["speed"]}м/с*\n' \
                  f'Облачность: *{j_owm["clouds"]["all"]}%*\n' \
                  f'Восход: *{datetime.utcfromtimestamp(int(j_owm["sys"]["sunrise"]) + int(j_owm["timezone"])).strftime("%H:%M:%S")}*\n' \
                  f'Закат: *{datetime.utcfromtimestamp(int(j_owm["sys"]["sunset"]) + int(j_owm["timezone"])).strftime("%H:%M:%S")}*'
            bot.send_message(
                chat_id, msg, reply_markup=keyboardMarkup, parse_mode='markdown')
        else:
            msg = 'Got unexpected status code {}: {!r}'.format(
                response.status_code, response.json())
            bot.send_message(
                chat_id, msg, reply_markup=keyboardMarkup, parse_mode='markdown')
    except Exception as e:
        msg = f'Exception: {e}'
        bot.send_message(
            chat_id, msg, reply_markup=keyboardMarkup, parse_mode='markdown')


def about(chat_id):
    msg = f'{platform.machine.__name__}: {platform.machine()}\n' \
          f'{platform.node.__name__}: {platform.node()}\n' \
          f'{platform.platform.__name__}: {platform.platform()}\n' \
          f'{platform.processor.__name__}: {platform.processor()}\n' \
          f'{platform.python_build.__name__}: {platform.python_build()}\n' \
          f'{platform.python_branch.__name__}: {platform.python_branch()}\n' \
          f'{platform.python_compiler.__name__}: {platform.python_compiler()}\n' \
          f'{platform.python_implementation.__name__}: {platform.python_implementation()}\n' \
          f'{platform.python_revision.__name__}: {platform.python_revision()}\n' \
          f'{platform.python_version.__name__}: {platform.python_version()}\n' \
          f'{platform.python_version_tuple.__name__}: {platform.python_version_tuple()}\n' \
          f'{platform.release.__name__}: {platform.release()}\n' \
          f'{platform.system.__name__}: {platform.system()}\n' \
          f'{platform.uname.__name__}: {platform.uname()}\n' \
          f'{platform.version.__name__}: {platform.version()}\n' \
          f'{platform.win32_edition.__name__}: {platform.win32_edition()}\n' \
          f'{platform.win32_is_iot.__name__}: {platform.win32_is_iot()}\n' \
          f'{platform.win32_ver.__name__}: {platform.win32_ver()}\n' \
          f'{platform._mac_ver_xml.__name__}: {platform._mac_ver_xml()}'
    bot.send_message(
        chat_id,
        msg,
        reply_markup=keyboardMarkup)


def bot_help(chat_id):
    msg = 'Use /keyboard to see all availiable commands.'
    bot.send_message(chat_id, msg, reply_markup=keyboardMarkup,
                     parse_mode='markdown')


def wttr_by_city(chat_id, city, lang='ru'):
    try:
        url = f'http://wttr.in/{city}_Mmtp_lang={lang}.png'
        response = requests.get(url)
        if response.status_code == 200:
            guid = uuid.uuid4()
            with open(f'./{guid}.png', 'wb') as f:
                f.write(response.content)
            bot.send_photo(chat_id, photo=open(f'./{guid}.png', 'rb'), reply_markup=keyboardMarkup,
                           parse_mode='markdown')
            os.remove(f'./{guid}.png')
        else:
            msg = 'Got unexpected status code {}: {!r}'.format(
                response.status_code, response.json())
            bot.send_message(
                chat_id, msg, reply_markup=keyboardMarkup, parse_mode='markdown')
    except Exception as e:
        bot.send_message(
            chat_id, f'Exception: {e}', reply_markup=keyboardMarkup, parse_mode='markdown')


def wttr_by_lon(chat_id, latitude=config.lat, longitude=config.lon, lang='ru'):
    try:
        url = f'http://wttr.in/{latitude}%2C{longitude}_Mmtp_lang={lang}.png'
        response = requests.get(url)
        if response.status_code == 200:
            guid = uuid.uuid4()
            with open(f'./{guid}.png', 'wb') as f:
                f.write(response.content)
            bot.send_photo(chat_id, photo=open(f'./{guid}.png', 'rb'), reply_markup=keyboardMarkup,
                           parse_mode='markdown')
            os.remove(f'./{guid}.png')
        else:
            msg = 'Got unexpected status code {}: {!r}'.format(
                response.status_code, response.json())
            bot.send_message(
                chat_id, msg, reply_markup=keyboardMarkup, parse_mode='markdown')
    except Exception as e:
        bot.send_message(
            chat_id, f'Exception: {e}', reply_markup=keyboardMarkup, parse_mode='markdown')


def cbr(chat_id, value1, value2):
    try:
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = requests.get(url)
        if response.status_code == 200:
            j_cbr = response.json()
            msg = f'*{j_cbr["Valute"][value1]["Name"]}*:\n' \
                  f'сегодня *{j_cbr["Valute"][value1]["Value"]}* рублей,\n' \
                  f'но было *{j_cbr["Valute"][value1]["Previous"]}* рублей'
            if value2 == 'EUR':
                msg += f'\n*{j_cbr["Valute"][value2]["Name"]}*:\n' \
                  f'сегодня *{j_cbr["Valute"][value2]["Value"]}* рублей,\n' \
                  f'но было *{j_cbr["Valute"][value2]["Previous"]}* рублей'
            keyboardMarkupCBR = telebot.types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True)
            keyboardMarkupCBR.row('/cbr USD', '/cbr EUR', '/keyboard')
            bot.send_message(
                chat_id, msg, reply_markup=keyboardMarkupCBR, parse_mode='markdown')
        else:
            msg = 'Got unexpected status code {}: {!r}'.format(
                response.status_code, response.json())
            bot.send_message(
                chat_id, msg, reply_markup=keyboardMarkup, parse_mode='markdown')
    except Exception as e:
        bot.send_message(
            chat_id, f'Exception: {e}', reply_markup=keyboardMarkup, parse_mode='markdown')


def doubleGisStatic(chat_id, lattitude=config.lat, longtitude=config.lon):
    try:
        url = f'https://static.maps.2gis.com/1.0?s=1200x675&c={lattitude},{longtitude}&z=16'
        response = requests.get(url)
        if response.status_code == 200:
            guid = uuid.uuid4()
            with open(f'./{guid}.png', 'wb') as f:
                f.write(response.content)
            bot.send_photo(chat_id, photo=open(f'./{guid}.png', 'rb'), reply_markup=keyboardMarkup,
                           parse_mode='markdown')
            os.remove(f'./{guid}.png')
        else:
            msg = 'Got unexpected status code {}: {!r}'.format(
                response.status_code, response.json())
            bot.send_message(
                chat_id, msg, reply_markup=keyboardMarkup, parse_mode='markdown')
    except Exception as e:
        bot.send_message(
            chat_id, f'Exception: {e}', reply_markup=keyboardMarkup, parse_mode='markdown')


def cgiImage(chat_id, cgImageURL):
    try:
        response = requests.get(cgImageURL)
        if response.status_code == 200:
            guid = uuid.uuid4()
            with open(f'./{guid}.jpg', 'wb') as f:
                f.write(response.content)
            bot.send_photo(chat_id, photo=open(f'./{guid}.jpg', 'rb'), reply_markup=keyboardMarkup,
                           parse_mode='markdown')
            os.remove(f'./{guid}.jpg')
        else:
            msg = 'Got unexpected status code {}: {!r}'.format(
                response.status_code, response.json())
            bot.send_message(
                chat_id, msg, reply_markup=keyboardMarkup, parse_mode='markdown')
    except Exception as e:
        bot.send_message(
            chat_id, f'Exception: {e}', reply_markup=keyboardMarkup, parse_mode='markdown')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 f'Я бот.\n' +
                 f'Приятно познакомиться, \n'
                 f'First name: *{message.from_user.first_name}*, \n' +
                 f'Last name: *{message.from_user.last_name}*, \n' +
                 f'User id: *{message.from_user.id}*, \n' +
                 f'Username: *{message.from_user.username}*\n' +
                 f'Пульт управления: /keyboard',
                 reply_markup=keyboardMarkup,
                 parse_mode='markdown')


# @bot.message_handler(commands=['geo'])
# def geo(message):
#    chat_id = message.chat.id
#    if chat_id == adminId:
#        keybd = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#        button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_lon=True)
#        keybd.add(button_geo)
#        bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keybd)


@bot.message_handler(content_types=['location'])
def lon(message):
    chat_id = message.chat.id
    if chat_id == config.adminId:
        try:
            lat = config.lat = message.location.latitude
            lon = config.lon = message.location.longitude
            with open(tg_config, 'w', encoding='utf-8') as f:
                json.dump(config.__dict__, f, ensure_ascii=False, indent=4)
            update_config()
            config.lat = lat
            config.lon = lon
            wttr_by_lon(chat_id, lat, lon)
            owm(chat_id, lat, lon)
            doubleGisStatic(chat_id, lat, lon)
        except Exception as e:
            bot.send_message(chat_id,
                             f'Exception: {e}',
                             reply_markup=keyboardMarkup,
                             parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.split()[0].upper()
    chat_id = message.chat.id
    if chat_id == config.adminId:
        if text == '/KEYBOARD':
            keyboard(chat_id)
        elif text == '/ABOUT':
            about(chat_id)
        elif text == '/PAW':
            paw(chat_id)
        elif text == '/OWM':
            owm(chat_id)
        elif text == '/HELP':
            bot_help(chat_id)
        elif text == '/WTTR':
            parts = len(message.text.split())
            if parts == 1:
                wttr_by_lon(chat_id)
            if parts == 2:
                wttr_by_city(chat_id, message.text.split()[1].upper())
            if parts == 3:
                wttr_by_lon(chat_id, message.text.split()[1].upper(), message.text.split()[2].upper())
        elif text == '/CBR':
            if len(message.text.split()) > 1:
                cbr(chat_id, message.text.split()[1].upper(), '')
            else:
                cbr(chat_id, 'USD', 'EUR')
        elif text == '/CGIMAGE':
            if len(message.text.split()) > 1:
                cgiImage(chat_id, message.text.split()[1].lower())
            else:
                cgiImage(chat_id, config.cgImageURL)
        elif text == '/2GIS':
            doubleGisStatic(chat_id)
        else:
            bot.send_message(chat_id, 'Do not understand.')


# wttr_by_lon(config.adminId)
# owm(config.adminId)
# cbr(config.adminId, 'USD', 'EUR')
# paw(config.adminId)
# cgiImage(config.adminId, config.cgImageURL)

print('Bot listening...')
bot.polling(none_stop=True)
