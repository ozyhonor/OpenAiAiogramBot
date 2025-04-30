import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('users_.db')
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    -- Глобальные переменные (для Telegram-бота)
    id INTEGER PRIMARY KEY,
    id_picture_panel INTEGER DEFAULT 0,
    id_settings_panel INTEGER DEFAULT 0,
    id_gpt_panel INTEGER DEFAULT 0,
    id_speech_panel INTEGER DEFAULT 0,
    id_vision_panel INTEGER DEFAULT 0,
    id_synthesis_panel INTEGER DEFAULT 0,

    -- Настройки для генирации изображения
    picture_model TEXT DEFAULT 'dall-e-2',
    picture_prompt TEXT DEFAULT 'Нарисуй картину маслом.',
    picture_size TEXT DEFAULT '1024x1024',
    picture_count INTEGER CHECK (picture_count >= 1 AND synthes_speed <= 10) DEFAULT 1,

    chatgpt_frequency FLOAT CHECK (chatgpt_frequency >= -2 AND chatgpt_frequency <= 2) DEFAULT 0 ,
    chatgpt_presence  FLOAT CHECK (chatgpt_presence >= -2 AND chatgpt_presence <= 2) DEFAULT 0,
    chatgpt_reasoning_effort TEXT DEFAULT 'medium',


    synthesis_language TEXT DEFAULT 'ru',
    synthesis_response_format TEXT DEFAULT 'text',

    -- Настройки для GPT-чата
    chatgpt_settings TEXT DEFAULT 'You have to compress texts to 100-150 characters revealing the main essence. Always give answers in Russian. No need to write what you did, just give me a compressed text in response.',
    chatgpt_model TEXT DEFAULT 'gpt-3.5-turbo',
    gpt_tokens TEXT CHECK (
        (gpt_tokens GLOB '[0-9]*' AND CAST(gpt_tokens AS INTEGER) BETWEEN 100 AND 128000) 
        OR (LENGTH(gpt_tokens) <= 11)
    ) DEFAULT '4096',
    chatgpt_degree FLOAT CHECK (chatgpt_degree >= 0 AND chatgpt_degree <= 1) DEFAULT 0,
    postprocess_bool BOOLEAN DEFAULT 0,

    -- Настройки для озвучки
    synthes_voice TEXT CHECK (synthes_voice IN ('alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer')) DEFAULT 'nova',
    synthes_speed FLOAT CHECK (synthes_speed >= 0.25 AND synthes_speed <= 4.0) DEFAULT 1,

    -- Постпроцессинг (GPT и Vision)
    vision_prompt TEXT DEFAULT '-',
    vision_model TEXT DEFAULT 'gpt-4o',
    ban BOOLEAN DEFAULT 0,
    similarity_threshold FLOAT CHECK (similarity_threshold >= 0 AND similarity_threshold <= 1) DEFAULT 0.5
    

)
""")

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
