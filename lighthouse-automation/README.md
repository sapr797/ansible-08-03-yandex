Структура проекта

ansible-hw-03/
├── lighthouse-automation/
│   ├── lighthouse_to_clickhouse.py     # Основной скрипт
│   ├── requirements.txt                # Зависимости Python
│   ├── config.example.yaml             # Пример конфигурации
│   ├── run_lighthouse.sh              # Скрипт-обёртка
│   └── README.md                      # Инструкция
├── site.yml                           # Ваш Ansible playbook
└── .github/workflows/
    └── lint.yml                       # GitHub Actions для проверки


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
GROUP BY date## 2. 🔧 Настройка окружения на ВМ Lighthouse

Выполните на ВМ `lighthous`:

```bash
# 1. Установите Python и pip
sudo apt update
sudo apt install -y python3-pip

# 2. Клонируйте или создайте структуру
mkdir -p ~/lighthouse-automation
cd ~/lighthouse-automation

# 3. Создайте и активируйте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 4. Установите зависимости
pip install clickhouse-driver PyYAML

# 5. Создайте конфигурационный файл
cat > config.yaml << 'EOF'
clickhouse:
  host: "178.154.220.227"
  port: 9000
  user: "default"
  password: ""
  database: "default"

lighthouse:
  chrome_path: "/usr/bin/google-chrome-stable"

urls_to_audit:
  - "https://example.com"
  - "https://yandex.ru"
ORDER BY date

