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
        dispatcher.process_update(update)
    return 'ok'


def bot_chat(bot, update):
    out = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        messages=[{"role": "user", "content": update.message.text}],
        max_tokens=256,
        temperature=0.7
        )
    bot.send_message(chat_id=update.message.chat_id, text=out['choices'][0]['message']['content'].strip())


def bot_help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="/ai, /image, /tr en|ko, /fact, /fc, /help")


def ai_chat(bot, update, args):
    prompt_in = ' '.join(args)
    out = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_in}],
        max_tokens=256,
        temperature=0.7
    )
    bot.send_message(chat_id=update.message.chat_id, text=out['choices'][0]['message']['content'].strip())


def ai_image(bot, update, args):
    prompt_in = ' '.join(args)
    out = openai.Image.create(
      prompt = prompt_in,
      n=1,
      size="512x512",
      response_format="url"
    )
    json_object = json.loads(str(out))
    bot.send_photo(chat_id=update.message.chat_id, photo=json_object['data'][0]['url'])

"""
def bot_trans(bot, update, args):
    prompt_in = ' '.join(args[1:])
    message = googletrans.Translator().translate(prompt_in, dest=args[0]).text.strip()
    bot.send_message(chat_id=update.message.chat_id, text=message)
    bot.send_message(chat_id=update.message.chat_id, text="under construction")
"""

def fortune(bot, update):
    out = requests.get("http://yerkee.com/api/fortune")
    bot.send_message(chat_id=update.message.chat_id, text=out.json()['fortune'].strip())


def fact(bot, update):
    out = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random", params={"language": "en"})
    bot.send_message(chat_id=update.message.chat_id, text=out.json()['text'].strip())


dispatcher = Dispatcher(bot, None)
#dispatcher.add_handler(MessageHandler(Filters.text, bot_chat))
dispatcher.add_handler(CommandHandler('help', bot_help))
dispatcher.add_handler(CommandHandler('ai', ai_chat, pass_args=True))
dispatcher.add_handler(CommandHandler('image', ai_image, pass_args=True))
#dispatcher.add_handler(CommandHandler('tr', bot_trans, pass_args=True))
dispatcher.add_handler(CommandHandler('fc', fortune))
dispatcher.add_handler(CommandHandler('fact', fact))


if __name__ == "__main__":
    # Running server
    app.run(debug=True)
