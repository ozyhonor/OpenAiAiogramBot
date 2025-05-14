import json
import aiofiles

FILENAME = 'messages.json'
MAX_MESSAGES = 20
MAX_CHARS = 50000

async def load_messages(filename):
    try:
        async with aiofiles.open(filename, 'r', encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)
    except FileNotFoundError:
        return []


async def save_messages(messages, filename):
    async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(messages, ensure_ascii=False, indent=2))

def get_last_n_messages(messages, n):
    return messages[-n:]

async def add_message(messages, new_message):
    messages.append(new_message)
    # Удаляем старые сообщения, если превышены лимиты
    while (len(messages) > MAX_MESSAGES or
           len(json.dumps(messages, ensure_ascii=False)) > MAX_CHARS):
        messages.pop(0)  # Удаляем самое старое сообщение
        await asyncio.sleep(0)  # Позволяет другим задачам выполняться
    while len(json.dumps(messages, ensure_ascii=False)) > MAX_CHARS and messages:
        messages.pop(0)
        await asyncio.sleep(0)
    return messages

# Пример использования:
import asyncio

async def main():
    messages = await load_messages(FILENAME)
    new_message = {"text": "Нов!", "from": "вася"}
    messages = add_message(messages, new_message)

    # Сохраняем обратно
    await save_messages(messages, FILENAME)

    # Получаем последние 4 сообщения
    last_4 = get_last_n_messages(messages, 4)
    print(last_4)

if __name__ == "__main__":
    asyncio.run(main())