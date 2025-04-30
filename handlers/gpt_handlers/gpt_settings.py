from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from db.database import db
from aiogram.fsm.context import FSMContext
from states.states import WaitingStatesChatGptSettings
from spawnbot import bot
from menu.keyboards import ChatGptSettingsKeyboard, ChatGptKeyboard
from menu.texts import ChatGptTexts
from logger_setup import logger
from menu import keyboards, texts

gpt_settings = Router()


@gpt_settings.callback_query(F.data == '⚙️ Настройки+')
async def change_gpt_postsettings(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    await state.set_state(WaitingStatesChatGptSettings.postsettings)
    markup = ChatGptSettingsKeyboard.create_inline_kb_default_settings()
    await bot.send_message(user_id, ChatGptTexts.write_gpt_settings, reply_markup=markup)

@gpt_settings.callback_query(F.data == '⚙️ Настройки')
async def change_gpt_settings(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    await state.set_state(WaitingStatesChatGptSettings.settings)
    markup = ChatGptSettingsKeyboard.create_inline_kb_default_settings()
    await bot.send_message(user_id, ChatGptTexts.write_gpt_settings, reply_markup=markup)


@gpt_settings.callback_query(F.data == '🤖 Модель+')
async def change_gpt_postmodel(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    markup = ChatGptSettingsKeyboard.create_gpt_model_settings('post')
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=markup)



@gpt_settings.callback_query(lambda callback_query: callback_query.data == 'gpt_back_to_main_markup')
async def back_from_model_menu(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await state.clear()
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    markup = ChatGptKeyboard.create_gpt_settings(process_bool)
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=markup)



@gpt_settings.callback_query(F.data == '🤖 Модель')
async def change_gpt_model(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    markup = ChatGptSettingsKeyboard.create_gpt_model_settings()
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=markup)


@gpt_settings.callback_query(lambda callback_query: callback_query.data.startswith('postsettings'))
async def change_postprocess_bool(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    panel_id = await db.get_user_setting('id_gpt_panel', user_id)
    message_id = callback_query.message.message_id
    last_postprocess = await db.get_user_setting('postprocess_bool', user_id)
    await db.update_user_setting('postprocess_bool', not(last_postprocess), user_id)
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    markup = ChatGptKeyboard.create_gpt_settings(process_bool)
    new_text_settings = await reload_settings(user_id)
    await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)


@gpt_settings.callback_query(lambda callback_query: callback_query.data.startswith('gpt_model:post'))
async def change_gpt_model(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    model = callback_query.data.split(':post')[1]
    panel_id = await db.get_user_setting('id_gpt_panel', user_id)
    message_id = callback_query.message.message_id
    await db.update_user_setting('postmodel', model, user_id)
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    markup = ChatGptKeyboard.create_gpt_settings(process_bool)
    new_text_settings = await reload_settings(user_id)
    await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)


@gpt_settings.callback_query(lambda callback_query: callback_query.data.startswith('gpt_model:'))
async def change_gpt_model(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    model = callback_query.data.split(':')[1]
    panel_id = await db.get_user_setting('id_gpt_panel', user_id)
    message_id = callback_query.message.message_id
    await db.update_user_setting('chatgpt_model', model, user_id)
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    markup = ChatGptKeyboard.create_gpt_settings(process_bool)
    new_text_settings = await reload_settings(user_id)
    await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)


@gpt_settings.message(WaitingStatesChatGptSettings.settings)
async def process_settings(message: Message, state: FSMContext) -> None:
    user_id, settings = message.from_user.id, message.text

    panel_id = await db.get_user_setting('id_gpt_panel', user_id)
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    markup = ChatGptKeyboard.create_gpt_settings(process_bool)
    await db.update_user_setting('chatgpt_settings', settings, user_id)
    await message.delete()
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    new_text_settings = await reload_settings(user_id)
    await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)
    await state.clear()


@gpt_settings.callback_query(F.data == '📉 Коэффициент')
async def change_gpt_coefficient(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    markup = ChatGptSettingsKeyboard.inline_cancel()
    await state.set_state(WaitingStatesChatGptSettings.coefficient)
    await bot.send_message(user_id, '<b>Введите коэффициент сравнения от [0 до 1].</b>', reply_markup=markup)


@gpt_settings.message(WaitingStatesChatGptSettings.coefficient)
async def process_coefficient(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    panel_id = await db.get_user_setting('id_gpt_panel', user_id)
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    markup = ChatGptKeyboard.create_gpt_settings(process_bool)
    try:
        coefficient = float(message.text)

        if not(0<=coefficient and coefficient<=1):
            raise ValueError
        await db.update_user_setting('similarity_threshold', coefficient, user_id)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
        new_text_settings = await reload_settings(user_id)
        await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
        await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)
        await state.clear()
    except ValueError:
        print('123123')



@gpt_settings.callback_query(F.data == '📏 Разделить')
async def change_gpt_degree(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    markup = ChatGptSettingsKeyboard.inline_cancel()
    await state.set_state(WaitingStatesChatGptSettings.tokens)
    await bot.send_message(user_id, '<b>Введите количество символов в одном запросе ChatGpt до 128 тыс. или разделяющую метку, пример: "#*#*#"</b>', reply_markup=markup)


@gpt_settings.message(WaitingStatesChatGptSettings.tokens)
async def process_degree(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    panel_id = await db.get_user_setting('id_gpt_panel', user_id)
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    markup = ChatGptKeyboard.create_gpt_settings(process_bool)
    tokens = message.text
    try:
        await db.update_user_setting('gpt_tokens', tokens, user_id)
    except:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    await message.delete()
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
    new_text_settings = await reload_settings(user_id)
    await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
    await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)
    await state.clear()


@gpt_settings.callback_query(F.data == '🦄 Уникальность')
async def change_frequency_penalty_gpt(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    markup = ChatGptSettingsKeyboard.inline_cancel()
    await state.set_state(WaitingStatesChatGptSettings.frequency_penalty_state)
    await bot.send_message(user_id, '<b>Введите уникальность ответов от ChatGpt</b>', reply_markup=markup)


@gpt_settings.message(WaitingStatesChatGptSettings.frequency_penalty_state)
async def process_frequency(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    panel_id = await db.get_user_setting('id_gpt_panel', user_id)
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    markup = ChatGptKeyboard.create_gpt_settings(process_bool)
    try:
        frequency_penalty_gpt = float(message.text)

        if not(-2<=frequency_penalty_gpt and frequency_penalty_gpt<=2):
            raise ValueError
        await db.update_user_setting('chatgpt_frequency', frequency_penalty_gpt, user_id)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
        new_text_settings = await reload_settings(user_id)
        await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
        await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)
        await state.clear()
    except ValueError:
        print('123123')


@gpt_settings.callback_query(F.data == '🚀 Креативность')
async def change_presence_penalty_gpt(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    markup = ChatGptSettingsKeyboard.inline_cancel()
    await state.set_state(WaitingStatesChatGptSettings.presence_penalty_state)
    await bot.send_message(user_id, '<b>Введите креативность ответов от ChatGpt</b>', reply_markup=markup)


@gpt_settings.message(WaitingStatesChatGptSettings.presence_penalty_state)
async def process_presence_penalty(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    panel_id = await db.get_user_setting('id_gpt_panel', user_id)
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    markup = ChatGptKeyboard.create_gpt_settings(process_bool)
    try:
        presence_penalty = float(message.text)

        if not(-2<=presence_penalty and presence_penalty<=2):
            raise ValueError
        await db.update_user_setting('chatgpt_presence', presence_penalty, user_id)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
        new_text_settings = await reload_settings(user_id)
        await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
        await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)
        await state.clear()
    except Exception as e:
        logger.exception(e)


@gpt_settings.callback_query(F.data == '🧠 Логика')
async def change_logic_gpt(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    markup = ChatGptSettingsKeyboard.inline_cancel()
    await state.set_state(WaitingStatesChatGptSettings.reasoning_effort_gpt)
    await bot.send_message(user_id, '<b>Введите "low", "medium", "high" логики ChatGpt</b>', reply_markup=markup)


@gpt_settings.message(WaitingStatesChatGptSettings.reasoning_effort_gpt)
async def process_reasoning_effort_gpt(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    panel_id = await db.get_user_setting('id_gpt_panel', user_id)
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    markup =ChatGptKeyboard.create_gpt_settings(process_bool)
    try:
        reasoning_effort_gpt = message.text

        if not(reasoning_effort_gpt in ['low','medium','high']):
            raise ValueError
        await db.update_user_setting('chatgpt_reasoning_effort', reasoning_effort_gpt, user_id)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
        new_text_settings = await reload_settings(user_id)
        await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
        await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)
        await state.clear()
    except ValueError:
        print('123123')


@gpt_settings.callback_query(F.data == '🌡 Градус')
async def change_gpt_degree(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    markup = ChatGptSettingsKeyboard.inline_cancel()
    await state.set_state(WaitingStatesChatGptSettings.degree)
    await bot.send_message(user_id, '<b>Введите темперауру ответов от ChatGpt</b>', reply_markup=markup)


@gpt_settings.message(WaitingStatesChatGptSettings.degree)
async def process_degree(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    panel_id = await db.get_user_setting('id_gpt_panel', user_id)
    process_bool = await db.get_user_setting('postprocess_bool', user_id)
    markup = ChatGptKeyboard.create_gpt_settings(process_bool)
    try:
        degree = float(message.text)

        if not(0<=degree and degree<=1):
            raise ValueError
        await db.update_user_setting('chatgpt_degree', degree, user_id)
        await message.delete()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
        new_text_settings = await reload_settings(user_id)
        await bot.edit_message_text(chat_id=user_id, message_id=panel_id, text=new_text_settings)
        await bot.edit_message_reply_markup(chat_id=user_id, message_id=panel_id, reply_markup=markup)
        await state.clear()
    except ValueError:
        print('123123')


async def reload_settings(user_id):

    settings = await db.get_user_setting('chatgpt_settings', user_id)
    degree = await db.get_user_setting('chatgpt_degree', user_id)
    gpt_model = await db.get_user_setting('chatgpt_model', user_id)
    gpt_tokens = await db.get_user_setting('gpt_tokens', user_id)
    need_analysis = await db.get_user_setting('postprocess_bool', user_id)

    similarity_threshold = await db.get_user_setting('similarity_threshold', user_id)

    frequency_penalty_gpt = await db.get_user_setting('chatgpt_frequency', user_id)
    reasoning_effort_gpt = await db.get_user_setting('chatgpt_reasoning_effort', user_id)
    presence_penalty_gpt = await db.get_user_setting('chatgpt_presence', user_id)

    new_text_to_panel = ChatGptTexts.settings_request_with_postprocessing.format(settings,
                                                                          degree,
                                                                          gpt_model,
                                                                          gpt_tokens,
                                                                          similarity_threshold,
                                                                          presence_penalty_gpt,
                                                                          reasoning_effort_gpt,
                                                                          frequency_penalty_gpt)
    return new_text_to_panel
