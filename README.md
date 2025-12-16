
# Lighthouse Automation with Ansible

Проект по автоматизации аудита веб-сайтов с помощью Google Lighthouse, сохранению результатов в ClickHouse и настройке всей инфраструктуры через Ansible.

## 📁 Структура проекта
lighthouse-automation/
├── ansible/ # Ansible плейбуки
│ ├── prod.yml # Production настройка всей системы
│ ├── site.yml # Базовая установка Lighthouse + Nginx
│ └── templates/ # Шаблоны Jinja2
│ ├── lighthouse.service.j2 # Systemd сервис
│ └── lighthouse_audit.py.j2 # Шаблон скрипта аудита
├── scripts/ # Рабочие скрипты
│ ├── lighthouse_audit.py # Основной скрипт аудита (рабочая версия)
│ ├── lighthouse_to_clickhouse.py # Оригинальный скрипт
│ └── simple_audit.js # Простой пример на JavaScript
├── configs/ # Конфигурационные файлы
│ ├── config.ini # Активная конфигурация
│ ├── config.yaml # Пример конфигурации YAML
│ └── requirements.txt # Зависимости Python
├── reports/ # Примеры отчётов (тестовые)
├── README.md # Этот файл
└── .ansible-lint # Конфигурация линтера Ansible

text

## 🎯 Возможности системы

- ✅ **Автоматический аудит** сайтов с помощью Google Lighthouse
- ✅ **Сохранение результатов** в базу данных ClickHouse
- ✅ **Планирование задач** через systemd и cron
- ✅ **Централизованное логирование**
- ✅ **Идемпотентные плейбуки Ansible**
- ✅ **Поддержка многокомпонентной архитектуры** (Lighthouse + ClickHouse)

## 🚀 Быстрый старт

### 1. Клонирование и настройка
```bash
git clone https://github.com/sapr797/ansible-08-03-yandex.git
cd ansible-08-03-yandex/lighthouse-automation
2. Настройка инфраструктуры через Ansible
bash
# Настройка production-системы (Lighthouse + зависимости)
ansible-playbook prod.yml --diff

# Базовая установка Lighthouse с Nginx
ansible-playbook site.yml --diff
3. Ручной запуск аудита
bash
cd scripts
python lighthouse_audit.py
⚙️ Конфигурация
Файл configs/config.ini
ini
[clickhouse]
host = clickhous          # Имя или IP сервера ClickHouse
port = 9000
user = default
password = 
database = default

[audit]
sites = https://voronezh.poryadok.ru, https://krasnodar.poryadok.ru, https://poryadok.ru
interval_hours = 24
timeout_seconds = 120
Переменные Ansible (prod.yml)
yaml
vars:
  lighthouse_user: lighthouse
  lighthouse_dir: /opt/lighthouse
  audit_sites:
    - https://voronezh.poryadok.ru
    - https://krasnodar.poryadok.ru
    - https://poryadok.ru
📊 Мониторинг и проверка
Проверка статуса системы
bash
# Статус сервиса Lighthouse
systemctl status lighthouse.service

# Просмотр логов
tail -f /var/log/lighthouse/audit.log

# Проверка cron-задачи
cat /etc/cron.d/lighthouse_audit
Запросы к ClickHouse
sql
-- Последние 5 аудитов
SELECT * FROM lighthouse_audits ORDER BY audit_timestamp DESC LIMIT 5;

-- Средняя производительность по сайтам
SELECT 
  url,
  AVG(performance_score) as avg_performance,
  COUNT(*) as audit_count
FROM lighthouse_audits 
GROUP BY url
ORDER BY avg_performance DESC;
✅ Выполнение задания
Проект содержит все необходимые компоненты:

Ansible плейбуки (prod.yml, site.yml) ✓

Инвентаризация (явная или неявная через localhost) ✓

Шаблоны для systemd и конфигураций ✓

Рабочие скрипты для аудита Lighthouse ✓

Конфигурационные файлы ✓

Идемпотентность проверена через --check --diff ✓

Ansible-lint пройден ✓

Полная документация в README.md ✓

🏷️ Тег задания
Коммит помечен тегом 08-ansible-03-yandex в соответствии с заданием.

Ссылка на репозиторий: https://github.com/sapr797/ansible-08-03-yandex

Ссылка на тег: https://github.com/sapr797/ansible-08-03-yandex/tree/08-ansible-03-yandex

⚠️ Решение проблем
Проблема	Решение
Ошибка подключения к ClickHouse	Проверить listen_host в /etc/clickhouse-server/config.xml
lighthouse is not a function	Использовать правильный импорт: const lighthouse = require('lighthouse')
Конфликт пакетов nodejs/npm	Использовать NVM для управления версиями Node.js
Сервис не находится systemd	Выполнить systemctl daemon-reload
📄 Лицензия
Проект распространяется под лицензией MIT.

text

## 📤 Шаги для загрузки в репозиторий

```bash
# 1. Добавьте новые файлы в Git
git add scripts/ configs/ README.md

# 2. Создайте коммит
git commit -m "Добавление рабочих скриптов и конфигураций для Lighthouse Automation"

# 3. Создайте и запушьте тег (если ещё не создан)
git tag 08-ansible-03-yandex
git push origin main --tags

# 4. Или обновите существующий тег
git tag -f 08-ansible-03-yandex
git push -f origin main --tags
