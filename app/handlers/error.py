import json
import traceback
import logging

logger = logging.getLogger(__name__)


def error(update, context):
    logger.error(traceback.format_exc())
    context.bot.send_message(
        text=json.dumps(update.to_dict(), ensure_ascii=False),
        chat_id=56631662,
    )
    context.bot.send_message(
        text=str(traceback.format_exc()[-4000:]),
        chat_id=56631662,
    )


def notify_error(bot, chat_id, r_json):
    bot.send_message(
        text=json.dumps(r_json, ensure_ascii=False),
        chat_id=56631662,
    )
    bot.send_message(
        chat_id=chat_id,
        text='Ooops, something went wrong with API'
    )


def register(dp):
    dp.add_error_handler(error)
