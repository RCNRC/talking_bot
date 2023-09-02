import signal
import sys
from dotenv import dotenv_values
from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
)

from diagflow_tools import detect_intent_texts, create_api_key


CLOUD_PROJECT_ID = dotenv_values()['PROJECT_ID']


def signal_handler(sig, frame):
    print('Bot stoped')
    sys.exit(0)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте'
    )


def echo(update: Update, context: CallbackContext):
    text = ''
    try:
        text = detect_intent_texts(
            CLOUD_PROJECT_ID,
            update.effective_chat.id,
            update.message.text,
        )
    except Exception:
        text = 'Произошла ошибка при посылке сообщения сервису.'
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
    )


def main():
    signal.signal(signal.SIGINT, signal_handler)

    try:
        create_api_key(CLOUD_PROJECT_ID)

        bot_telegramm_api_token = dotenv_values()['TELEGRAM_BOT_API_TOKEN']
        updater = Updater(token=bot_telegramm_api_token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(
            MessageHandler(Filters.text & (~Filters.command), echo)
        )

        updater.start_polling()
    except Exception as exception:
        print(exception)


if __name__ == '__main__':
    main()
