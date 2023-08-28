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
from google.cloud import dialogflow_v2, api_keys_v2
from google.cloud.api_keys_v2 import Key


CLOUD_PROJECT_ID = dotenv_values()['PROJECT_ID']


def create_api_key(project_id: str) -> Key:
    """
    Creates and restrict an API key. Add the suffix for uniqueness.

    TODO(Developer):
    1. Before running this sample,
      set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    2. Make sure you have the necessary permission to create API keys.

    Args:
        project_id: Google Cloud project id.

    Returns:
        response: Returns the created API Key.
    """
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = 'My first API key'

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f'projects/{project_id}/locations/global'
    request.key = key

    response = client.create_key(request=request).result()

    print(f'Successfully created an API key: {response.name}\n'
          f'key string: {response.key_string}')

    return response


def detect_intent_texts(project_id, session_id, text, language_code='ru'):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation.
    """

    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow_v2.TextInput(
        text=text,
        language_code=language_code,
    )
    query_input = dialogflow_v2.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


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
