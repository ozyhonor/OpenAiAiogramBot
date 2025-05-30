from aiogram import Router, F
from aiogram.types import Message
from db.database import db
from aiogram.fsm.context import FSMContext
from utility.get_flag_by_code import get_flag_by_code
from menu.keyboards import AudioToTextKeyboard
from states.states import WaitingStateAudioToText
from menu.texts import AudioToText, MainMenuTexts
from logger_setup import logger
from handlers.audio_to_text.synthesis_file import go_synthesis_file_request

audio_tt_router = Router()

@audio_tt_router.message(F.text == '📝 Панель')
@audio_tt_router.message(F.text == '📝 Аудио в текст')
async def create_synthesis_request_for_request(message: Message, state: FSMContext):
    user_id = message.from_user.id

    language = await db.get_user_setting('synthesis_language', user_id)
    format = await db.get_user_setting('synthesis_response_format', user_id)
    flag = await get_flag_by_code(language)
    markup = AudioToTextKeyboard.create_synthesis_main()
    f_text = '📝 Аудио в текст'
    markup_inline = AudioToTextKeyboard.create_inline_synthesis_settings()
    await message.answer(f'{MainMenuTexts.future_request_information.format(f_text)}', reply_markup=markup)
    text = AudioToText.synthesis_panel.format(language, flag, format)

    id_picture_panel = await message.answer(text, reply_markup=markup_inline)
    id_picture_panel = id_picture_panel.message_id
    await db.update_user_setting('id_synthesis_panel', id_picture_panel, user_id)
    await state.set_state(WaitingStateAudioToText.wait_message_from_user)


@audio_tt_router.message(WaitingStateAudioToText.wait_message_from_user)
async def detect_message_from_user(message: Message, state: FSMContext):
    #this detect what send user text or file
    logger.info(message.text)
    logger.info(message.content_type)
    await go_synthesis_file_request(message, state)



