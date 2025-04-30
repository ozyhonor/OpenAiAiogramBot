from aiogram.fsm.state import State, StatesGroup


class WaitingStateChatGpt(StatesGroup):
    wait_message_from_user = State()
    file = State()

class WaitingStateAudioToText(StatesGroup):
    wait_message_from_user = State()

class WaitingStateSpeech(StatesGroup):
    wait_message_from_user = State()
    rate = State()
    file = State()

class WaitingStatesChatGptSettings(StatesGroup):

    frequency_penalty_state = State()  # уникальност
    presence_penalty_state = State()  # креативность
    reasoning_effort_gpt = State()  # логика
    postsettings = State()
    postmodel = State()
    queue_files = State()
    settings = State()
    text_gpt = State()
    file_gpt = State()
    model = State()
    degree = State()
    theme = State()
    tokens = State()
    coefficient = State()


class AdminStates(StatesGroup):
    need_add_new_user = State()
    need_ban_new_user = State()



class WaitingStateVisualisation(StatesGroup):
    wait_message_from_user = State()
