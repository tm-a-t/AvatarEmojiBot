import logging
import os

from dotenv import load_dotenv

from app.bot import Bot
from app.handlers.handlers import handlers

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]', level=logging.INFO)

load_dotenv()
api_id, api_hash = int(os.environ['API_ID']), os.environ['API_HASH']
token = os.environ['BOT_TOKEN']

bot = Bot('bot', api_id, api_hash)
handlers.apply(bot)


def run():
    bot.run(token)
