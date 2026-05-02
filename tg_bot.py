from environs import env
from google.cloud import dialogflow
from telegram import ForceReply, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from logger_conf import setup_logger

logger = setup_logger(name='tg_bot')


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


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    logger.info(f'Пользователь {user.id} (@{user.username}) запустил бота')
    update.message.reply_text(
        'Здравствуйте! Я бот технической поддержки издательства "Игра глаголов". '
        'Задайте мне интересующий Вас вопрос, и я постараюсь помочь.',
        reply_markup=ForceReply(selective=True),
    )


def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_text = update.message.text

    logger.info(f'От пользователя {user_id} получено сообщение: {user_text}')

    project_id = context.bot_data.get('PROJECT_ID')

    try:
        session_id = user_id
        answer = detect_intent(project_id, session_id, user_text)

        update.message.reply_text(answer)
        logger.info(f'Бот ответил пользователю {user_id}: {answer}')
    except Exception as e:
        logger.error(f'Ошибка при обращении к dialogflow: {e}', exc_info=True)
        update.message.reply_text(
            'Прошу произошла ошибка при обработке запроса. Попробуйте позже.'
        )


def main():
    env.read_env()
    BOT_TOKEN = env.str('TG_BOT_TOKEN')
    PROJECT_ID = env.str('PROJECT_ID')

    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['PROJECT_ID'] = PROJECT_ID

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_message)
    )

    updater.start_polling()
    logger.info('Бот запущен. Для его отключения нажмите Ctrl+C')
    updater.idle()


if __name__ == '__main__':
    main()
