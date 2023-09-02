from dotenv import dotenv_values

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType


def main():
    vk_session = VkApi(token=dotenv_values()['VK_BOT_API_TOKEN'])
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    main()
