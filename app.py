#!/usr/bin/env python3

#Сделать веб приложение, на выбранном вами языке, при открытии должно показать кнопку «авторизоваться» по нажатию делает oauth авторизацию ВКонтакте, и показывает имя авторизованного пользователя и 5 любых друзей пользователя. При последующих запусках/заходах на страницу сразу показывает всю информацию т.к. уже понимает, что авторизовано и авторизация запоминается. Бекенд если потребуется, на любой технологии на ваш выбор.
#Результат предоставить в качестве url (или приложения, которое можно установить на мобильное устройство) где можно протестировать работу и в виде исходных кодов в tar.gz архиве на телеграмм @Hrcheck (вопросы сюда же) также указать ссылку на резюме, ожидания по ЗП и графику работы.

import sqlite3

from flask import Flask
from flask import render_template, make_response, redirect
from flask import request

import requests

from db import DB
import config

app = Flask(__name__)

database = DB("users.db")

@app.route('/')
def main_page():
    session_id = request.cookies.get('session_id')
    return render_template('index.html', session_id=session_id)


@app.route('/callback', methods=['GET'])
def get_and_store_token():
    error=None
    if request.method == 'GET':
        payload = {'client_id': config.client_id,
                   'client_secret': config.client_secret,
                   'redirect_uri': config.redirect_uri,
                   'code': request.args.get('code')}
        r = requests.get('https://oauth.vk.com/access_token', params=payload)
        res = r.json()

        if "access_token" in res:
            last_id = database.insert_record(res["access_token"], int(res["expires_in"]))
        else:
            return "Ошибка! Вернитесь назад и попробуйте ещё раз."

        response = make_response(redirect('/'))
        response.set_cookie('session_id', str(last_id))
        return response

    else:
        return "Ошибка! Вернитесь назад и попробуйте ещё раз."
