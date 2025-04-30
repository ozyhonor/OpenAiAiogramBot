from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Dict, Any
from menu.keyboards import MainMenuKeyboard
from db.database import db
from config_reader import admins_ids
from logger_setup import logger
from aiogram import types
from functools import wraps



async def check_user_in_db(user_id: int) -> bool:
    answer = await db.is_user_exist(user_id)
    return answer


def admin_required(func: Callable[[types.Message], Awaitable[Any]]) -> Callable[[types.Message], Awaitable[Any]]:
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        user_id = message.from_user.id
        if user_id in admins_ids:
            return await func(message, *args, **kwargs)
        else:
            await message.answer("У вас нет прав для выполнения этой команды.")
            print(user_id, admins_ids)
            return None
    return wrapper


class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = getattr(event, 'from_user', None)
        if not user:
            return await handler(event, data)

        user_id = user.id
        user_name = user.full_name

        is_banned = await db.get_user_setting('ban', user_id)
        if is_banned:
            logger.info(f"⛔ Игнорируем забаненного пользователя: {user_name} ({user_id})")
            if isinstance(event, types.CallbackQuery):
                try:
                    await event.answer(cache_time=1)
                except Exception:
                    pass
            return
        if isinstance(event, types.Message):
            is_known = await check_user_in_db(user_id)
            if not is_known:
                if user_id in admins_ids:
                    await db.add_new_user(user_id)
                    logger.info(f'Админ {user_name} был автоматически добавлен')
                    return await handler(event, data)
                markup = MainMenuKeyboard.create_pls_accept()
                await event.answer("Запросите доступ.", reply_markup=markup)
                logger.warning(f"⚠️ Неизвестный пользователь id:{user_id}, name:{user_name}")
                return

        return await handler(event, data)


