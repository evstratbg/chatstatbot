from telegram import ReplyKeyboardMarkup, ParseMode
from telegram.ext import (
    MessageHandler,
    ConversationHandler,
    Filters,
)

from .main import start
from .error import notify_error
from tools.api import chat_stats
from tools.menu_builder import build_keyboard
from tools.deco import track_stats


@track_stats
def revoke_token(update, context):
    menu = build_keyboard(
        buttons=list(context.user_data['bots_data'].keys()),
        footer_buttons=['Back']
    )

    context.bot.send_message(
        chat_id=update.effective_user.id,
        text='Choose bot\'s username',
        reply_markup=ReplyKeyboardMarkup(menu)
    )
    return 'choose_bot_username'


@track_stats
def choose_bot_username(update, context):
    chat_id = update.effective_user.id
    bot_username = update.message.text

    bot_data = context.user_data['bots_data']
    if bot_username not in bot_data:
        context.bot.send_message(
            chat_id=chat_id,
            text='Choose username on keyboard',
        )
        return

    resp = chat_stats.revoke_token(
        creator_id=chat_id,
        token=bot_data[bot_username]
    )
    if resp.status_code == 500:
        return notify_error(
            bot=context.bot,
            chat_id=chat_id,
            r_json=resp.text
        )

    text = f"Here is the new token for bot @{bot_username}:\n\n"
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text + f"<code>{resp.json()['new_token']}</code>",
        reply_markup=ReplyKeyboardMarkup([['Back']]),
        parse_mode=ParseMode.HTML
    )
    return start(update, context)


def register(dp):
    conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^➖ Revoke token$'), revoke_token),
        ],
        states={
            'choose_bot_username': [
                MessageHandler(Filters.regex('^/start$'), start),
                MessageHandler(Filters.regex('^Back$'), start),
                MessageHandler(Filters.text, choose_bot_username)
            ]
        },
        fallbacks=[],
        allow_reentry=True,
        persistent=True,
        name='revoke_token'
    )
    dp.add_handler(conv)
