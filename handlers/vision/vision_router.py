from aiogram import Router, F
from aiogram.types import Message
from utility.create_translate import create_translate_text
from db.database import db
from aiogram import Router, F
from aiogram.types import Message
import states.states
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from states.states import WaitingStateGpt
from aiogram.fsm.context import FSMContext
from menu import keyboards, texts
from spawnbot import bot
from aiogram import types
from spawnbot import bot
from aiogram import Router
from  db.database import db
from aiogram.types import Message
from states.states import WaitingStateVision
from aiogram.fsm.context import FSMContext
from menu import texts
import os
from aiogram import types
from utility.decode_any_format import detect_file_format
from utility.split_text_for_gpt import (split_text)


vision_router = Router()


@vision_router.message(F.text == '👁‍🗨 Зрение')
async def create_gpt_request_for_request(message: Message):
    user_id = message.from_user.id
    vision_prompt = await db.get_user_setting('vision_prompt', user_id)
    vision_model = await db.get_user_setting('vision_model', user_id)
    markup_inline = keyboards.CustomKeyboard.create_vision_button()
    markup_reply = keyboards.CustomKeyboard.create_vision_buttons_down()

    await message.answer(f'{texts.future_request_information.format('👁‍🗨 Зрение')}', reply_markup=markup_reply)
    text = texts.vision_request.format(vision_prompt, vision_model)
    id_vision_panel = await message.answer(text, reply_markup=markup_inline)
    id_vision_panel = id_vision_panel.message_id
    await db.update_user_setting('id_vision_panel', id_vision_panel, user_id)

@vision_router.message(WaitingStateVision.wait_photo)
async def detect_message_from_user(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.full_name

    if message.photo or (message.document and message.document.mime_type.startswith('image/')):
        logger.info(f'Пользователь {message.from_user.id} отправил сообщение для chatgpt')
        await bot.send_chat_action(user_id, 'upload_photo')
        # Получаем настройки запроса
        vision_prompt = await db.get_user_setting('vision_prompt', user_id)
        vision_model = await db.get_user_setting('vision_model', user_id)

        # Получаем изображение (берем самое большое изображение из всех отправленных)
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        file_path = file_info.file_path

        # Скачиваем изображение для дальнейшей обработки
        file_url = f"https://api.telegram.org/file/bot{telegram_token}/{file_path}"

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(file_url) as response:
                if response.status == 200:
                    image_data = await response.read()  # Получаем бинарные данные изображения

                    # Передаем данные изображения в вашу функцию solo_request для дальнейшего распознавания
                    answer = await vision_request(image_data, settings=vision_prompt, model=vision_model)

                    await message.answer(texts.water_mark_omnigpt.format(answer[2]))
                    await message.answer(f'{str(answer[1])}')
                else:
                    await message.answer("Ошибка при загрузке изображения.")

        # Очищаем состояние
