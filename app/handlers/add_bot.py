from telegram import ReplyKeyboardMarkup, ParseMode
from telegram.ext import (
    MessageHandler,
    ConversationHandler,
    Filters,
)

from .main import start
from .error import notify_error
from tools.api import chat_stats
from tools.deco import track_stats


@track_stats
def add_bot(update, context):
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text='Enter bot\'s username',
        reply_markup=ReplyKeyboardMarkup([['Back']])
    )
    return 'get_bot_username'


@track_stats
def get_bot_username(update, context):
    chat_id = update.effective_user.id
    bot_username = update.message.text
    resp = chat_stats.get_new_token(
        creator_id=chat_id,
        username=bot_username
    )
    if resp.status_code == 422:
        context.bot.send_message(
            chat_id=chat_id,
            text='Sorry, this username is already registered',
            reply_markup=ReplyKeyboardMarkup([['Back']])
        )
    elif resp.status_code == 500:
        return notify_error(
            bot=context.bot,
            chat_id=chat_id,
            r_json=resp.text
        )

    text = f"Here is the token for bot @{bot_username}:\n\n"
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text + f"<code>{resp.json()['token']}</code>",
        reply_markup=ReplyKeyboardMarkup([['Back']]),
        parse_mode=ParseMode.HTML
    )
    return start(update, context)


def register(dp):
    conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^➕ Add bot$'), add_bot),
        ],
        states={
            'get_bot_username': [
                MessageHandler(Filters.regex('^/start$'), start),
                MessageHandler(Filters.regex('^Back$'), start),
                MessageHandler(Filters.text, get_bot_username)
            ]
        },
        fallbacks=[],
        allow_reentry=True,
        persistent=True,
        name='add_bot'
    )
    dp.add_handler(conv)
