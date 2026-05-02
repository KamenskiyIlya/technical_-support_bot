import random

import vk_api as vk
from environs import env
from vk_api.longpoll import VkEventType, VkLongPoll

from logger_conf import setup_logger

logger = setup_logger(name='vk_bot')


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000),
    )
    logger.info(
        f'Пользователю {event.user_id} отправлено сообщение: {event.text}'
    )


def main():
    env.read_env()
    BOT_TOKEN = env.str('VK_BOT_TOKEN')

    logger.info('Авторизация в VK...')
    vk_session = vk.VkApi(token=BOT_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger.info('Авторизация прошла успешно, ожидание новых сообщений')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            logger.info(
                f'Новое сообщение для меня от пользователя {event.user_id}: '
                f'{event.text}'
            )
            echo(event, vk_api)


if __name__ == '__main__':
    main()
