"""
Обработчики текстовых сообщений.
"""
import asyncio

from aiogram import types, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramForbiddenError

from bot_instance import bot, dp
from config import logger, MESSAGES, DEBUG, DEBUG_CHAT
from database import User
from services.llm_service import process_user_message
from utils import keep_typing, forward_to_debug


@dp.message(F.text)
async def handle_text_message(message: types.Message):
    """Обработка текстовых сообщений через LLM."""
    if DEBUG:
        await bot.send_message(DEBUG_CHAT, f"USER{message.chat.id}:")
    
    logger.info(f"USER{message.chat.id}TOLLM:{message.text}")
    await forward_to_debug(message.chat.id, message.message_id)
    
    # Запускаем индикатор печати
    typing_task = asyncio.create_task(keep_typing(message.chat.id))
    
    try:
        # Обрабатываем сообщение через LLM
        converted_response = await process_user_message(message.chat.id, message.text)
        
        if converted_response is None:
            await message.answer(
                "Прости, твое сообщение вызвало у меня ошибку(( "
                "Пожалуйста попробуй снова"
            )
            return
        
        # Отправляем ответ пользователю (с разбивкой на части если нужно)
        start = 0
        while start < len(converted_response):
            chunk = converted_response[start:start + 4096]
            try:
                generated_message = await message.answer(
                    chunk, 
                    parse_mode=ParseMode.MARKDOWN_V2
                )
                await forward_to_debug(message.chat.id, generated_message.message_id)
            except TelegramForbiddenError:
                user = User(message.chat.id)
                await user.get_from_db()
                user.remind_of_yourself = 0
                await user.update_in_db()
                await bot.send_message(
                    DEBUG_CHAT, 
                    f"USER{message.chat.id} заблокировал чатбота"
                )
                return
            except Exception as e:
                # Пробуем отправить без форматирования
                try:
                    generated_message = await message.answer(chunk)
                    await forward_to_debug(message.chat.id, generated_message.message_id)
                except:
                    pass
                await bot.send_message(DEBUG_CHAT, f"LLM{message.chat.id} - {e}")
            
            start += 4096
        
        logger.info(f"LLM{message.chat.id} - {converted_response}")
        
    finally:
        typing_task.cancel()


@dp.message()
async def unknown_message(message: types.Message):
    """Обработка неизвестных типов сообщений."""
    await message.answer(MESSAGES["unknown_message"])

