from aiogram import Router, F
from aiogram.types import Message
from db.database import db
from aiogram.fsm.context import FSMContext
from menu import keyboards, texts
import os
from utility.create_download_link import upload_file_to_gDisk
import shutil
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from states.states import WaitingStateSpeech
from spawnbot import bot
import config_reader
from utility.speech_requests import file_request, openai_audio_request
from logger_setup import logger
from menu.keyboards import SpeechKeyboard, ChatGptKeyboard
from utility.get_size import get_readable_size
from handlers.text_to_speech_gpt.speech_text import go_speech_request
from menu.texts import MainMenuTexts, SpeechTexts, ChatGptTexts
from utility.decode_any_format import detect_file_format
from utility.split_text_for_gpt import split_text
speech_router = Router()

@speech_router.message(F.text == '🎙 Панель')
@speech_router.message(F.text == '🎙 Озвучка')
async def create_gpt_request_for_request(message: Message,state: FSMContext):
    user_id = message.from_user.id
    f_text = '🎙 Озвучка'
    voice = await db.get_user_setting('synthes_voice', user_id)
    rate = await db.get_user_setting('synthes_speed', user_id)


    buttons1 = SpeechKeyboard.create_speech_main()
    await message.answer(f'{MainMenuTexts.future_request_information.format(f_text)}', reply_markup=buttons1)

    buttons2 = SpeechKeyboard.create_inline_speech_settings()
    panel_id = await message.answer(f'{SpeechTexts.synthesis_information.format(rate, voice)}', reply_markup=buttons2)
    panel_id = panel_id.message_id
    await db.update_user_setting('id_speech_panel', panel_id, user_id)
    await state.set_state(WaitingStateSpeech.wait_message_from_user)


@speech_router.message(WaitingStateSpeech.wait_message_from_user)
async def detect_message_from_user(message: Message, state: FSMContext):
    #this detect what send user text or file

    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.full_name

    if message.text:
        if message.text.startswith("/"):
            return
        user_text_request = message.text
        logger.info(f'Пользователь {message.from_user.id} отправил сообщение "{user_text_request}" для генирации картинки')
        await bot.send_chat_action(user_id, 'typing')

        await go_speech_request(message, state)
    elif message.document:
        mime_type = message.document.mime_type
        allowed_mime_types = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # docx
            'text/plain'
        ]
        if mime_type in allowed_mime_types:
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            file_name = message.document.file_name
            file_path = file.file_path
            main_file_name = ['user_files/', message.document.file_name]
            await bot.download_file(file_path, main_file_name[0] + main_file_name[1])
            text = detect_file_format(main_file_name[0] + main_file_name[1])
            logger.info(f'Пользователь {user_name} отправил файл {file_name}, размер файла {get_readable_size(''.join(main_file_name))}')
            if user_id in config_reader.admins_ids:
                chunks = split_text(text, 3500)
                answer = await file_request(chunks, message)
                file_size_bytes = os.path.getsize('user_files/output.mp3')

                file_size_mb = file_size_bytes / (1024 ** 2)
                if file_size_mb > 47:
                    link = await upload_file_to_gDisk('user_files/output.mp3')
                    await message.answer(f'Ваша ссылка на файл: {link}')
                    shutil.rmtree('user_files')
                    os.makedirs('user_files')
                else:
                    audio = FSInputFile(f'user_files/output.mp3')
                    await message.answer(MainMenuTexts.water_mark_omnigpt.format(answer[1]))

                    await bot.send_audio(message.from_user.id, audio=audio)
                    shutil.rmtree('user_files')
                    os.makedirs('user_files')
                return
            quize_markup = ChatGptKeyboard.create_chatgpt_file_inline()
            await bot.send_message(message.chat.id, ChatGptTexts.chatgpt_quize_text.format(file_name),
                                   reply_markup=quize_markup)
            await state.update_data(user_message_with_file=message)
        else:
            await bot.send_message(message.chat.id, "⚠️ Этот тип документа не поддерживается.")
    else:
        await bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте текст или файл")

