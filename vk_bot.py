import random
import signal
from dotenv import dotenv_values

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from tools.diagflow_tools import create_api_key, detect_intent_texts
from tools.common_tools import signal_handler


CLOUD_PROJECT_ID = dotenv_values()['PROJECT_ID']


def echo(event, vk_api):
    text = ''
    try:
        text = detect_intent_texts(
            CLOUD_PROJECT_ID,
            event.user_id,
            event.text,
        )
    except Exception:
        text = 'Произошла ошибка при посылке сообщения сервису.'
    vk_api.messages.send(
        user_id=event.user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


def main():
    signal.signal(signal.SIGINT, signal_handler)

    try:
        create_api_key(CLOUD_PROJECT_ID)

        vk_session = VkApi(token=dotenv_values()['VK_BOT_API_TOKEN'])
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api)

    except Exception as exception:
        print(exception)


if __name__ == '__main__':
    main()
