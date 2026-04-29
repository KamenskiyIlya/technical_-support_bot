import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(level=logging.DEBUG, name=__name__):

    log_path = Path('logs')
    log_path.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        '%(levelname)s:%(name)s: %(asctime)s | %(message)s'
    )

    file_handler = RotatingFileHandler(
        log_path / 'logs.log',
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8',
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
