"""
Обработчики пользовательских команд.
"""
from aiogram import types, F
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot_instance import bot, dp
from config import MESSAGES, DEBUG_CHAT
from database import User
from filters import UserNotInDB, OldMessage
from utils import forward_to_debug


@dp.message(F.chat.id == DEBUG_CHAT)
async def test(message: types.Message):
    """Игнорирует сообщения в отладочном чате."""
    pass


@dp.message(OldMessage())
async def spam(message: types.Message):
    """Игнорирует старые сообщения (старше 1 минуты)."""
    pass


@dp.message(UserNotInDB())
async def registration(message: types.Message):
    """Регистрация нового пользователя."""
    args = message.text.split()
    
    if len(args) > 1:
        referral_code = args[1]
        await bot.send_message(
            DEBUG_CHAT, 
            f"Переход по реф.ссылке, код: {referral_code}"
        )
    
    user = message.from_user
    if user and user.username:
        username = user.username
    else:
        username = "Not_of_registration"
    
    user = User(int(message.chat.id), username)
    await user.save_for_db()
    builder = ReplyKeyboardBuilder()

    sent_msg = await message.answer(
        MESSAGES["msg_start"], 
        reply_markup=builder.as_markup()
    )
    await forward_to_debug(message.chat.id, message.message_id)
    await forward_to_debug(message.chat.id, sent_msg.message_id)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Команда /start - приветствие."""
    sent_msg = await message.answer(
        MESSAGES["msg_start"], 
        reply_markup=ReplyKeyboardRemove()
    )
    await forward_to_debug(message.chat.id, message.message_id)
    await forward_to_debug(message.chat.id, sent_msg.message_id)


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Команда /help - справка."""
    sent_msg = await message.answer(
        MESSAGES["msg_help"], 
        reply_markup=ReplyKeyboardRemove()
    )
    await forward_to_debug(message.chat.id, message.message_id)
    await forward_to_debug(message.chat.id, sent_msg.message_id)


@dp.message(Command("forget"))
async def cmd_forget(message: types.Message):
    """Команда /forget - сброс истории диалога."""
    sent_msg = await message.answer(
        MESSAGES["msg_forget"], 
        reply_markup=ReplyKeyboardRemove()
    )
    user = User(message.chat.id)
    await user.get_from_db()
    user.remind_of_yourself = "0"
    user.prompt = []
    await user.update_in_db()

    await forward_to_debug(message.chat.id, message.message_id)
    await forward_to_debug(message.chat.id, sent_msg.message_id)


@dp.message(Command("reminder"))
async def cmd_reminder(message: types.Message):
    """Команда /reminder - отключение напоминаний."""
    sent_msg = await message.answer(
        MESSAGES["msg_reminder"], 
        reply_markup=ReplyKeyboardRemove()
    )
    user = User(message.chat.id)
    await user.get_from_db()
    user.remind_of_yourself = "0"
    await user.update_in_db()
    
    await forward_to_debug(message.chat.id, message.message_id)
    await forward_to_debug(message.chat.id, sent_msg.message_id)

