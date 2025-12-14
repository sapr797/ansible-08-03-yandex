# Домашнее задание к занятию 3 «Использование Ansible»

## Описание Playbook

Этот playbook устанавливает и настраивает три компонента инфраструктуры:

1. **ClickHouse** - колоночная система управления базами данных
2. **Vector** - инструмент для сбора и обработки логов
3. **Lighthouse** - легковесный веб-интерфейс для ClickHouse

## Параметры и теги

Playbook состоит из трёх отдельных плейов:
- `Install ClickHouse` - для группы хостов `clickhouse`
- `Install Vector` - для группы хостов `vector`
- `Install and Configure Lighthouse` - для группы хостов `lighthouse`

Для выборочного запуска используйте теги:
```bash
ansible-playbook site.yml --tags clickhouse
ansible-playbook site.yml --tags vector
ansible-playbook site.yml --tags lighthouse
Используемые модули
При создании tasks использованы модули:

get_url - для скачивания пакета Vector

template - для настройки конфигурации Nginx

apt - для установки пакетов на Ubuntu/Debian

git - для клонирования репозитория Lighthouse

systemd - для управления сервисами

Inventory
Inventory файл inventory/prod.yml содержит три группы хостов:

clickhouse - для сервера ClickHouse

vector - для агента сбора логов

lighthouse - для веб-интерфейса

Запуск и проверка
Проверка синтаксиса:
bash
ansible-playbook site.yml --syntax-check
Проверка в режиме dry-run:
bash
ansible-playbook site.yml --check
Запуск с отображением изменений:
bash
ansible-playbook site.yml --diff
Полный запуск:
bash
ansible-playbook site.yml
Проверка идемпотентности:
bash
# Первый запуск
ansible-playbook site.yml --diff

# Повторный запуск (должно быть 0 изменений)
ansible-playbook site.yml --diff
Структура проекта
text
ansible-hw-03/
├── site.yml                          # Основной playbook
├── README.md                         # Документация
├── ansible.cfg                       # Конфигурация Ansible
├── inventory/
│   └── prod.yml                      # Inventory файл
└── templates/
    └── lighthouse-nginx.conf.j2      # Шаблон конфига Nginx
Идемпотентность
Playbook разработан с учетом принципа идемпотентности - повторный запуск не вносит изменений в систему, если конфигурация не менялась.
