import vk_api
from environs import env
from vk_api.longpoll import VkEventType, VkLongPoll

from logger_conf import setup_logger

logger = setup_logger(name='vk_bot')


def main():
    env.read_env()
    BOT_TOKEN = env.str('VK_BOT_TOKEN')

    logger.info('Авторизация в VK...')
    session = vk_api.VkApi(token=BOT_TOKEN)
    longpoll = VkLongPoll(session)
    logger.info('Авторизация прошла успешно, ожидание новых сообщений')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            logger.info('Новое сообщение:')
            if event.to_me:
                logger.info(f'Для меня от: {event.user_id}')
            else:
                logger.info(f'От меня для: {event.user_id}')
            logger.info(f'Текст: {event.text}')


if __name__ == '__main__':
    main()
