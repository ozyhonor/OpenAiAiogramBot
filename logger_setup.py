import logging
import sys
import asyncio
from pathlib import Path
from logging.handlers import RotatingFileHandler

Path("logs").mkdir(exist_ok=True)


class MaxLevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno <= self.level


logger = logging.getLogger("my_bot")
logger.setLevel(logging.DEBUG)


info_handler = RotatingFileHandler("logs/info.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
info_handler.setLevel(logging.DEBUG)
info_handler.addFilter(MaxLevelFilter(logging.WARNING))
info_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %H:%M:%S'))

error_handler = RotatingFileHandler("logs/error.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s",
                                             datefmt='%d/%m/%Y %H:%M:%S'))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%H:%M:%S'))


logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)


def handle_async_exception(loop, context):
    exception = context.get("exception")
    if exception:
        logger.error("Неотслеживаемая асинхронная ошибка:",
                     exc_info=(type(exception), exception, exception.__traceback__))
    else:
        logger.error("Неотслеживаемая асинхронная ошибка: %s", context["message"])


loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_async_exception)
