import asyncio
from logger_setup import logger
from spawnbot import dp, bot
from handlers.main import main_router
from handlers.gpt_handlers.gpt_router import gpt_router
from handlers.gpt_handlers.gpt_settings import gpt_settings
from handlers.gpt_handlers.gpt_router import gpt_router
from handlers.gpt_handlers.gpt_router import gpt_router
from handlers.gpt_handlers.gpt_router import gpt_router
from handlers.error_handler import errors_router


async def main():
    dp.include_routers(main_router,
                       gpt_router,
                       gpt_settings,
                       errors_router)
    logger.info('Bot started.')

    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())

