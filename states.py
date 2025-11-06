"""
FSM состояния для администраторских команд.
"""

from aiogram.fsm.state import State, StatesGroup


class AdminDispatch(StatesGroup):
    """Состояния для отправки сообщения конкретному пользователю."""

    input_id = State()
    input_text = State()


class AdminDispatchAll(StatesGroup):
    """Состояния для массовой рассылки всем пользователям."""

    input_text = State()


class AdminSetReminderTimes(StatesGroup):
    """Состояния для установки времен напоминаний пользователю."""

    input_times = State()
