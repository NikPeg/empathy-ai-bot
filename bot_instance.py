"""
Инициализация бота и диспетчера.
"""
from aiogram import Bot, Dispatcher
from config import TG_TOKEN

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

