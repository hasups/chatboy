import logging
import os
from flask import Flask, request
import openai
import telegram
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler
import json
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_bot_token = str(os.getenv("TELEGRAM_BOT_TOKEN"))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

bot = telegram.Bot(token=telegram_bot_token)

# Set route /callback with POST method will trigger this method.
@app.route('/callback', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'

def reply_handler(bot, update):
    response = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        messages=[{"role": "user", "content": update.message.text}],
        max_tokens=256,
        temperature=0.7
        )
    update.message.reply_text(response['choices'][0]['message']['content'].strip())

#def fortune(update, context):
def fortune(bot, update):
    response = requests.get("http://yerkee.com/api/fortune")
    message = response.json()['fortune']
    #message = googletrans.Translator().translate(response.json()['fortune'], dest='ko').text
    #update.message.reply_text(message)
    update.message.reply_text(message)

dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
dispatcher.add_handler(CommandHandler('fc', fortune))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)
