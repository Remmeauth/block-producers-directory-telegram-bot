"""
Provide implementation of database for Telegram bot.
"""
import os

import psycopg2

from utils import parse_db_url

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

    connection.commit()
