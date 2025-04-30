import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import telegram_token
from middlewears.access import AccessMiddleware

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Dispatcher

storage = MemoryStorage()
bot = Bot(token=telegram_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)
print(asyncio.run(bot.me()
dp.message.middleware(AccessMiddleware())
