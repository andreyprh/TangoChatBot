import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger('tango_bot')
    logger.setLevel(logging.DEBUG)

    # Создаем обработчик для записи логов в файл
    file_handler = RotatingFileHandler('tango_bot.log', maxBytes=5242880, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    # Создаем обработчик для вывода логов в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Создаем форматтер и добавляем его в обработчики
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики в логгер
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger