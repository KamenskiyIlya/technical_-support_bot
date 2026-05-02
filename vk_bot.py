import random

import vk_api as vk
from environs import env
from google.cloud import dialogflow
from vk_api.longpoll import VkEventType, VkLongPoll

from logger_conf import setup_logger

logger = setup_logger(name='vk_bot')


def detect_intent(project_id, session_id, text, language_code='ru'):
    logger.debug(f'Отправляем запрос в Dialogflow: {text}')

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )

    answer = response.query_result.fulfillment_text
    logger.debug(f'Ответ dialogflow: {answer}')

    return answer


def handle_message(user_id, vk_api, text):
    vk_api.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1, 1000),
    )
    logger.info(f'Пользователю {user_id} отправлено сообщение: {text}')


def main():
    env.read_env()
    BOT_TOKEN = env.str('VK_BOT_TOKEN')
    GOOGLE_PROJECT_ID = env.str('GOOGLE_PROJECT_ID')

    logger.info('Авторизация в VK...')
    vk_session = vk.VkApi(token=BOT_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger.info('Авторизация прошла успешно, ожидание новых сообщений')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            user_msg = event.text
            logger.info(
                f'Новое сообщение для меня от пользователя {user_id}: '
                f'{user_msg}'
            )
            try:
                answer = detect_intent(GOOGLE_PROJECT_ID, user_id, user_msg)
                handle_message(user_id, vk_api, answer)
            except Exception as e:
                logger.error(
                    f'Ошибка при обращении к dialogflow: {e}', exc_info=True
                )
                error_msg = (
                    'Произошла ошибка при обработке запроса. Попробуйте позже.'
                )
                handle_message(user_id, vk_api, error_msg)


if __name__ == '__main__':
    main()
