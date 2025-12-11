# Ansible проект для развертывания ClickHouse, Vector и LightHouse

## Архитектура
- **ClickHouse**: 178.154.201.166 (аналитическая СУБД)
- **Vector**: 158.160.62.159 (система сбора и обработки логов)
- **LightHouse**: 62.84.126.14:8080 (веб-интерфейс)

## Структура проекта
ans-project/
├── inventory/
│ └── production.yml # Конфигурация хостов
├── playbooks/
│ ├── clickhouse.yml # Установка ClickHouse
│ ├── vector.yml # Установка Vector
│ ├── lighthouse.yml # Установка LightHouse
│ └── setup-all.yml # Установка всех компонентов
├── templates/ # Шаблоны конфигураций
├── ansible.cfg # Конфигурация Ansible
└── README.md # Документация

text

## Инвентарь
```yaml
all:
  hosts:
    clickhouse:
      ansible_host: 178.154.201.166
      ansible_user: ubuntu
    vector:
      ansible_host: 158.160.62.159
      ansible_user: ubuntu
    lighthouse:
      ansible_host: localhost
      ansible_connection: local
Использование
1. Проверка доступности хостов
bash
ansible all -m ping
2. Установка всех компонентов
bash
ansible-playbook playbooks/setup-all.yml
3. Установка отдельных компонентов
bash
# Установка ClickHouse
ansible-playbook playbooks/clickhouse.yml

# Установка Vector
ansible-playbook playbooks/vector.yml

# Установка LightHouse
ansible-playbook playbooks/lighthouse.yml
4. Проверка состояния
bash
# Проверить LightHouse
curl http://localhost:8080/

# Проверить ClickHouse (после установки)
ssh ubuntu@178.154.201.166 "clickhouse-client --query='SELECT version()'"

# Проверить Vector (после установки)
ssh ubuntu@158.160.62.159 "vector --version"
Порты
LightHouse: 8080

ClickHouse: 8123 (HTTP), 9000 (TCP)

Vector: 8686 (метрики)

Мониторинг
LightHouse доступен по HTTP на порту 8080

Все компоненты имеют systemd службы
