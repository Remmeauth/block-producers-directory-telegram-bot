"""
Provide implementation of block producers directory Telegram bot.
"""
import logging
import os

import telebot
from flask import (
    Flask,
    jsonify,
    request,
)

from database import (
    check_if_bp_creation_subscriber_exist,
    create_db_tables,
    insert_bp_creation_subscriber,
    get_admins,
    get_bp_creation_subscribers,
)

ENVIRONMENT = os.environ.get('ENVIRONMENT')
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
PRODUCTION_HOST = os.environ.get('PRODUCTION_HOST')

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


def render_main_keyboard(message):
    """
    Render main keyboard.
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Subscribe to new block producers')
    bot.send_message(message.from_user.id, 'Choose one of the the following keyboard buttons:', reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    """
    Start command.
    """
    render_main_keyboard(message)


@bot.message_handler(func=lambda message: message.text == 'Subscribe to new block producers', content_types=['text'])
def handle_bp_creation_subscribing_button(message):
    """
    Handle user's request to check address tokens balance.
    """
    if not check_if_bp_creation_subscriber_exist(chat_id=message.chat.id):
        insert_bp_creation_subscriber(chat_id=message.chat.id, nickname=message.from_user.username)
        bot.send_message(message.chat.id, 'You have been subscribed to new block producers.')
        return

    bot.send_message(message.chat.id, 'You are already subscribed to new block producers.')


@server.route('/subscribers/block-producer/creation')
def get_block_producer_creation_subscribers():
    """
    Get list of block producer subscribers.
    """
    subscribers = get_bp_creation_subscribers()

    if not subscribers:
        return jsonify({'result': []})

    return jsonify({'result': subscribers})


@server.route('/administrators')
def get_administrators():
    """
    Get list of administrators.
    """
    administrators = get_admins()

    if not administrators:
        return jsonify({'result': []})

    return jsonify({'result': administrators})


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
