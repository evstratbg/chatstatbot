from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    MessageHandler,
    Filters,
)

from tools.menu_builder import build_keyboard
from tools.api import chat_stats
from app.handlers.error import notify_error
from tools.deco import track_stats


@track_stats
def start(update, context):
    chat_id = update.effective_user.id
    resp = chat_stats.get_bots(creator_id=chat_id)
    if not resp.ok:
        return notify_error(
            bot=context.bot,
            chat_id=chat_id,
            r_json=resp.text
        )

    bots_data = {}
    for r in resp.json():
        username, token = r['username'], r['token']
        bots_data[username] = token
    context.user_data['bots_data'] = bots_data

    footer_buttons = []
    header_buttons = ['➕ Add bot', ]
    if bots_data:
        footer_buttons.append('Statistics')
        header_buttons.append('➖ Revoke token')

    menu = build_keyboard(
        buttons=list(bots_data.keys()),
        header_buttons=header_buttons,
        footer_buttons=footer_buttons
    )
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text='Choose from menu',
        reply_markup=ReplyKeyboardMarkup(menu)
    )
    return -1


def register(dp):
    dp.add_handler(MessageHandler(Filters.regex('^/start'), start))
