
class MainMenuTexts:
        translator_text_panel = '<b><blockquote>Отправьте сообщение или файл и я переведу на {0} {1}</blockquote></b>\n<b><blockquote>{2}/5</blockquote></b>'
        access_info = 'Запросили доступ! \nid:<pre>{0}</pre>name:@{1}'
        future_request_information = """
        ➖➖➖<b>{}</b>➖➖➖
        """
        water_mark_omnigpt = """
        ➖➖➖<b>OmniGpt</b>➖➖➖
        <b>Токенов:</b> <i>{0} потрачено</i> 
        """

class Visualisation:
        visualisation = """
<blockquote>🤖 <i>{0}</i></blockquote>\n<blockquote><i>📏 {1}</i></blockquote>\n<blockquote><i>🔢 {2}</i></blockquote>
"""

class SpeechTexts:
    synthesis_rate_info = '''
    <b>Скорость генерируемого звука. Напишите значение от 0,25 до 4,0. 1.0 является значением по умолчанию.</b>
    '''
    synthesis_voice_info = '''
    <b>Голос, который будет использоваться при создании звука. Выберите вариант из списка.</b>
    '''
    synthesis_information = """
    <b>Настройки запроса</b>\n<blockquote><b>Скорость</b>: <i>{0}</i></blockquote>\n<blockquote><b>Голос:</b> <i>{1}</i></blockquote>
    """

class ChatGptTexts:
    subscript_map = {
        'a': 'ₐ',
        'e': 'ₑ',
        'h': 'ₕ',
        'i': 'ᵢ',
        'j': 'ⱼ',
        'k': 'ₖ',
        'l': 'ₗ',
        'm': 'ₘ',
        'n': 'ₙ',
        'o': 'ₒ',
        'p': 'ₚ',
        'r': 'ᵣ',
        's': 'ₛ',
        't': 'ₜ',
        'u': 'ᵤ',
        'v': 'ᵥ',
        'x': 'ₓ',
        'y': 'ᵧ',
        '0': '₀',
        '1': '₁',
        '2': '₂',
        '3': '₃',
        '4': '₄',
        '5': '₅',
        '6': '₆',
        '7': '₇',
        '8': '₈',
        '9': '₉',
    }
    history_data = [
        {
            "text": "-",
            "from": "user"
        },
        {
            "text": "-",
            "from": "openai"
        }
    ]
    water_mark_omnigpt = """
    ➖➖➖<b>OmniGpt</b>➖➖➖
    <b>Токенов:</b> <i>{0} потрачено</i> 
    """
    write_gpt_settings = """
    <b>Введите настройки запроса</b>
    """
    dict_bool = {'✅': 1, '❌': 0}
    chatgpt_quize_text = "Отправить файл {0} chatgpt? Ответ будет в файле формата .txt"
    settings_request = """
    <b>Настройки запроса</b>:\n<pre><i>{0}</i></pre><i></i>\n\n<blockquote>🌡 <i>{1}</i></blockquote>\n<blockquote><i>🤖 {2}</i></blockquote>\n<blockquote><i>📏 {3}</i></blockquote>\n<blockquote><i>⚖️ {4}</i></blockquote>\n<blockquote><i>🚀 {5}</i></blockquote>\n<blockquote><i>🧠 {6}</i></blockquote>\n<blockquote><i>🦄 {7}</i></blockquote><i>📝 {8}</i></blockquote>
    """
    settings_request_with_postprocessing = """
    <b>Настройки запроса</b>:\n<pre><i>{0}</i></pre><i></i>\n\n<blockquote>🌡 <i>{1}</i></blockquote>\n<blockquote><i>🤖 {2}</i></blockquote>\n<blockquote><i>📏 {3}</i></blockquote>\n<blockquote><i>⚖️ {4}</i></blockquote>\n<blockquote><i>🚀 {5}</i></blockquote>\n<blockquote><i>🧠 {6}</i></blockquote>\n<blockquote><i>🦄 {7}</i></blockquote>\n<blockquote><i>📝 {8}</i></blockquote>
    """

class AudioToText:

        synthesis_panel = '<b><blockquote>Язык аудио: {0} {1}</blockquote></b>\n<b><blockquote>Формат ответа: {2}</blockquote></b>'

        languages = [
            {'code': 'en', 'flag': '🇬🇧', 'name': 'English'},
            {'code': 'es', 'flag': '🇪🇸', 'name': 'Spanish'},
            {'code': 'fr', 'flag': '🇫🇷', 'name': 'French'},
            {'code': 'ru', 'flag': '🇷🇺', 'name': 'Russian'},
            {'code': 'zh-cn', 'flag': '🇨🇳', 'name': 'Chinese (Simplified)'},
            {'code': 'ar', 'flag': '🇸🇦', 'name': 'Arabic'},
            {'code': 'pt', 'flag': '🇵🇹', 'name': 'Portuguese'},
            {'code': 'de', 'flag': '🇩🇪', 'name': 'German'},
            {'code': 'ja', 'flag': '🇯🇵', 'name': 'Japanese'},
            {'code': 'hi', 'flag': '🇮🇳', 'name': 'Hindi'},
            {'code': 'it', 'flag': '🇮🇹', 'name': 'Italian'},
            {'code': 'ko', 'flag': '🇰🇷', 'name': 'Korean'},
        ]
