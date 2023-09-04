# talking_bot

Боты для Vk и Telegram, проводящие общение с сервисом Dialogflow Essentials. Запущенный [бот для telegram](https://t.me/talking_dialogflow_crnrc_bot). Запущенный [бот для vk сообщества](https://vk.com/club218407797).

Примеры работающих ботов:
![Telegram bot example](docs/demo_tg_bot.gif)
![Vk bot example](docs/demo_vk_bot.gif)

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
13. Пройдите все [пункты по подключению API от Dialogflow](https://cloud.google.com/dialogflow/es/docs/quick/setup) на вашем сервере. По итогу при прохождении [последнего шага](https://cloud.google.com/dialogflow/es/docs/quick/setup#client-library-user-account-authentication) на вашем сервере должны быть установлен файл конфигурации для вашего проекта от Dialogflow, обязательно скопируйте абсолютный путь к этому файлу.
14. В файл `.env` добавить строку `GOOGLE_APPLICATION_CREDENTIALS=/path/to/config/.config/gcloud/application_default_credentials.json`, где после равенства укажите путь к конфигурационному файлу, полученному на шаге 13.
15. Создайте апи ключ выполнив команду `python3 tools/dialogflow_tools.py -k`.

## Запуск

Telegram бот: `python3 telegram_bot.py`  
Vk бот: `python3 vk_bot.py`

## Дополнительные опции

Автоматическое создание простых [intents](https://cloud.google.com/dialogflow/es/docs/intents-overview) в Dialogflow по типу вопрос-ответ:
1. Выполните команду `python3 tools/dialogflow_tools.py path/to/questions/file.json`, где `path/to/questions/file.json` - путь до .json файла со следующей структурой (поля `questions` и `answer` могут быть как одной строкой, так и массивом строк):
```json
{
    "intent_name": {
        "questions": [
            "question_1",
            "question_2",
            "question_3",
            ...
            "question_n"
        ],
        "answer": "answer_1"
    },
    ...
}
```

[Пример заполненного файла .json](./examples/questions.json).
