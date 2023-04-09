# chatboy
gpt-3.5-turbo [python-telegram-bot](https://docs.python-telegram-bot.org/en/stable/) (in a group chat room) on [Vercel](https://vercel.com/dashboard)

# environment variables
- OPENAI_API_KEY
- TELEGRAM_BOT_TOKEN

# webhook setup
https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url=https://{YOUR_DOMAIN}.vercel.app/callback

# services
- /ai
  - [gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5)
- /image
  - [DALL.E](https://platform.openai.com/docs/models/dall-e)
- /tr
  - [LibreTranslate-py](https://github.com/argosopentech/LibreTranslate-py)
- /fc
  - [Fortune Cookie API](http://yerkee.com/api)
- /fact
  - [HTTP API for useless facts](https://uselessfacts.jsph.pl/)
- /help
  - help
