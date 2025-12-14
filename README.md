# Домашнее задание 08-ansible-03-yandex

## Описание
Playbook для установки ClickHouse, Vector и Lighthouse в Яндекс Облаке.

## Инфраструктура
- **ClickHouse**: 51.250.94.16
- **Vector**: 46.21.246.174  
- **Lighthouse**: 89.169.142.63 (ID: fhmbnrd9a7k0mhpof8sf)

## Использование yc cli
```bash
# Подключение к lighthouse
yc compute ssh --id fhmbnrd9a7k0mhpof8sf --identity-file ~/.ssh/yandex_cloud_key --login ubuntu

# Проверка статуса ВМ
yc compute instance get fhmbnrd9a7k0mhpof8sf
Запуск playbook
bash
# Проверка синтаксиса
ansible-playbook site.yml --syntax-check

# Тестовый запуск
ansible-playbook site.yml --check

# Запуск
ansible-playbook site.yml
Используемые модули Ansible
get_url - скачивание Vector

template - настройка конфигураций

apt - установка пакетов

git - клонирование Lighthouse
