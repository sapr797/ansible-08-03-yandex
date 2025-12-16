#!/usr/bin/env python3
"""
Скрипт для автоматического аудита сайтов через Lighthouse
и сохранения результатов в ClickHouse
"""

import subprocess
import json
import os
import sys
import time
import configparser
from datetime import datetime
from clickhouse_driver import Client
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/var/log/lighthouse/audit.log')
    ]
)
logger = logging.getLogger(__name__)

def load_config():
    """Загрузка конфигурации из config.ini"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def setup_database(config):
    """Создание таблицы в ClickHouse"""
    try:
        client = Client(
            host=config['clickhouse']['host'],
            port=int(config['clickhouse'].get('port', 9000)),
            user=config['clickhouse']['user'],
            password=config['clickhouse']['password'],
            database=config['clickhouse']['database']
        )
        
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS lighthouse_audits (
            url String,
            performance Float64,
            accessibility Float64,
            best_practices Float64,
            seo Float64,
            timestamp DateTime DEFAULT now(),
            audit_date Date DEFAULT today()
        ) ENGINE = MergeTree()
        ORDER BY (audit_date, url, timestamp)
        '''
        
        client.execute(create_table_query)
        logger.info("Таблица lighthouse_audits создана или уже существует")
        return True
    except Exception as e:
        logger.error(f"Ошибка при создании таблицы: {e}")
        return False

def run_lighthouse_audit(url, chrome_path='/usr/bin/google-chrome-stable'):
    """Запуск аудита Lighthouse для заданного URL"""
    try:
        logger.info(f"Запуск Lighthouse для {url}")
        
        # Генерируем имя файла отчета
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"/tmp/lighthouse_report_{timestamp}.json"
        
        # Формируем команду
        command = [
            'lighthouse',
            url,
            '--output=json',
            f'--output-path={report_file}',
            '--chrome-flags=--no-sandbox --headless --disable-gpu',
            f'--chrome-path={chrome_path}',
            '--only-categories=performance,accessibility,best-practices,seo',
            '--quiet',
            '--max-wait-for-load=45000'
        ]
        
        # Запускаем Lighthouse
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            logger.error(f"Lighthouse вернул ошибку: {result.stderr[:200]}")
            return None
        
        # Читаем результат
        if os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            # Извлекаем метрики
            scores = {}
            categories = ['performance', 'accessibility', 'best-practices', 'seo']
            
            for category in categories:
                if category in report.get('categories', {}):
                    score = report['categories'][category].get('score', 0)
                    if score is not None:
                        scores[category] = score * 100
                    else:
                        scores[category] = 0
                else:
                    scores[category] = 0
            
            # Удаляем временный файл
            os.remove(report_file)
            
            return {
                'url': url,
                'performance': scores.get('performance', 0),
                'accessibility': scores.get('accessibility', 0),
                'best_practices': scores.get('best-practices', 0),
                'seo': scores.get('seo', 0)
            }
        else:
            logger.error(f"Файл отчета не создан: {report_file}")
            return None
        
    except subprocess.TimeoutExpired:
        logger.error(f"Таймаут при аудите {url}")
        return None
    except Exception as e:
        logger.error(f"Ошибка при аудите {url}: {e}")
        return None

def save_to_clickhouse(data, config):
    """Сохранение результатов в ClickHouse"""
    try:
        client = Client(
            host=config['clickhouse']['host'],
            port=int(config['clickhouse'].get('port', 9000)),
            user=config['clickhouse']['user'],
            password=config['clickhouse']['password'],
            database=config['clickhouse']['database']
        )
        
        insert_query = '''
        INSERT INTO lighthouse_audits (url, performance, accessibility, best_practices, seo)
        VALUES (%(url)s, %(performance)s, %(accessibility)s, %(best_practices)s, %(seo)s)
        '''
        
        client.execute(insert_query, data)
        logger.info(f"Результаты для {data['url']} сохранены в ClickHouse")
        return True
    except Exception as e:
        logger.error(f"Ошибка при сохранении в ClickHouse: {e}")
        return False

def main():
    """Основная функция"""
    logger.info("Начало процесса аудита")
    
    # Загружаем конфигурацию
    config = load_config()
    
    # Список URL для аудита
    sites = config['audit']['sites'].split(',')
    
    # Настраиваем БД
    if not setup_database(config):
        logger.error("Не удалось настроить базу данных")
        return
    
    # Запускаем аудит для каждого URL
    successful = 0
    total = len(sites)
    
    for url in sites:
        url = url.strip()
        logger.info(f"Начинаю аудит: {url}")
        
        # Запускаем аудит
        result = run_lighthouse_audit(url)
        
        if result:
            # Сохраняем результат
            if save_to_clickhouse(result, config):
                successful += 1
                logger.info(f"Аудит {url} завершён успешно")
            else:
                logger.warning(f"Не удалось сохранить результат для {url}")
        else:
            logger.warning(f"Пропускаю {url} из-за ошибки")
        
        # Пауза между запросами
        if url != sites[-1]:
            logger.info("Пауза 10 секунд перед следующим аудитом...")
            time.sleep(10)
    
    logger.info(f"Аудит завершён. Успешно: {successful}/{total}")

if __name__ == "__main__":
    main()
