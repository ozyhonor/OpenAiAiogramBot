from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from db.database import db
from aiogram.fsm.context import FSMContext
from states.states import WaitingStateSpeech
from spawnbot import bot
from menu.texts import MainMenuTexts
from utility.speech_requests import openai_audio_request
from aiogram.types.input_file import FSInputFile


async def go_speech_request(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    rate = await db.get_user_setting('synthes_speed', user_id)
    voice = await db.get_user_setting('synthes_voice', user_id)
    outputfilename = 'omnibot'
    await bot.send_chat_action(message.from_user.id, 'record_voice')
    answer = await openai_audio_request(model="gpt-4o-mini-tts", voice=voice, input_text=message.text, output_file=f"user_files/{outputfilename}.mp3", speed=rate)
    await bot.send_chat_action(message.from_user.id, 'upload_voice')
    audio = FSInputFile(f'user_files/{outputfilename}.mp3')
    await message.answer(MainMenuTexts.water_mark_omnigpt.format(answer[1]))
    await bot.send_audio(message.from_user.id, audio=audio)

