# talking_bot

Боты для Vk и Telegram, проводящие общение с сервисом Dialogflow Essentials.

## Установка и подготовка

Требуется [Python](https://www.python.org/downloads/) версии 3.7 или выше и установленный [pip](https://pip.pypa.io/en/stable/getting-started/).

1. Скачайте репозиторий.
2. Установите необходимые зависимости:  
   - Для Unix/macOs:`python -m pip install -r requirements.txt`
   - Для Windows:`py -m pip install --destination-directory DIR -r requirements.txt`
3. В корне репозитория создайте пустой файл `.env`
4. Создайте нового телеграмм бота у [BotFather](https://telegram.me/BotFather). По итогу вы должны получить `token` от нового бота.
5. В файл `.env` добавить строку `TELEGRAM_BOT_API_TOKEN=token`, где `token` - полученный на шаге 6 токен от [BotFather](https://telegram.me/BotFather).
6. Создайте [сообщество](https://vk.com/groups?tab=admin) в Vk или получите к нему права администратора. Убедитесь что у сообщества установлено разрешение на сообщения.
7. В файл `.env` добавить строку `VK_BOT_API_TOKEN=token`, где `token` - ключ доступа сообщества, у которого должны быть разрешения на "управление сообществом" и "сообщения сообщества".
8. Создайте нового телеграмм бота для логгирования у [BotFather](https://telegram.me/BotFather). По итогу вы должны получить `token` от нового бота.
9.  В файл `.env` добавить строку `TELEGRAM_BOT_LOGGER_API_TOKEN=token`, где `token` - полученный на шаге 9 токен от [BotFather](https://telegram.me/BotFather).
10. В файл `.env` добавить строку `TELEGRAM_CHAT_ID=id`, где `id` - "id" в телеграмме, куда бот логгер будет отправлять возникающе ошибки. 
   - Если не знаете ваш "id", воспользуйтесь специальным [ботом](https://telegram.me/userinfobot).
11. Создайте [проект Dialogflow](https://dialogflow.cloud.google.com/#/getStarted). По итогу вы должны получить ID проекта `project_id`.
12. В файл `.env` добавить строку `PROJECT_ID=project_id`, где `project_id` - ID проекта, полученный на шаге 11.
13. Пройдите все [пункты по подключению API от Dialogflow](https://cloud.google.com/dialogflow/es/docs/quick/setup) на вашем сервере. По итогу на вашем сервере должны быть установлен файл конфигурации для вашего проекта от Dialogflow, обязательно скопируйте абсолютный путь к этому файлу.
14. В файл `.env` добавить строку `GOOGLE_APPLICATION_CREDENTIALS=/path/to/config/.config/gcloud/application_default_credentials.json`, где после равенства укажите путь к конфигурационному файлу, полученному на шаге 13.

## Запуск

Telegram бот: `python3 telegram_bot.py`  
Vk бот: `python3 vk_bot.py`
