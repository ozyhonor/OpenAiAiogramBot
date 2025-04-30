from menu.keyboards import MainMenuKeyboard
from middlewears.access import admin_required
from aiogram import types
from spawnbot import bot
from config_reader import admins_ids
from aiogram import Router, F
from aiogram.filters import Command
from logger_setup import logger
from states.states import AdminStates
from db.database import db
from aiogram.fsm.context import FSMContext
from menu.texts import MainMenuTexts
from aiogram.types import Message, CallbackQuery

main_router = Router()

@main_router.callback_query(lambda callback_query: callback_query.data.startswith('access_pls'))
async def process_music(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    is_user_exist_value = await db.is_user_exist(user_id)
    reply_markup = MainMenuKeyboard.create_reply_main_menu()
    for admin_id in admins_ids:
        if is_user_exist_value:
            ban_bool = await db.get_user_setting('ban', user_id)
            if ban_bool: a = '🤭'
            else: a = ''
            await callback_query.answer(f"🧊 {callback_query.from_user.full_name} у Вас есть доступ! {a} 🧊",
                                        reply_markup=reply_markup)
        else:
            await callback_query.answer('Ожидайте 😎')
            reply_markup_to_admin = MainMenuKeyboard.create_access()

            await bot.send_message(chat_id=admin_id,
                                   text=MainMenuTexts.access_info.format(user_id,
                                                           callback_query.from_user.username or callback_query.from_user.full_name),
                                   reply_markup=reply_markup_to_admin)


@main_router.callback_query(F.data == '✅ Принять')
@admin_required
async def accept_new_user(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer('Введите id:')
    await state.set_state(AdminStates.need_add_new_user)


@main_router.callback_query(F.data == '❌ Отказать')
@admin_required
async def accept_new_user(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer('Введите id:')
    await state.set_state(AdminStates.need_ban_new_user)


@main_router.message(AdminStates.need_ban_new_user)
async def refuse_access_request(message: Message, state: FSMContext):
    await db.add_new_user(message.text)
    added_user_id = message.text
    admin_name = message.from_user.username
    markup = MainMenuKeyboard.create_reply_main_menu()
    await state.clear()
    for admin_id in admins_ids:
        user_info = await bot.get_chat(added_user_id)
        username = user_info.username if user_info.username else user_info.full_name
        await db.update_user_setting('ban', True, added_user_id)
        logger.info(f"Aдмин {admin_name} отказал {username}")
        await bot.send_message(text='Было отказано.', chat_id=admin_id)
    await bot.send_message(chat_id=message.text, text='Вам отказано.')



@main_router.message(AdminStates.need_add_new_user)
async def add_new_premium_user(message: Message, state: FSMContext):
    await db.add_new_user(message.text)
    added_user_id = message.text
    admin_name = message.from_user.username
    markup = MainMenuKeyboard.create_reply_main_menu()
    await state.clear()
    for admin_id in admins_ids:
        user_info = await bot.get_chat(added_user_id)
        username = user_info.username if user_info.username else user_info.full_name

        logger.info(f"Aдмин {admin_name} добавил {username}")
        await bot.send_message(text='Пользователь добавлен', chat_id=admin_id)

    await bot.send_message(chat_id=message.text, text='Вам выдали доступ!', reply_markup=markup)


@main_router.message(F.text == '⬅️ Назад')
@main_router.message(Command("start"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    markup = MainMenuKeyboard.create_reply_main_menu()
    markup_accept = MainMenuKeyboard.create_pls_accept()
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    is_user_exist_value = await db.is_user_exist(user_id)
    if is_user_exist_value:
        await message.answer(f"Главное меню", reply_markup=markup)
    else:
        await message.answer(f"Привет, <b>{user_name}</b> !, получите доступ", reply_markup=markup_accept)


@main_router.callback_query(lambda callback_query: callback_query.data == 'cancel_inline')
async def cancel_button(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback_query.from_user.id

    data = await state.get_data()
    previous_message_id = data.get('previous_message_id')

    if previous_message_id:
        await bot.delete_message(chat_id=user_id, message_id=previous_message_id)

    await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)
    await state.clear()