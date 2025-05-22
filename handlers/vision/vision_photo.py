from aiogram import Router, F
from aiogram.types import Message
from db.database import db
from aiogram.fsm.context import FSMContext
from states.states import WaitingStateVision
from spawnbot import bot
from menu import texts
import asyncio
from config_reader import telegram_token
from utils.vision_requests import vision_request
import aiohttp

from utils.gpt_requests import solo_request


vision_photo_router = Router()


async def go_gpt_text_request(message: Message) -> None:
    user_id = message.from_user.id
    degree = await db.get_user_setting('chatgpt_degree', user_id)
    settings = await db.get_user_setting('chatgpt_settings', user_id)
    model = await db.get_user_setting('chatgpt_model', user_id)
    frequency = await db.get_user_setting('chatgpt_frequency', user_id)



@vision_photo_router.message(WaitingStateVision.vision_photo)
async def go_gpt_text_request(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id

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
    await state.clear()
