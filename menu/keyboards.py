from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from menu.texts import AudioToText

class MainMenuKeyboard:
    @staticmethod
    def create_reply_main_menu():

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='🤖 ChatGpt'),
                    KeyboardButton(text='🎙 Озвучка'),
                    KeyboardButton(text='👁‍🗨 Зрение'),
                    KeyboardButton(text='👨‍🎨 Визуализация'),
                    KeyboardButton(text='📝 Аудио в текст')
                ]
                ],  resize_keyboard=True)

        return keyboard

    @staticmethod
    def create_pls_accept():
        builder = InlineKeyboardBuilder()
        keyboard = builder.row(InlineKeyboardButton(text='🙏 Доступ', callback_data='access_pls'))
        return keyboard.as_markup()

    @staticmethod
    def create_access():
        names_gender = ['✅ Принять', '❌ Отказать']
        builder = InlineKeyboardBuilder()
        for name in names_gender:
            builder.button(text=f"{name}", callback_data=f"{name}")
        return builder.as_markup()

class SpeechKeyboard:
    @staticmethod
    def create_inline_speech_settings():

        names_settings_speech = ['🔊 Скорость', '🗣 Голос']
        builder = InlineKeyboardBuilder()
        for name in names_settings_speech:
            builder.button(text=f"{name}", callback_data=f"{name}")
        return builder.as_markup()

    @staticmethod
    def create_voice_menu():
        builder = InlineKeyboardBuilder()
        voices = [
            'alloy', 'ash', 'ballad', 'coral', 'echo',
            'fable', 'nova', 'onyx', 'sage', 'shimmer'
        ]

        # Добавляем кнопки по 2 в ряд
        for i in range(0, len(voices), 2):
            row = [
                InlineKeyboardButton(
                    text=voices[i], callback_data=f'change_voice:{voices[i]}'
                )
            ]
            if i + 1 < len(voices):
                row.append(
                    InlineKeyboardButton(
                        text=voices[i + 1], callback_data=f'change_voice:{voices[i + 1]}'
                    )
                )
            builder.row(*row)

        builder.row(InlineKeyboardButton(text='Отмена', callback_data='video_cancel'))
        return builder.as_markup()

    @staticmethod
    def create_speech_main():

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='◀️ Назад'),
                    KeyboardButton(text='🎙 Панель')
                ]
                ],  resize_keyboard=True)

        return keyboard


class AudioToTextKeyboard:
    @staticmethod
    def inline_synthesis_language():
        builder = InlineKeyboardBuilder()
        for i in range(0, len(AudioToText.languages), 6):
            row = AudioToText.languages[i:i + 6]
            buttons_row = [
                InlineKeyboardButton(text=language['flag'] + ' ' + language["code"],
                                     callback_data=f'synthesis_language:{language["code"]}') for
                language in row
            ]
            builder.row(*buttons_row)
        builder.row(
            InlineKeyboardButton(text='🔙 Назад', callback_data='back_synthesis_language'),
            InlineKeyboardButton(text='🏁 auto', callback_data='synthesis_language:auto')
        )
        return builder.as_markup()
    @staticmethod
    def create_synthesis_main():

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='◀️ Назад'),
                    KeyboardButton(text='📝 Панель')
                ]
                ],  resize_keyboard=True)

        return keyboard
    @staticmethod
    def create_inline_synthesis_settings():
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text='⚙️ Язык', callback_data='synthesis_language_settings'),
            InlineKeyboardButton(text='📨 Формат', callback_data='synthesis_format_settings')
        )
        return builder.as_markup()
    @staticmethod
    def create_format_synthesis_settings():
        builder = InlineKeyboardBuilder()
        builder.row(
        InlineKeyboardButton(text='Текст', callback_data=f'synthesis_format:text'),
        InlineKeyboardButton(text='Субтитры', callback_data=f'synthesis_format:subtitles'),
        InlineKeyboardButton(text='Слова', callback_data=f'synthesis_format:word'))

        return builder.as_markup()

class VisualisationKeyboard:
    @staticmethod
    def create_inline_picture_models():
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text='🥈 GPT Image', callback_data='model_picture:gpt-image-1'),
            InlineKeyboardButton(text='🥇 dall-e-3', callback_data='model_picture:dall-e-3')
        )
        builder.row(InlineKeyboardButton(text='🔙 Назад', callback_data='picture_back'))
        return builder.as_markup()
    @staticmethod
    def create_inline_picture_settings():
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text='🤖 Модель', callback_data='model_picture'),
            InlineKeyboardButton(text='📏 Размер', callback_data='size_picture'),
            InlineKeyboardButton(text='🔢 Количество', callback_data='count_picture')
        )
        return builder.as_markup()

    @staticmethod
    def create_visualisation_menu():
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='◀️ Назад'),
                    KeyboardButton(text='👨‍🎨 Панель')
                ]
                ],  resize_keyboard=True)
        return keyboard
    @staticmethod
    def create_picture_count():
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text='1', callback_data='picture_count:1'),
            InlineKeyboardButton(text='2', callback_data='picture_count:2'),
            InlineKeyboardButton(text='3', callback_data='picture_count:3'),
            InlineKeyboardButton(text='4', callback_data='picture_count:4'),
            InlineKeyboardButton(text='5', callback_data='picture_count:5')
        )
        builder.row(
            InlineKeyboardButton(text='6', callback_data='picture_count:6'),
            InlineKeyboardButton(text='7', callback_data='picture_count:7'),
            InlineKeyboardButton(text='8', callback_data='picture_count:8'),
            InlineKeyboardButton(text='9', callback_data='picture_count:9'),
            InlineKeyboardButton(text='10', callback_data='picture_count:10')
        )

        builder.row(InlineKeyboardButton(text='🔙 Назад', callback_data='picture_back'))
        return builder.as_markup()

    @staticmethod
    def create_picture_size():
        builder = InlineKeyboardBuilder()
        builder.row(
        InlineKeyboardButton(text='1024x1024', callback_data='picture_size:1024x1024')
        )
        builder.row(InlineKeyboardButton(text='1792x1024', callback_data='picture_size:1792x1024'),
            )
        builder.row(
            InlineKeyboardButton(text='1024x1792', callback_data='picture_size:1024x1792')
        )
        builder.row(InlineKeyboardButton(text='🔙 Назад', callback_data='picture_back'))
        return builder.as_markup()


    @staticmethod
    def create_picture_menu():
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='⬅️ Назад'),
                    KeyboardButton(text='👨‍🎨 Панель')
                ]
                ],  resize_keyboard=True)

        return keyboard


