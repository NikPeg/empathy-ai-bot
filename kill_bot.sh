#!/bin/bash
# Скрипт для принудительной остановки бота

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔍 Ищем процессы бота в директории $SCRIPT_DIR..."
pids=$(ps aux | grep "python.*$SCRIPT_DIR/main.py" | grep -v grep | awk '{print $2}')

if [ -z "$pids" ]; then
    echo "✅ Процессы бота не найдены"
    exit 0
fi

echo "🛑 Найдены процессы:"
ps aux | grep "python.*$SCRIPT_DIR/main.py" | grep -v grep

read -p "⚠️  Остановить эти процессы? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "$pids" | xargs kill -15  # Сначала пробуем мягкую остановку
    sleep 2
    
    # Проверяем, остались ли процессы
    remaining=$(ps aux | grep "python.*$SCRIPT_DIR/main.py" | grep -v grep | awk '{print $2}')
    if [ ! -z "$remaining" ]; then
        echo "⚡ Процессы не остановились, применяем kill -9..."
        echo "$remaining" | xargs kill -9
    fi
    
    echo "✅ Все процессы остановлены"
else
    echo "❌ Отменено"
    exit 1
fi

