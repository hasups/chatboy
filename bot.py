import logging
import os
from flask import Flask, request
import openai
import telegram
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

def private_chat(bot, update):
    out = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        messages=[{"role": "user", "content": update.message.text}],
        max_tokens=256,
        temperature=0.7
        )
    update.message.reply_text(out['choices'][0]['message']['content'].strip())

def ai_chat(bot, update):
    prompt_in = ' '.join(update.message.text)
    out = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_in}],
        max_tokens=256,
        temperature=0.7
    )
    #update.message.reply_text(out['choices'][0]['message']['content'].strip())
    bot.send_message(chat_id=update.message.chat_id, text=out['choices'][0]['message']['content'].strip())

def fortune(bot, update):
    out = requests.get("http://yerkee.com/api/fortune")
    update.message.reply_text(out.json()['fortune'].strip())
    

def fact(bot, update):
    out = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random", params={"language": "en"})
    update.message.reply_text(out.json()['text'].strip())
    bot.send_message(chat_id=update.message.chat_id, text="$$$$")


dispatcher = Dispatcher(bot, None)
#dispatcher.add_handler(MessageHandler(Filters.text, private_chat))
dispatcher.add_handler(CommandHandler('a', ai_chat))
dispatcher.add_handler(CommandHandler('fc', fortune))
dispatcher.add_handler(CommandHandler('fact', fact))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)
