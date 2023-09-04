import json
from dotenv import dotenv_values
import argparse

from google.cloud import dialogflow_v2, api_keys_v2
from google.cloud.api_keys_v2 import Key


CLOUD_PROJECT_ID = dotenv_values()['PROJECT_ID']


def initialize_arg_parser():
    parser = argparse.ArgumentParser(
        description='Creates question intents from given json'
        )
    parser.add_argument(
        '-f',
        '--file',
        type=str,
        help='file .json with intets',
    )
    parser.add_argument(
        '-k',
        '--key',
        help='creates dialogflow api key for current environment' +
             ' for project which name set in .env',
        action='store_true',
    )
    return parser


def create_api_key(project_id: str) -> Key:
    """
    Creates and restrict an API key.

    TODO(Developer):
    1. Before running this sample,
      set up ADC as described in
      https://cloud.google.com/docs/authentication/external/set-up-adc
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


def detect_intent_texts(
        project_id,
        session_id,
        text,
        language_code='ru',
        ) -> (str, bool):
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
        request={'session': session, 'query_input': query_input}
    )
    return (response.query_result.fulfillment_text,
            response.query_result.intent.is_fallback)


def create_intent(
        project_id,
        display_name,
        training_phrases_parts: list[str],
        message_texts: list[str],
        language_code='ru'
        ):
    """Create an intent of the given intent type."""

    intents_client = dialogflow_v2.IntentsClient()

    parent = dialogflow_v2.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow_v2.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow_v2.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow_v2.Intent.Message.Text(text=message_texts)
    message = dialogflow_v2.Intent.Message(text=text)

    intent = dialogflow_v2.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    response = intents_client.create_intent(
        request={
            'parent': parent,
            'intent': intent,
            'language_code': language_code,
        },
    )

    print(f'Intent created: {response}')


def get_question_intents(file: str) -> (str, list[str], list[str]):
    with open(file, "r", encoding='utf-8') as file:
        intensts_json = file.read()

    intents = json.loads(intensts_json)
    for name, intent_content in intents.items():
        if not isinstance(intent_content['questions'], list):
            intent_content['questions'] = [intent_content['questions']]
        if not isinstance(intent_content['answer'], list):
            intent_content['answer'] = [intent_content['answer']]

        yield name, intent_content['questions'], intent_content['answer']


def main():
    args = initialize_arg_parser().parse_args()
    if args.file:
        for name, phrases, answers in get_question_intents(args.file):
            create_intent(
                CLOUD_PROJECT_ID,
                name,
                phrases,
                answers,
            )
    elif args.key:
        create_api_key(CLOUD_PROJECT_ID)


if __name__ == '__main__':
    main()
