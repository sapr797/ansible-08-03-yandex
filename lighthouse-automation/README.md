# Lighthouse Automation with ClickHouse

Автоматизация аудита веб-сайтов с сохранением результатов в ClickHouse.

## Установка

1. Убедитесь, что установлены:
   - Node.js 18+
   - Lighthouse: `npm install -g lighthouse`
   - Google Chrome
   - Python 3.8+

2. Установите зависимости Python:
   ```bash
   pip install -r requirements.txt
   
3.Настройте конфигурацию:

bash
cp config.example.yaml config.yaml
nano config.yaml  # Отредактируйте под ваши нужды
Использование
Быстрый запуск
bash
./run_lighthouse.sh
Запуск с конкретными URL
bash
python3 lighthouse_to_clickhouse.py config.yaml https://example.com https://google.com
Настройка cron для ежедневного аудита
bash
# Добавьте в crontab (crontab -e)
0 2 * * * cd /path/to/lighthouse-automation && ./run_lighthouse.sh >> /var/log/lighthouse_cron.log 2>&1
Структура данных в ClickHouse
Таблица lighthouse_audits содержит:

Основные метрики производительности

Оценки по категориям (Performance, Accessibility, SEO, etc.)

Временные метрики (FCP, LCP, TBT, etc.)

Полный JSON-отчёт в поле raw_report

Пример запросов к ClickHouse
sql
-- Средняя производительность по сайтам
SELECT 
    url,
    avg(performance) as avg_performance,
    count() as audits_count
FROM lighthouse_audits
WHERE audit_date > now() - interval 7 day
GROUP BY url
ORDER BY avg_performance DESC

-- Тенденции производительности для конкретного сайта
SELECT 
    toDate(audit_date) as date,
    avg(performance) as daily_performance
FROM lighthouse_audits
WHERE url = 'https://example.com'
GROUP BY date
ORDER BY date
