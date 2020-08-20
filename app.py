#!/usr/bin/env python3

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
    if session_id:
        key = database.get_record_by_id(session_id)
        payload = {'access_token': key[0],
                   'order': 'random',
                   'fields': 'photo_200_orig',
                   'count': 5,
                   'v': 5.122}
        friends = requests.get('https://api.vk.com/method/friends.get',
                               params=payload)
        # friends_json = friends.json()

        payload = {'access_token': key[0],
                   'fields': 'photo_200_orig',
                   'v': 5.122}
        profile = requests.get(
            'https://api.vk.com/method/users.get', params=payload)
        # ["response"])
        return render_template('index.html', session_id=session_id, users=friends.json()["response"]["items"], profile=profile.json()["response"][0])

    return render_template('index.html', session_id=session_id)


@ app.route('/callback', methods=['GET'])
def get_and_store_token():
    error = None
    if request.method == 'GET':
        payload = {'client_id': config.client_id,
                   'client_secret': config.client_secret,
                   'redirect_uri': config.redirect_uri,
                   'code': request.args.get('code')}
        r = requests.get('https://oauth.vk.com/access_token', params=payload)
        res = r.json()

        if "access_token" in res:
            last_id = database.insert_record(
                res["access_token"], int(res["expires_in"]))
        else:
            return "Ошибка! Вернитесь назад и попробуйте ещё раз."

        response = make_response(redirect('/'))
        response.set_cookie('session_id', str(last_id))
        return response

    return "Ошибка! Вернитесь назад и попробуйте ещё раз."
