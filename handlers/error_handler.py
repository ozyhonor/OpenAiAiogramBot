# handlers/error_handler.py

from aiogram import Router
from aiogram.types import Update
from logger_setup import logger

errors_router = Router()

@errors_router.errors()
async def global_error_handler(update: Update) -> bool:
    logger.exception(f"⚠️ Ошибка при обработке апдейта {update}: ")
    return True
