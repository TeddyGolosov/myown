# -*- coding: utf-8 -*-
import flask
import os
import telebot
import urllib.request
import urllib.parse
from urllib.parse import quote

TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN, threaded=False)


bot.remove_webhook()

bot.set_webhook(url="https://radiant-stream-78940.herokuapp.com/bot")

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Доброго времени суток, уважаемый собеседник! Я бот, который занимается дистрибутивной семантикой. \n Я могу определять ближайших соседей для слов, которые ты введёшь. Для этого тебе нужно будет ввести слово, а я найду его во всех корпусах!  \n Если ты напишешь слово, которое может быть начальной формой для нескольких слов, то мы выдадим тебе все варианты. Если тебе нужно только одно слово, то нужно прописать тэги! Например, '_NOUN'. Их список можно найти на этом сайте: http://universaldependencies.org/u/pos/all.html'")


@bot.message_handler(content_types=['text'])
def send_len(message):
    word = message.text
    corp = ['news', 'ruscorpora', 'ruwikiruscorpora', 'web']
    answ = ''
    for crp in corp:
        req = urllib.request.Request('http://rusvectores.org/'+ crp +'/{0}/api/csv'.format(quote(word)))
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        answ = answ + html + '\n'
    bot.send_message(message.chat.id, answ)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route("/bot", methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
