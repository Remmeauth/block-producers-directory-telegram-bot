Block producers directory Telegram bot.

## Development

Clone the project with the following command:

```bash
$ git clone https://github.com/Remmeauth/block-producers-directory-telegram-bot.git
$ cd block-producers-directory-telegram-bot
```

To build the project, use the following command:

```bash
$ docker build -t block-producers-directory-telegram-bot . -f Dockerfile.development
```

To run the project, use the following command. It will start the server and occupate current terminal session:

```bash
$ docker run -v $PWD:/block-producers-directory-telegram-bot \
      -e ENVIRONMENT=development \
      -e TELEGRAM_BOT_TOKEN='918231803:AAHLN7w1xg82ziHzI3Pgb0NnG0pAFErFS2Q' \
      -e DATABASE_URL='postgres://vtlavnrs:C1y8UMym4YCHMk7Mw26MfX9nGzUOmq2i@raja.db.elephantsql.com:5432/vtlavnrs' \
      --name block-producers-directory-telegram-bot block-producers-directory-telegram-bot
```

If you need to enter the bash of the container, use the following command:

```bash
$ docker exec -it block-producers-directory-telegram-bot bash
```

Clean all containers with the following command:

```bash
$ docker rm $(docker ps -a -q) -f
```

Clean all images with the following command:

```bash
$ docker rmi $(docker images -q) -f
```

## Production


Clone the project with the following command:

```bash
$ git clone https://github.com/Remmeauth/block-producers-directory-telegram-bot.git
$ cd block-producers-directory-telegram-bot
```

To build the project, use the following command:

```bash
$ docker build -t block-producers-directory-telegram-bot . -f Dockerfile.production
```

To run the project, use the following command. It will start the server and occupate current terminal session:

```bash
$ docker run -p 8000:8000 -e PORT=8000 -v $PWD:/block-producers-directory-telegram-bot \
      -e ENVIRONMENT=production \
      -e TELEGRAM_BOT_TOKEN='918231803:AAHLN7w1xg82ziHzI3Pgb0NnG0pAFErFS2Q' \
      -e DATABASE_URL='postgres://vtlavnrs:C1y8UMym4YCHMk7Mw26MfX9nGzUOmq2i@raja.db.elephantsql.com:5432/vtlavnrs' \
      -e PRODUCTION_HOST='https://bps-directory-telebot-staging.herokuapp.com' \
      --name block-producers-directory-telegram-bot block-producers-directory-telegram-bot
```