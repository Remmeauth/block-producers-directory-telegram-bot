"""
Provide implementation of block producers directory Telegram bot.
"""
import logging
import os

import telebot
from flask import (
    Flask,
    request,
)

from database import create_db_tables

ENVIRONMENT = os.environ.get('ENVIRONMENT')
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
PRODUCTION_HOST = os.environ.get('PRODUCTION_HOST')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@server.route('/' + TOKEN, methods=['POST'])
def get_updates_from_telegram():
    """
    Push updates from Telegram to bot pull.
    """
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode('utf-8'))]
    )

    return '!', 200


@server.route('/')
def web_hook():
    """
    Initialize web-hook for production server.
    """
    bot.remove_webhook()
    bot.set_webhook(url=PRODUCTION_HOST + '/' + TOKEN)

    return '!', 200


if __name__ == '__main__':
    create_db_tables()

    if ENVIRONMENT == 'production':
        server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

    if ENVIRONMENT == 'development':
        bot.polling()
