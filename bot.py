# -*- coding: utf-8 -*-
import logging
import os
from flask import Flask, request
import openai
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters

openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_bot_token = str(os.getenv("TELEGRAM_BOT_TOKEN"))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=telegram_bot_token)

@app.route('/callback', methods=['POST'])
def webhook_handler():
    """Set route /callback with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'

def reply_handler(bot, update):
    """Reply message."""
    response = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        messages=[{"role": "user", "content": update.message.text}]
        )
    update.message.reply_text(response['choices'][0]['message']['content'].strip())

# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)
