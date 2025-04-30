import asyncio
from logger_setup import logger
from spawnbot import dp, bot
from handlers.main import main_router
from handlers.gpt_handlers.gpt_router import gpt_router
from handlers.gpt_handlers.gpt_settings import gpt_settings
from handlers.gpt_handlers.gpt_router import gpt_router
from handlers.picture_generation.picture_text import picture_text
from handlers.picture_generation.picture_settings import picture_settings
from handlers.picture_generation.picture_router import picture_router
from handlers.gpt_handlers.gpt_router import gpt_router
from handlers.error_handler import errors_router
from handlers.audio_to_text.audio_to_text_router import audio_tt_router
from handlers.audio_to_text.audio_tt_settings import audio_tt_settings
from handlers.text_to_speech_gpt.speech_router import speech_router
from handlers.text_to_speech_gpt.speech_settings import speech_settings_router
async def main():
    dp.include_routers(main_router,
                       gpt_router,
                       gpt_settings,
                       picture_router,
                       picture_settings,
                       picture_text,
                       audio_tt_router,
                       errors_router,
                       audio_tt_settings,
                       speech_router,
                       )
    logger.info('Bot started.')

    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())

