from environs import env
from telegram import ForceReply, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from logger_conf import setup_logger

logger = setup_logger()


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        'Здравствуйте!', reply_markup=ForceReply(selective=True)
    )


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main():
    env.read_env()
    BOT_TOKEN = env.str('BOT_TOKEN')

    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo)
    )

    updater.start_polling()
    logger.info('Бот запущен')
    updater.idle()


if __name__ == '__main__':
    main()
