import argparse
import json

from environs import env
from google.cloud import dialogflow


def parse_cmd_args():
    parser = argparse.ArgumentParser(
        description='Создание интента в DialodFlow из JSON файла'
    )
    parser.add_argument(
        '--intent_name',
        '-i',
        type=str,
        required=True,
        help='Название интента для создания (из файла)',
    )
    return parser.parse_args()


def create_intent(project_id, display_name, training_phrases, answer):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    prepared_training_phrases = []
    for phrase in training_phrases:
        part = dialogflow.Intent.TrainingPhrase.Part(text=phrase)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        prepared_training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[answer])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=prepared_training_phrases,
        messages=[message],
    )

    response = intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )
    print(f'Интент {display_name} создан')

    return response


def main():
    args = parse_cmd_args()
    env.read_env()

    PROJECT_ID = env.str('PROJECT_ID')
    intent_name = args.intent_name

    with open('db_questions_and_answer.json', 'r', encoding='utf-8') as file:
        database = json.load(file)

    intent_data = database[intent_name]
    training_phrases = intent_data.get('questions', [])
    answer = intent_data.get('answer')
    if not training_phrases or not answer:
        print('Не хватает данных, нет вопросов или ответов')

    create_intent(PROJECT_ID, intent_name, training_phrases, answer)


if __name__ == '__main__':
    main()
