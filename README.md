# Домашнее задание 08-ansible-03-yandex

## Описание
Playbook устанавливает и настраивает:
1. ClickHouse - СУБД
2. Vector - сборщик логов  
3. Lighthouse - веб-интерфейс для ClickHouse

## Использованные модули
- `apt` - установка пакетов
- `get_url` - скачивание Vector
- `git` - клонирование Lighthouse
- `template` - настройка Nginx
- `systemd` - управление сервисами

## Запуск
```bash
ansible-playbook site.yml --check
ansible-playbook site.yml --diff
ansible-playbook site.yml
