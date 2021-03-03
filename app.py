from flask import Flask, request
import telegram
from emotiond.credentials import bot_token, bot_user_name,URL
import re

global bot
global TOKEN
TOKEN =  bot_token

bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def init():
    incoming_text = telegram.Update.de_json(request.get_json(force = True), bot)
    
    chat_id = incoming_text.message.chat_id
    msg_id = incoming_text.message.message_id

    
    text = incoming_text.message.text
    if text != None:
        text = incoming_text.message.text.encode('utf-8').decode()
    else:
        text = "segment.com"
    if text == "init":
        hello = """Hello,
        I am emotiond,
        At your service.
        """
        bot.sendMessage(
        chat_id = chat_id,
        text = hello, 
        reply_to_message_id = msg_id
        )

    else:
        try:
            #clean received text to remove non-alphabets
            text = re.sub(r"\W", "_", text)
            #api for fetching from cool avatars
            url = "https://api.hello-avatar.com/adorables/{}".format(text.strip())

            bot.sendPhoto(
               chat_id = chat_id,
               photo = url, 
               reply_to_message_id = msg_id 
            )
        except Exception:
             bot.sendMessage(
                chat_id = chat_id,
                text = "hello systemd, help me out", 
                reply_to_message_id = msg_id
        )
    return 'ok'

@app.route('/star', methods = ['GET', 'POST'])
def set_webhook():
    hooky = bot.setWebhook('{URL}{HOOK}'.format(URL = URL, HOOK = TOKEN))

    if hooky:
        return "webhook ok"
    else:
        return "webhook !ok"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)