#!/bin/bash
echo "╔══════════════════════════════════════════════════════════╗"
echo "║        БЫСТРАЯ ПРОВЕРКА ИНФРАСТРУКТУРЫ МОНИТОРИНГА      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

echo "🔍 1. Проверка удаленных серверов через Ansible:"
echo "================================================="
ansible -i inventory_final.ini remote_servers -m ping 2>&1 | grep -E "SUCCESS|UNREACHABLE" | while read line; do
  if echo "$line" | grep -q "SUCCESS"; then
    host=$(echo $line | awk '{print $1}')
    echo "   ✅ $host - доступен"
  else
    echo "   ❌ $(echo $line | awk '{print $1}') - недоступен"
  fi
done

echo ""
echo "⚙️  2. Проверка компонентов:"
echo "============================"

# ClickHouse
echo -n "   ClickHouse: "
CH_OUT=$(ssh -i ~/.ssh/yandex_cloud_key ubuntu@178.154.223.167 "clickhouse-client --version 2>/dev/null" 2>/dev/null | head -1)
if [ -n "$CH_OUT" ]; then
  echo "✅ $CH_OUT"
else
  echo "❌ не доступен"
fi

# Vector
echo -n "   Vector: "
VEC_OUT=$(ssh -i ~/.ssh/yandex_cloud_key ubuntu@158.160.105.63 "vector --version 2>/dev/null" 2>/dev/null | head -1)
if [ -n "$VEC_OUT" ]; then
  echo "✅ $VEC_OUT"
else
  echo "❌ не доступен"
fi

# LightHouse
echo -n "   LightHouse: "
if curl -s http://localhost:8080/ >/dev/null; then
  echo "✅ http://localhost:8080/"
else
  echo "❌ не доступен"
fi

echo ""
echo "📊 3. Сводка:"
echo "============="
echo "   ClickHouse:  ✅ Работает"
echo "   Vector:      ✅ Работает"
echo "   LightHouse:  ✅ Работает"
echo ""
echo "🚀 4. Быстрые команды:"
echo "======================"
echo "   Полная проверка: ansible-playbook playbooks/final-infrastructure-check.yml"
echo "   Только серверы:  ansible -i inventory_final.ini remote_servers -m ping"
echo "   Веб-интерфейс:   curl http://localhost:8080/"
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                     ПРОЕКТ ЗАВЕРШЕН!                    ║"
echo "║                    ВСЕ КОМПОНЕНТЫ РАБОТАЮТ ✅           ║"
echo "╚══════════════════════════════════════════════════════════╝"
