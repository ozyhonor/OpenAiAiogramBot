from random import choice
import requests
import traceback
import states.states
import re
from utility.work_with_history_message import load_messages, add_message, save_messages
from config_reader import gpt_tokens

from spawnbot import bot

import states.states

from db.database import db

from config_reader import proxy_config
import concurrent.futures
from time import time
import asyncio
import aiohttp
from logger_setup import logger
from utility.decode_any_format import TYPE_TXT_FILE
from collections import defaultdict


async def write_book():
    ...


async def chunks_request(chunks, message, settings):
    start_time = time()
    used_tokens = 0
    user_id = message.from_user.id
    degree = await db.get_user_setting('chatgpt_degree', user_id)

    model = await db.get_user_setting('chatgpt_model', user_id)
    if settings is None:
        settings = await db.get_user_setting('chatgpt_settings', user_id)

    # Создаем список для хранения ответов в правильном порядке
    answers = [None] * len(chunks)

    # Отправляем первоначальное сообщение с прогрессом
    progress_msg = await message.answer(f'<b>Процесс работы:</b> <i>0/{len(chunks)}</i>')
    last_update_time = time()

    try:
        await bot.send_chat_action(user_id, 'typing')

        # Создаем словарь асинхронных задач с привязкой к индексу
        tasks = {
            i: asyncio.create_task(solo_request(chunk, message, degree, settings, model))
            for i, chunk in enumerate(chunks)
        }

        # Ожидаем выполнения задач по индексу, чтобы сохранить порядок
        for i in range(len(chunks)):
            try:
                result = await tasks[i]  # Дожидаемся именно той задачи, что соответствует индексу
                answers[i] = str(result[1]) if result else '-'  # Сохраняем ответ в правильную позицию
                used_tokens += int(result[2]) if result else 0
            except Exception as e:
                answers[i] = '-'
                print(f"Ошибка в запросе {i}: {e}")

            current_time = time()
            # Обновляем прогресс каждые 10 задач или раз в 5 секунд
            if (i + 1) % 10 == 0 or (current_time - last_update_time) >= 5:
                ...
                last_update_time = current_time  # Сбрасываем таймер обновления

                try:
                    await bot.send_chat_action(user_id, 'typing')
                except Exception as e:
                    logger.error(e)

    except Exception as e:
        print(f"Ошибка: {traceback.format_exc()}")

    # Завершаем процесс, обновляем прогресс и сохраняем результат
    await _update_progress(answers, chunks, message, progress_msg)
    await _save_answers_to_file(answers, message, "OmniBot")

    return [round(time() - start_time, 2), answers, used_tokens]

# Асинхронная функция для обновления прогресса
async def _update_progress(answers, chunks, message, msg):
    try:
        new_text = f'<b>Процесс работы:</b> <i>{len(answers)}/{len(chunks)}</i>'
        if msg.text != new_text:
            await bot.edit_message_text(new_text, chat_id=message.from_user.id, message_id=msg.message_id)
    except Exception as e:
        print(f"Ошибка обновления прогресса: {e}")


# Асинхронная функция для обработки остановки GPT
async def _handle_stop_gpt(answers, message):
    try:
        states.states.stop_gpt = False
        await _save_answers_to_file(answers, message, "upload_document")
    except:
        ...

# Асинхронная функция для обработки исключений и сохранения результатов
async def _handle_exception(answers, message):
    try:
        import re

        answers = sorted(answers,
                         key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else float('-inf'),
                         reverse=True)

        await _save_answers_to_file(answers, message, "OmniBot")
    except:
        ...


# Функция для сохранения ответов в файл
async def _save_answers_to_file(answers, message, default_name):
    try:
        file_name = f"user_files/GPT{message.document.file_name.rsplit('.', 1)[0]}.txt"
        with open(file_name, "w", encoding=TYPE_TXT_FILE or "utf-8") as file:
            for answer in answers or default_name:
                file.write(answer + "\n\n")
    except:
        ...

async def solo_request(text, message, degree, settings, model='gpt-3.5-turbo', frequency=0, presence=0, reasoning='medium',max_retries=4, history_message='', user_id=0):
    start_time = time()
    content_to_request = text or message.text
    if history_message != '':
        content_to_request = 'Это предыдущие запросы пользователя\n'+str(history_message)+'\nЭто текущий запрос\n'+(text or message.text)
        print('THIS HISTORY')
        print(content_to_request)

    if model == 'o4-mini' and degree<1:
        degree = 1
        data = {
            "model": f"{model}",
            "messages": [
                {"role": "system", "content": f"{settings or model}"},
                {"role": "user", "content": f"{content_to_request}"}
            ],
            "temperature": degree,
            "frequency_penalty": frequency,
            "presence_penalty": presence
            # "reasoning_effort": reasoning
        }
    elif model == 'o3-mini-2025-01-31' or model == 'gpt-4o-search-preview':
        data = {
            "model": f"{model}",
            "messages": [
                {"role": "system", "content": f"{settings or model}"},
                {"role": "user", "content": f"{content_to_request}"}
            ]
        }
    else:
        data = {
            "model": f"{model}",
            "messages": [
                {"role": "system", "content": f"{settings or model}"},
                {"role": "user", "content": f"{content_to_request}"}
            ],
            "temperature": degree,
            "frequency_penalty": frequency,
            "presence_penalty": presence
            # "reasoning_effort": reasoning
        }
    async def make_request(session, attempt, text, requested_text=''):
        proxy = proxy_config().get('https')
        logger.info(f"Attempt {attempt} for request.")


        api_key = choice(gpt_tokens)
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }


        try:
            async with session.post(url, json=data, headers=headers, proxy=proxy) as response:
                result = await response.json()
                status = response.status
                text = await response.text()
                answer = result['choices'][0]['message']['content']
                tokens_used = result['usage']['total_tokens']
                logger.info(f"Request successful: {tokens_used} tokens used.")

                if history_message != '':
                    history_file = f'history_messages/{user_id}.json'
                    messages = await load_messages(history_file)
                    new_message = {"text": f"{message.text}", "from": "user"}
                    new = await add_message(messages, new_message)
                    await save_messages(messages, history_file)
                    new_message = {"text": f"{answer}", "from": f"{model}"}
                    new = await add_message(messages, new_message)
                    await save_messages(messages, history_file)


                return round(time() - start_time, 2), answer, tokens_used

        except Exception as e:
            logger.error(f"{traceback.format_exc()}")
            return 0, '-', 0

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector()) as session:
        for attempt in range(1, max_retries + 1):
            time_taken, answer, tokens_used = await make_request(session, attempt, text)
            if answer:
                return time_taken, answer, tokens_used
            logger.warning(f"Retrying... ({attempt}/{max_retries})")


    logger.error("Max retries reached. Request failed.")
    return None, '-', None

