import logging
import random
import sys
from dotenv import dotenv_values

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from tools.dialogflow_tools import detect_intent_texts
from tools.logger import LogsHandler


CLOUD_PROJECT_ID = dotenv_values()['PROJECT_ID']
LOGGER = logging.getLogger('Vk bot logger')


def talk_to_dialogflow(event, vk_api):
    try:
        text, is_fallback = detect_intent_texts(
            CLOUD_PROJECT_ID,
            event.user_id,
            event.text,
        )
    except Exception as exception:
        text = 'Произошла ошибка при посылке сообщения сервису.'
        LOGGER.exception(exception)
    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=text,
            random_id=random.randint(1, 1000)
        )


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

    try:
        vk_session = VkApi(token=dotenv_values()['VK_BOT_API_TOKEN'])
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                talk_to_dialogflow(event, vk_api)
    except KeyboardInterrupt:
        LOGGER.info('Bot ended work.')
        sys.exit(0)
    except Exception as exception:
        LOGGER.exception(exception)


if __name__ == '__main__':
    main()
