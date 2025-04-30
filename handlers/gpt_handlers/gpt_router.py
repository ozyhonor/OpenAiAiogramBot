from aiogram import Router, F
from aiogram.types import Message
from db.database import db
from aiogram.fsm.context import FSMContext
from menu import keyboards, texts
from spawnbot import bot
from menu.texts import ChatGptTexts, MainMenuTexts
from logger_setup import logger
from utility.get_size import get_readable_size
from utility.gpt_requests import solo_request
from states.states import WaitingStateChatGpt
from menu.keyboards import ChatGptKeyboard, MainMenuKeyboard
from handlers.gpt_handlers.gpt_text import go_gpt_text_request, process_file_gpt_request
import config_reader
from utility.gpt_requests import chunks_request

gpt_router = Router()





@gpt_router.message(F.text == '🤖 Панель')
@gpt_router.message(F.text == '🤖 ChatGpt')
async def create_gpt_request_for_request(message: Message, state: FSMContext):
    f_text = "🤖 ChatGpt"
    await state.clear()
    user_id = message.from_user.id
    setting = await db.get_user_setting('chatgpt_settings', user_id)
    degree = await db.get_user_setting('chatgpt_degree', user_id)
    model = await db.get_user_setting('chatgpt_model', user_id)
    tokens = await db.get_user_setting('gpt_tokens', user_id)

    markup_reply = ChatGptKeyboard.create_chatgpt_menu()
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    inline_reply = ChatGptKeyboard.create_gpt_settings(process_bool)

    need_analysis = await db.get_user_setting('postprocess_bool', user_id)
    similarity_threshold = await db.get_user_setting('similarity_threshold', user_id)

    frequency_penalty_gpt = await db.get_user_setting('chatgpt_frequency', user_id)
    reasoning_effort_gpt = await db.get_user_setting('chatgpt_reasoning_effort', user_id)
    presence_penalty_gpt = await db.get_user_setting('chatgpt_presence', user_id)

    new_text_to_panel = ChatGptTexts.settings_request.format(setting,
                                                                          degree,
                                                                          model,
                                                                          tokens,
                                                                          similarity_threshold,
                                                                          presence_penalty_gpt,
                                                                          reasoning_effort_gpt,
                                                                          frequency_penalty_gpt)

    await message.answer(f'{MainMenuTexts.future_request_information.format(f_text)}', reply_markup=markup_reply)
    id_gpt_panel = await message.answer(new_text_to_panel,
                                        reply_markup=inline_reply)
    await state.set_state(WaitingStateChatGpt.wait_message_from_user)
    id_gpt_panel = id_gpt_panel.message_id
    await db.update_user_setting('id_gpt_panel', id_gpt_panel, user_id)


@gpt_router.message(WaitingStateChatGpt.wait_message_from_user)
async def detect_message_from_user(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.full_name

    if message.text:
        if message.text.startswith("/"):
            return
        logger.info(f'Пользователь {message.from_user.id} отправил сообщение для chatgpt')
        await bot.send_chat_action(user_id, 'typing')
        user_text_request = message.text
        await go_gpt_text_request(message)


    elif message.document:
        mime_type = message.document.mime_type
        allowed_mime_types = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # docx
            'text/plain'
        ]
        if mime_type in allowed_mime_types:
            file_id = message.document.file_id
            file = await bot.get_file(file_id)  # получаем объект с file_path

            file_path = file.file_path
            destination_path = f"user_files/{message.document.file_name}"

            await bot.download_file(file_path, destination_path)
            logger.info(f'Пользователь {user_name} отправил файл {file_path}, размер файла {get_readable_size(''.join(destination_path))}' )
            if user_id in config_reader.admins_ids:
                 await process_file_gpt_request(message, state)
                 return
            quize_markup = ChatGptKeyboard.create_chatgpt_file_inline()
            await bot.send_message(message.chat.id, ChatGptTexts.chatgpt_quize_text.format(file_path),reply_markup=quize_markup)
            await state.update_data(user_message_with_file=message)
        else:
            await bot.send_message(message.chat.id, "⚠️ Этот тип документа не поддерживается.")

    else:
        await bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте текст или поддерживаемый документ.")



@gpt_router.message(F.text == '◀️ Назад')
async def go_to_main_menu(message: Message, state: FSMContext):
    markup = MainMenuKeyboard.create_reply_main_menu()
    await message.answer('<b>Главное меню</b>', reply_markup=markup)
    await state.clear()
