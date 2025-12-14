#!/bin/bash
# Скрипт для запуска автоматического аудита

set -e

cd "$(dirname "$0")"

# Активируем виртуальное окружение (опционально)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Проверяем зависимости
if ! command -v lighthouse &> /dev/null; then
    echo "Ошибка: Lighthouse не установлен"
    exit 1
fi

if ! python3 -c "import clickhouse_driver" &> /dev/null; then
    echo "Установка зависимостей Python..."
    pip3 install -r requirements.txt
fi

# Запускаем основной скрипт
python3 lighthouse_to_clickhouse.py

# Очищаем старые отчёты (если нужно)
find ./reports -name "*.html" -mtime +30 -delete 2>/dev/null || true
