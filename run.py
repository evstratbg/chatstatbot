from pathlib import Path
import logging

from telegram.ext import Updater, PicklePersistence
from telegram.utils.request import Request

from app.handlers import (
    main, error, add_bot, revoke_token
)
from app.bot import MQBot
from settings.config import (
    BOT_TOKEN, IS_DEBUG, BOT_PORT, SSL_CERT, SSL_KEY, BOT_IP, BASE_DIR
)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


def run():
    mqbot = MQBot(
        token=BOT_TOKEN,
        request=Request(connect_timeout=10, con_pool_size=30)
    )
    updater = Updater(
        bot=mqbot,
        use_context=True,
        persistence=PicklePersistence(
            filename=Path(BASE_DIR, 'persistence', 'conversations')
        )
    )
    dp = updater.dispatcher

    add_bot.register(dp)
    revoke_token.register(dp)
    main.register(dp)

    if not IS_DEBUG:
        error.register(dp)
        updater.start_webhook(
            listen='0.0.0.0',
            port=BOT_PORT,
            url_path=BOT_TOKEN,
            key=SSL_KEY,
            cert=SSL_CERT,
            webhook_url=f"https://{BOT_IP}:{BOT_PORT}/{BOT_TOKEN}"
        )
    else:
        updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run()
