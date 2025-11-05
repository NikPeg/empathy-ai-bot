"""
Обработчики администраторских команд.
"""
from aiogram import types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot_instance import bot, dp
from config import MESSAGES, DEBUG_CHAT
from database import User
from filters import UserIsAdmin
from states import ADMINKA_despatch, ADMINKA_despatch_all


@dp.message(ADMINKA_despatch.adminka_input_text)
async def cmd_dispatch_input_text(message: types.Message, state: FSMContext):
    """Обработка ввода текста для отправки конкретному пользователю."""
    data = await state.get_data()
    user_id = data.get("id")
    
    try:
        await bot.send_message(int(user_id), text=message.text)
    except Exception as e:
        await bot.send_message(
            DEBUG_CHAT,
            f"LLM{message.chat.id} - ошибка при отправке {e}. Вы в главном меню"
        )
        await message.answer(
            f"LLM{message.chat.id} - ошибка при отправке {e}. Вы в главном меню"
        )
        await state.clear()
        return
    
    await message.answer(MESSAGES["adminka_dispatch3"])
    await state.clear()


@dp.message(ADMINKA_despatch.adminka_input_id)
async def cmd_dispatch_input_id(message: types.Message, state: FSMContext):
    """Обработка ввода ID пользователя для отправки сообщения."""
    user_input = message.text
    await state.update_data(id=user_input)
    await message.answer(MESSAGES["adminka_dispatch2"])
    await state.set_state(ADMINKA_despatch.adminka_input_text)


@dp.message(UserIsAdmin(), Command("dispatch"))
async def cmd_dispatch(message: types.Message, state: FSMContext):
    """Команда /dispatch - отправка сообщения конкретному пользователю."""
    await message.answer(
        MESSAGES["adminka_dispatch1"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ADMINKA_despatch.adminka_input_id)


@dp.message(ADMINKA_despatch_all.adminka_input_text)
async def cmd_dispatch_all_input_text(message: types.Message, state: FSMContext):
    """Обработка ввода текста для массовой рассылки."""
    try:
        all_ids = await User.get_ids_from_table()
        success_dispatch = 0
        
        for user_id in all_ids:
            try:
                await bot.send_message(user_id, message.text)
                success_dispatch += 1
            except:
                continue
        
        result_msg = f"Сообщение отправлено {success_dispatch} пользователям"
        await bot.send_message(DEBUG_CHAT, result_msg)
        await bot.send_message(message.chat.id, result_msg)
        
    except Exception as e:
        error_msg = f"USER{message.chat.id} - ошибка при отправке {e}. Вы в главном меню"
        await bot.send_message(DEBUG_CHAT, error_msg)
        await message.answer(error_msg)
        await state.clear()
        return
    
    await message.answer(MESSAGES["adminka_dispatch3"])
    await state.clear()


@dp.message(UserIsAdmin(), Command("dispatch_all"))
async def cmd_dispatch_all(message: types.Message, state: FSMContext):
    """Команда /dispatch_all - массовая рассылка всем пользователям."""
    await message.answer(
        MESSAGES["adminka_dispatch_all"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ADMINKA_despatch_all.adminka_input_text)

