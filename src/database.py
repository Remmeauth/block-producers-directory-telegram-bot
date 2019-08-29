"""
Provide implementation of database for Telegram bot.
"""
import os

import telebot
import psycopg2
import psycopg2.extras

from utils import parse_db_url

logger = telebot.logger

DATABASE_URL = os.environ.get('DATABASE_URL')


def connection_to_db():
    """
    Get connection to the database.
    """
    credentials = parse_db_url(DATABASE_URL)
    connection = psycopg2.connect(**credentials)

    return connection


def create_db_tables():
    """
    Create database tables.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS admins (
        chat_id INTEGER UNIQUE NOT NULL,
        nickname VARCHAR (128) DEFAULT NULL);
        """
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS bp_creation_subscribers (
        chat_id INTEGER UNIQUE NOT NULL,
        nickname VARCHAR (128) DEFAULT NULL);
        """
    )

    connection.commit()


def insert_bp_creation_subscriber(chat_id, nickname):
    """
    Insert block producer subscriber.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO bp_creation_subscribers (chat_id, nickname) "
        "VALUES (%s, %s);", (chat_id, nickname)
    )

    connection.commit()


def check_if_bp_creation_subscriber_exist(chat_id):
    """
    Check if block producer subscriber exists by chat id.
    """
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM bp_creation_subscribers WHERE chat_id={};".format(chat_id))

    if cursor.fetchall():
        return True

    return False


def get_bp_creation_subscribers():
    """
    Get block producer subscribers.
    """
    connection = connection_to_db()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT * FROM bp_creation_subscribers;")
    return cursor.fetchall()


def get_admins():
    """
    Get administrators.
    """
    connection = connection_to_db()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT * FROM admins;")
    return cursor.fetchall()
