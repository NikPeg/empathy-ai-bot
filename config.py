"""
Конфигурация приложения и настройка логирования.
"""
import json
import logging
import logging.handlers
import os

from dotenv import load_dotenv
from telegramify_markdown import customize

# Загружаем переменные окружения
load_dotenv()

# Telegram конфигурация
TG_TOKEN = os.environ.get("TG_TOKEN")
DEBUG = bool(int(os.environ.get("DEBUG")))
DEBUG_CHAT = int(os.environ.get("DEBUG_CHAT"))

# LLM конфигурация
LLM_TOKEN = os.environ.get("LLM_TOKEN")

# База данных
DATABASE_NAME = os.environ.get("DATABASE_NAME")
TABLE_NAME = os.environ.get("TABLE_NAME")
MAX_CONTEXT = int(os.environ.get("MAX_CONTEXT"))

# Напоминания
DELAYED_REMINDERS_HOURS = int(os.environ.get("DELAYED_REMINDERS_HOURS"))
DELAYED_REMINDERS_MINUTES = int(os.environ.get("DELAYED_REMINDERS_MINUTES"))
TIMEZONE_OFFSET = int(os.environ.get("TIMEZONE_OFFSET"))
FROM_TIME = int(os.environ.get("FROM_TIME"))
TO_TIME = int(os.environ.get("TO_TIME"))

# Администраторы
ADMIN_LIST_STR = os.environ.get("ADMIN_LIST")
if ADMIN_LIST_STR:
    ADMIN_LIST = list(map(int, ADMIN_LIST_STR.split(",")))
else:
    ADMIN_LIST = set()

# Загрузка промптов и сообщений
with open("config/prompts.json", encoding="utf-8") as f:
    PROMPTS = json.load(f)
    DEFAULT_PROMPT = PROMPTS["DEFAULT_PROMPT"]
    REMINDER_PROMPT = PROMPTS["REMINDER_PROMPT"]

with open("config/messages.json", encoding="utf-8") as f:
    MESSAGES = json.load(f)


def setup_logger():
    """Настройка логирования."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter_console = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter_console)
    
    # File handler
    fh = logging.handlers.RotatingFileHandler(
        "debug.log", maxBytes=1024 * 1024, backupCount=5, encoding="utf8"
    )
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return logger


# Настройка telegramify_markdown
customize.strict_markdown = True
customize.cite_expandable = True

# Создаем логгер
logger = setup_logger()

