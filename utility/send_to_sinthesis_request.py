from random import choice
from config_reader import gpt_tokens, proxy_config
import aiohttp
import asyncio
import traceback
import aiofiles
from random import choice
from setup_logger import logger
from yarl import URL
from utils.detect_file_format import detect_file_type


async def send_recognize_request(file, language='auto', future_format='text'):
    logger.info(f'Send recognize {file}')
    file_format = detect_file_type(file).split('_')[1]
    data = {
        'model': 'whisper-1',
        'prompt': 'use punctuation marks actively, U S'
    }
    if language != 'auto':
        data['language'] = language

    if future_format == 'text':
        format = '.txt'
        data['response_format'] = 'text'

    elif future_format == 'word':
        format = '.json'
        data['response_format'] = 'verbose_json'
        data['timestamp_granularities[]'] = 'word'

    else:
        format = '.srt'
        data = {"model": 'gpt-4o', "response_format": 'srt'}

    api_key = choice(gpt_tokens)
    url = 'https://api.openai.com/v1/audio/transcriptions'
    headers = {'Authorization': f'Bearer {api_key}'}

    async with aiofiles.open(file, 'rb') as f:
        file_data = await f.read()

    form_data = aiohttp.FormData()
    form_data.add_field('file', file_data, filename=file, content_type='audio/mpeg')
    for key, value in data.items():
        form_data.add_field(key, value)

    proxy_url = proxy_config()['http']
    parsed_url = URL(proxy_url)
    if parsed_url.user and parsed_url.password:
        proxy_auth = aiohttp.BasicAuth(parsed_url.user, parsed_url.password)
        proxy_url = str(parsed_url.with_user(None).with_password(None))
    else:
        proxy_auth = None

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=form_data, proxy=proxy_url, proxy_auth=proxy_auth) as response:
                response_text = await response.text()

                output_file = file.replace(file_format, format)
                print('out_f', output_file)
                async with aiofiles.open(output_file, 'w', encoding='utf-8') as f:
                    await f.write(response_text)
                logger.info(f'Recognize successful done with outputfile {output_file    }')
                return output_file
    except Exception as e:
        logger.error(f'Error in recognize: {e}')
        logger.debug(f"Traceback: {traceback.format_exc()}")