import traceback
from aiogram.types.input_file import FSInputFile
import os
from aiogram import Router, F
from aiogram.types import Message
from utility.remove_similar_sentences import remove_similar_sentences
from db.database import db
from aiogram.fsm.context import FSMContext
from states.states import WaitingStateChatGpt
from utility.decode_any_format import TYPE_TXT_FILE
from spawnbot import bot
from menu import texts
from utility.decode_any_format import detect_file_format
from utility.latex_to_unicode import convert_latex_to_unicode
import re
from datetime import datetime
from utility.gpt_requests import solo_request
from utility.split_text_for_gpt import split_text
from utility.gpt_requests import chunks_request
from menu.texts import MainMenuTexts


gpt_text = Router()

def safe_remove(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Файл {file_path} удалён.")
        else:
            print(f"Файл {file_path} не существует.")
    except Exception as e:
        print(f"Не удалось удалить файл {file_path}: {e}")


async def go_gpt_text_request(message: Message) -> None:
    user_id = message.from_user.id
    degree = await db.get_user_setting('chatgpt_degree', user_id)
    settings = await db.get_user_setting('chatgpt_settings', user_id)
    model = await db.get_user_setting('chatgpt_model', user_id)
    frequency = await db.get_user_setting('chatgpt_frequency', user_id)
    presence = await db.get_user_setting('chatgpt_presence', user_id)
    reasoning_effort = await db.get_user_setting('chatgpt_reasoning_effort', user_id)

    await bot.send_chat_action(user_id, 'typing')
    answer = await solo_request(None, message, degree, None, model, frequency=frequency, reasoning=reasoning_effort, presence=presence)
    print(answer[1])
    cleared_answer = await convert_latex_to_unicode(answer[1])

    await message.answer(texts.ChatGptTexts.water_mark_omnigpt.format(answer[2]))
    try:
        cleared_answer_str = str(cleared_answer)
        if len(cleared_answer_str) > 4000:
            file_path = f'{re.sub(r'[:\-]', '_', str(datetime.now()).split('.')[0])}.txt'

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(cleared_answer_str)

            document = FSInputFile(file_path)
            await bot.send_document(message.chat.id, document)
            os.remove(file_path)
        else:
            await message.answer(cleared_answer_str, parse_mode="Markdown")
    except:
        print(traceback.format_exc())


async def process_file_gpt_request(message: Message, state: FSMContext, settings=None) -> None:

    user_id = message.from_user.id
    result: bool = await bot.send_chat_action(user_id, 'upload_document')
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    postprocess_bool = await db.get_user_setting('postprocess_bool', user_id)
    file_path = file.file_path
    main_file_name = ['user_files/', message.document.file_name]
    await bot.download_file(file_path, main_file_name[0]+main_file_name[1])
    similar_sentences_files = ['', '', '']
    text = detect_file_format(main_file_name[0]+main_file_name[1])
    model = await db.get_user_setting('chatgpt_model', user_id)
    marks = await db.get_user_setting('gpt_tokens', user_id)
    similar = await db.get_user_setting('similarity_threshold', user_id)
    result: bool = await bot.send_chat_action(user_id, 'typing')
    try:
        marks = int(marks)
        symbol = None
    except:
        symbol = marks
    chunks = split_text(text, token=marks, symbol=symbol)
    await message.answer(f'<b>Количество запросов в файле</b>: {len(chunks)}\n')

    answer = await chunks_request(chunks, message, settings)

    await message.answer(MainMenuTexts.water_mark_omnigpt.format(answer[2]))

    file_name = main_file_name[1].rsplit('.', 1)[0] + '.txt'
    answers_to_similar = []
    with open(file_name, "w", encoding=TYPE_TXT_FILE or "utf-8") as file:
        for answer in answer[1]:
            answers_to_similar.append(answer)
            file.write(str(answer) + "\n\n")
    document = FSInputFile("user_files/GPT"+file_name)
    await bot.send_document(message.chat.id, document)

    if postprocess_bool and similar!=0:
        print('ans to sim')
        similar_sentences_files = await remove_similar_sentences("user_files/GPT"+file_name,answers_to_similar, similar)
        document_deleted = FSInputFile(similar_sentences_files[0])
        await bot.send_message(message.chat.id, 'фильтрованный файл')
        await bot.send_document(message.chat.id, document_deleted)

        document_filtered = FSInputFile(similar_sentences_files[1])
        await bot.send_message(message.chat.id, 'предложения, которые были удалены')
        await bot.send_document(message.chat.id, document_filtered)

        document_paired = FSInputFile(similar_sentences_files[2])
        await bot.send_message(message.chat.id, 'похожие предложения')
        await bot.send_document(message.chat.id, document_paired)

    files_to_remove = [
        f"txt files/{file_name}",
        f'{file_name}',
        similar_sentences_files[0],
        similar_sentences_files[1],
        similar_sentences_files[2],
        f'txt files/sorted{file_name}',
        f'txt files/GPT{file_name}',
        f'{main_file_name[0] + main_file_name[1]}'
    ]

    for file_path in files_to_remove:
        safe_remove(file_path)