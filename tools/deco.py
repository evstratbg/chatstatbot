import functools

from chatstats.sync_api import SyncChatStats

chat_stats = SyncChatStats(url='http://localhost:8000', token='531326ab-eb15-45fa-b163-2f010bfc66be')


def track_stats(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        update, context = args
        if not update.effective_user:
            return

        uid = update.effective_user.id
        text = update.effective_message.text
        username = update.effective_user.username
        first_name = update.effective_user.first_name
        last_name = update.effective_user.last_name
        language_code = update.effective_user.language_code
        is_bot = update.effective_user.is_bot

        r = chat_stats.new_event(
            event_name=text,
            user_id=uid,
            user_first_name=first_name,
            user_last_name=last_name,
            user_username=username,
            user_language_code=language_code,
            is_bot=is_bot
        )
        print(r.text)
        return func(*args, **kwargs)

    return decorator
