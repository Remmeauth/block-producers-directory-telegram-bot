#!/usr/bin/env bash

cd /block-producers-directory-telegram-bot/src && python -c 'from database import create_db_tables; create_db_tables()'
gunicorn app:server -b 0.0.0.0:$PORT
