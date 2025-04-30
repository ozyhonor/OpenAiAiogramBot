from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from db.database import db
from aiogram.fsm.context import FSMContext
from states.states import WaitingStartSpeech
from spawnbot import bot
from menu import keyboards, texts
from aiogram import types
speech_settings_router = Router()


@speech_settings_router.callback_query(F.data == '🔊 Скорость')
async def rate_speech(message: Message, state: FSMContext) -> None:
    await state.clear()
    user_id = message.from_user.id
    markup = keyboards.CustomKeyboard.inline_cancel()
    await state.set_state(WaitingStartSpeech.rate)
    await bot.send_message(chat_id=user_id, text=texts.synthesis_rate_info, reply_markup=markup)



@speech_settings_router.message(WaitingStartSpeech.rate)
async def change_rate_speech(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        await db.update_user_setting('synthes_speed', message.text, user_id)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
        markup = keyboards.CustomKeyboard.create_inline_speech_settings().as_markup()
        panel_id = await db.get_user_setting('id_speech_panel', user_id)
        new_text_settings = await reload_settings(user_id)
        await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
        await bot.edit_message_reply_markup(user_id, panel_id, reply_markup=markup)
    except Exception as e:
        print(e)
    await state.clear()


@speech_settings_router.callback_query(F.data == '🗣 Голос')
async def voice_speech(message: Message) -> None:
    user_id = message.from_user.id
    markup = keyboards.CustomKeyboard.create_voice_menu()
    await bot.send_message(chat_id=user_id, text=texts.synthesis_voice_info, reply_markup=markup)


@speech_settings_router.callback_query(lambda callback_query: callback_query.data.startswith('change_voice:'))
async def process_original_speed_button(callback_query: types.CallbackQuery, state: FSMContext):

    user_id=callback_query.from_user.id
    voice = callback_query.data.split(':')[1]
    await db.update_user_setting('synthes_voice', voice, user_id=user_id)

    await callback_query.answer('Голос изменен ✅')
    markup = keyboards.CustomKeyboard.create_inline_speech_settings().as_markup()
    panel_id = await db.get_user_setting('id_speech_panel', user_id)
    new_text_settings = await reload_settings(user_id)
    await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
    await bot.edit_message_reply_markup(user_id, panel_id, reply_markup=markup)
    data = await state.get_data()
    previous_message_id = data.get('previous_message_id')

    if previous_message_id:
        await bot.delete_message(chat_id=user_id, message_id=previous_message_id)

    await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)



async def reload_settings(user_id):
    speed = await db.get_user_setting('synthes_speed', user_id)
    voice = await db.get_user_setting('synthes_voice', user_id)
    new_settings = texts.synthesis_information.format(speed,voice)
    return new_settings
