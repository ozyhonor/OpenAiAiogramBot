from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from db.database import db
from aiogram.fsm.context import FSMContext
from spawnbot import bot
from menu import keyboards, texts
from utility.get_flag_by_code import get_flag_by_code
from menu.keyboards import AudioToTextKeyboard
from menu.texts import AudioToText

audio_tt_settings = Router()


@audio_tt_settings.callback_query(lambda callback_query: callback_query.data == 'synthesis_language_settings')
async def change_model_picture(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    id_panel = await db.get_user_setting('id_picture_panel', user_id)
    markup = AudioToTextKeyboard.inline_synthesis_language()
    await callback_query.message.edit_reply_markup(reply_markup=markup)


@audio_tt_settings.callback_query(lambda callback_query: callback_query.data.startswith('synthesis_language:'))
async def change_model_picture(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    panel_id = await db.get_user_setting('id_synthesis_panel', user_id)
    language = callback_query.data.split(':')[1]
    await db.update_user_setting('synthesis_language', language, user_id)

    markup = AudioToTextKeyboard.create_inline_synthesis_settings()
    new_text_settings = await reload_settings(user_id)

    await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
    message_id = callback_query.message.message_id
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)


@audio_tt_settings.callback_query(lambda callback_query: callback_query.data == 'back_synthesis_language')
async def change_size_picture(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    id_panel = await db.get_user_setting('id_picture_panel', user_id)
    markup = AudioToTextKeyboard.create_inline_synthesis_settings()
    await callback_query.message.edit_reply_markup(reply_markup=markup)


@audio_tt_settings.callback_query(lambda callback_query: callback_query.data.startswith('synthesis_format:'))
async def do_size_picture(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    format = callback_query.data.split(':')[1]

    panel_id = await db.get_user_setting('id_synthesis_panel', user_id)
    await db.update_user_setting('synthesis_response_format', format, user_id)

    markup = AudioToTextKeyboard.create_inline_synthesis_settings()
    new_text_settings = await reload_settings(user_id)

    await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)


@audio_tt_settings.callback_query(lambda callback_query: callback_query.data == 'synthesis_format_settings')
async def change_count_picture(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    id_panel = await db.get_user_setting('id_synthesis_panel', user_id)
    markup = AudioToTextKeyboard.create_format_synthesis_settings()
    await callback_query.message.edit_reply_markup(reply_markup=markup)



async def reload_settings(user_id):
    new_formats = {'text': 'Текст', 'word': 'Слова', 'subtitles': 'Субтитры'}
    language = await db.get_user_setting('synthesis_language', user_id)
    format = await db.get_user_setting('synthesis_response_format', user_id)
    flag = await get_flag_by_code(language)
    new_settings = AudioToText.synthesis_panel.format(language,
                                                 flag,
                                                new_formats[format])

    return new_settings
