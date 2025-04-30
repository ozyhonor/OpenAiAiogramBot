from aiogram import Router, F
from aiogram.types import Message
from db.database import db
from aiogram.fsm.context import FSMContext
from menu.texts import MainMenuTexts, Visualisation
from menu.keyboards import VisualisationKeyboard
from states.states import WaitingStateVisualisation
from logger_setup import logger
from spawnbot import bot
from handlers.picture_generation.picture_text import go_picture_text_request
from utility.picture_requests import create_solo_photo
picture_router = Router()


@picture_router.message(F.text == '👨‍🎨 Панель')
@picture_router.message(F.text == '👨‍🎨 Визуализация')
async def create_picture_request_for_request(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    model = await db.get_user_setting('picture_model', user_id)
    size = await db.get_user_setting('picture_size', user_id)
    picture_count = await db.get_user_setting('picture_count', user_id)

    markup = VisualisationKeyboard.create_visualisation_menu()
    f_text = '👨‍🎨 Визуализация'
    markup_inline = VisualisationKeyboard.create_inline_picture_settings()
    await message.answer(f'{MainMenuTexts.future_request_information.format(f_text)}', reply_markup=markup)
    text = Visualisation.visualisation.format(model, size, picture_count)
    id_picture_panel = await message.answer(text, reply_markup=markup_inline)
    id_picture_panel = id_picture_panel.message_id
    await db.update_user_setting('id_picture_panel', id_picture_panel, user_id)
    await state.set_state(WaitingStateVisualisation.wait_message_from_user)


@picture_router.message(WaitingStateVisualisation.wait_message_from_user)
async def detect_message_from_user(message: Message, state: FSMContext):
    #this detect what send user text or file
    if message.text.startswith("/"):
        return
    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.full_name

    if message.text:
        user_text_request = message.text
        logger.info(f'Пользователь {message.from_user.id} отправил сообщение "{user_text_request}" для генирации картинки')
        await bot.send_chat_action(user_id, 'typing')

        await go_picture_text_request(message, state)

    else:
        await bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте текст.")






