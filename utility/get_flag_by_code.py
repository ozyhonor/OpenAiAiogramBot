from menu.texts import AudioToText


async def get_flag_by_code(flag_code):
    flag = 0
    for language in AudioToText.languages:
        if language['code'].lower() == str(flag_code).lower():
            flag = language['flag']
    return flag