class ChatGptKeyboard:

    @staticmethod
    def create_chatgpt_menu():
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='⬅️ Назад'),
                    KeyboardButton(text='🤖 Панель')
                ]
                ],  resize_keyboard=True)

        return keyboard


    @staticmethod
    def create_chatgpt_file_inline():
        names_gender = ['❌ Нет', '✅ Да']
        builder = InlineKeyboardBuilder()
        for name in names_gender:
            builder.button(text=f"{name}", callback_data=f"{name}")
        return builder.as_markup()

    @staticmethod
    def create_gpt_settings(postprocess_bool):
        dict_bool = {1:'✅', 0:'❌'}
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text='⚙️ Настройки', callback_data='⚙️ Настройки'),
            InlineKeyboardButton(text='🌡 Градус', callback_data='🌡 Градус'),
            InlineKeyboardButton(text='🤖 Модель', callback_data='🤖 Модель'),
            InlineKeyboardButton(text='📏 Разделить', callback_data='📏 Разделить')
        )
        builder.row(
            InlineKeyboardButton(text='📉 Коэффициент', callback_data='📉 Коэффициент'),
            InlineKeyboardButton(text='🚀 Креативность', callback_data='🚀 Креативность'),
            InlineKeyboardButton(text='🧠 Логика', callback_data='🧠 Логика'),
            InlineKeyboardButton(text='🦄 Уникальность', callback_data='🦄 Уникальность')
        )
        builder.row(
            InlineKeyboardButton(text=f'📝 История', callback_data='📝 История')
        )
        builder.row(
            InlineKeyboardButton(text=f'🔬Сортировка {dict_bool[postprocess_bool]}', callback_data='postsettings')
        )
        return builder.as_markup()


class ChatGptSettingsKeyboard:
    @staticmethod
    def create_gpt_model_settings(postsettings = ''):
        builder = InlineKeyboardBuilder()

        # Первый ряд с тремя кнопками
        builder.row(
            InlineKeyboardButton(text='🏅gpt-4o', callback_data=f'gpt_model:{postsettings}gpt-4o'),
            InlineKeyboardButton(text='🎖gpt-4-turbo', callback_data=f'gpt_model:{postsettings}gpt-4-turbo'),
            InlineKeyboardButton(text='🥈gpt-4o-mini', callback_data=f'gpt_model:{postsettings}gpt-4o-mini')
        )
        builder.row(
            InlineKeyboardButton(text='o4-mini', callback_data=f'gpt_model:{postsettings}o4-mini'),
            InlineKeyboardButton(text='o3-mini-2025-01-31', callback_data=f'gpt_model:{postsettings}o3-mini-2025-01-31'),
            InlineKeyboardButton(text='chatgpt-4o-latest', callback_data=f'gpt_model:{postsettings}chatgpt-4o-latest'),
            InlineKeyboardButton(text='gpt-4o-search-preview', callback_data=f'gpt_model:{postsettings}gpt-4o-search-preview')
        )
        builder.row(
            InlineKeyboardButton(text='🥉gpt-3.5-turbo', callback_data=f'gpt_model:{postsettings}gpt-3.5-turbo'),
            InlineKeyboardButton(text='🏆gpt-4.1', callback_data=f'gpt_model:gpt-4.1'),
            InlineKeyboardButton(text='🥇gpt-4', callback_data=f'gpt_model:gpt-4')
        )
        builder.row(
            InlineKeyboardButton(text='◀️ Назад', callback_data=f'gpt_back_to_main_markup')
        )
        return builder.as_markup()
    @staticmethod
    def create_inline_kb_default_settings():
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text='Отмена', callback_data='cancel_inline'))
        return builder.as_markup()

    @staticmethod
    def inline_cancel():
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text='Отмена', callback_data='cancel_inline'))
        return builder.as_markup()

    @staticmethod
    def create_queue_button():
        names_gender = ['✅ Выполнить', '🎛 Настройка']
        builder = InlineKeyboardBuilder()
        for name in names_gender:
            builder.button(text=f"{name}", callback_data=f"{name}")
        return builder