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

circled_bullet = '⦿'
white_circle = '○'


@track_stats
def stats(update, context):
    menu = build_keyboard(
        buttons=list(context.user_data['bots_data'].keys()),
        footer_buttons=['Back']
    )

    context.bot.send_message(
        chat_id=update.effective_user.id,
        text='Choose bot\'s username',
        reply_markup=ReplyKeyboardMarkup(menu)
    )
    return 'stats_bot_username'


@track_stats
def stats_bot_username(update, context):
    chat_id = update.effective_user.id
    bot_username = update.message.text

    bot_data = context.user_data['bots_data']
    if bot_username not in bot_data:
        context.bot.send_message(
            chat_id=chat_id,
            text='Choose username on keyboard',
        )
        return

    context.user_data['current_username'] = bot_username

    menu = build_keyboard(
        header_buttons=[
            f'{circled_bullet}Day', f'{white_circle}Week', f'{white_circle}Month'
        ],
        buttons=[
            '🙎 Users', '👣 Sessions', '🏃 New users', '✨ Top events',
            '👫 Sex'
        ],
        footer_buttons=['Back']
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
            MessageHandler(Filters.regex('^Statistics$'), track_stats),
        ],
        states={
            'stats_bot_username': [
                MessageHandler(Filters.regex('^/start$'), start),
                MessageHandler(Filters.regex('^Back$'), start),
                MessageHandler(Filters.text, stats_bot_username)
            ]
        },
        fallbacks=[],
        allow_reentry=True,
        persistent=True,
        name='revoke_token'
    )
    dp.add_handler(conv)
