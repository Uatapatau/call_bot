
# -*- coding: utf-8 -*-
#
# Authors:
#   Uatapatau

from telegram import KeyboardButton
from telegram.ext import Updater
from telegram.ext import CommandHandler, ConversationHandler
from telegram.error import (
    TelegramError, BadRequest, TimedOut, NetworkError)
from datetime import datetime
from time import strftime
import logging
import settings
from dialog import main_conversation


def myid_handler(update, context):
    """
    выдаётся идентификатор пользователя Telegram
    """
    message = update.message
    res = "username=@{}, user_id:{}, chat_id={}".format(
        message.from_user.username, message.from_user.id, message.chat_id)
    message.reply_text(text=res)


def fallback_handler(update, context):
    message = update.message if update.message is not None else update.callback_query.message
    message.reply_text(text='Увидимся!')
    return ConversationHandler.END


def start_bot():
    try:
        print('Connecting to telegram')
        updater = Updater(token=settings.BOT_TOKEN, use_context=True)
        print(updater.bot.get_me(timeout=10))
    except Exception as e:
        print(e)
    return updater


def main():
    logging.basicConfig(filename=settings.LOGFILE, level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    settings.updater = start_bot()

    dp = settings.updater.dispatcher
    load_bot = ConversationHandler(
        entry_points=[
            main_conversation('start'),
            CommandHandler('info', myid_handler)
        ],

        states={},

        fallbacks=[
            CommandHandler('cancel', fallback_handler)
        ]
    )

    dp.add_handler(load_bot)

    settings.updater.start_polling(timeout=10)
    settings.updater.idle()


if __name__ == '__main__':
    main()
