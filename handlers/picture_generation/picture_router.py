from aiogram import Router, F
from aiogram.types import Message
from db.database import db
from aiogram.fsm.context import FSMContext
from menu import texts
from menu.keyboards import VisualisationKeyboard
from states.states import WaitingStateVisualisation

picture_router = Router()


@picture_router.message(F.text == '👨‍🎨 Визуализация')
async def create_picture_request_for_request(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    prompt = await db.get_user_setting('picture_prompt', user_id)
    model = await db.get_user_setting('picture_model', user_id)
    size = await db.get_user_setting('picture_size', user_id)
    picture_count = await db.get_user_setting('picture_count', user_id)

    markup = VisualisationKeyboard.create_visualisation_menu()
    f_text = '👨‍🎨 Визуализация'
    markup_inline = VisualisationKeyboard.create_inline_picture_settings()
    await message.answer(f'{texts.future_request_information.format(f_text)}', reply_markup=markup)
    text = texts.picture_panel.format(prompt, model, size, picture_count)

    id_picture_panel = await message.answer(text, reply_markup=markup_inline)
    id_picture_panel = id_picture_panel.message_id
    await db.update_user_setting('id_picture_panel', id_picture_panel, user_id)
    await state.set_state(WaitingStateVisualisation.wait_message_from_user)





