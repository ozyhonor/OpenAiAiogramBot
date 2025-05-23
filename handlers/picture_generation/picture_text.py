import traceback
from aiogram.types.input_file import FSInputFile
import os
from aiogram import Router, F
from aiogram.types import Message
from db.database import db
from aiogram.fsm.context import FSMContext
from spawnbot import bot
from utility.picture_requests import create_solo_photo
from utility.download_picture_from_gpt import download_images
from aiogram.types import InputMediaPhoto



picture_text = Router()

async def go_picture_text_request(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    text = message.text
    model = await db.get_user_setting('picture_model', user_id)
    size = await db.get_user_setting('picture_size', user_id)
    count_of_picture = await db.get_user_setting('picture_count', user_id)
    await bot.send_chat_action(user_id, 'upload_photo')
    answer = await create_solo_photo(text, size=size, count_of_pictures=count_of_picture, model=model)
    local_picture_links = await download_images(answer[1])

    media_group = [InputMediaPhoto(media=FSInputFile(photo_path)) for photo_path in local_picture_links]
    await bot.send_media_group(user_id, media_group)

    for file in local_picture_links:
        os.remove(file)

    await state.clear()
