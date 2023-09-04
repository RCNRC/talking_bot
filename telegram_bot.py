import logging
import sys
import traceback
from dotenv import dotenv_values
from telegram import Update
import telegram
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
)

from tools.dialogflow_tools import detect_intent_texts, create_api_key
from tools.logger import LogsHandler


CLOUD_PROJECT_ID = dotenv_values()['PROJECT_ID']
LOGGER = logging.getLogger('Telegram bot logger')


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте'
    )


def talk_to_dialogflow(update: Update, context: CallbackContext):
    try:
        text, _ = detect_intent_texts(
            CLOUD_PROJECT_ID,
            update.effective_chat.id,
            update.message.text,
        )
    except Exception as exception:
        text = 'Произошла ошибка при посылке сообщения сервису.'
        LOGGER.error(exception)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
    )


def error_handler(_, context):
    tb_list = traceback.format_exception(
        None,
        context.error,
        context.error.__traceback__,
    )
    tb_string = ''.join(tb_list)
    LOGGER.error(tb_string)


def main():
    LOGGER.setLevel(logging.DEBUG)

    chat_id = dotenv_values()['TELEGRAM_CHAT_ID']
    bot_telegram_logger_api_token = dotenv_values()[
        'TELEGRAM_BOT_LOGGER_API_TOKEN'
    ]
    logger_format = logging.Formatter(
        '%(process)d [%(levelname)s] (%(asctime)s) in %(name)s:\n\n%(message)s'
    )
    handler = LogsHandler(
        bot_telegram_logger_api_token,
        chat_id,
    )
    handler.setFormatter(logger_format)

    LOGGER.addHandler(handler)

    bot_telegramm_api_token = dotenv_values()['TELEGRAM_BOT_API_TOKEN']
    bot = telegram.Bot(token=bot_telegramm_api_token)
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & (~Filters.command), talk_to_dialogflow)
    )
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
