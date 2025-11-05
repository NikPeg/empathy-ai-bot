"""
FSM состояния для администраторских команд.
"""
from aiogram.fsm.state import StatesGroup, State


class ADMINKA_despatch(StatesGroup):
    """Состояния для отправки сообщения конкретному пользователю."""
    adminka_input_id = State()
    adminka_input_text = State()


class ADMINKA_despatch_all(StatesGroup):
    """Состояния для массовой рассылки всем пользователям."""
    adminka_input_text = State()

