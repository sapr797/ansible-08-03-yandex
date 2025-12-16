#!/usr/bin/env python3
"""
Скрипт для автоматического аудита сайтов Lighthouse и отправки результатов в ClickHouse
"""

import subprocess
import json
import sys
import os
from datetime import datetime
from clickhouse_driver import Client
import yaml
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
       # logging.FileHandler('/var/log/lighthouse_automation.log'),
        logging.FileHandler(os.path.expanduser('~/lighthouse_automation.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LighthouseToClickHouse:
    def __init__(self, config_path='config.yaml'):
        """Инициализация с загрузкой конфигурации"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.clickhouse_client = Client(
            host=self.config['clickhouse']['host'],
            port=self.config['clickhouse'].get('port', 9000),
            user=self.config['clickhouse'].get('user', 'default'),
            password=self.config['clickhouse'].get('password', ''),
            database=self.config['clickhouse'].get('database', 'default')
        )
        
        # Создаём таблицу, если её нет
        self._create_table()
    
    def _create_table(self):
        """Создание таблицы в ClickHouse для хранения метрик"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS lighthouse_audits (
            audit_date DateTime DEFAULT now(),
            url String,
            performance Float32,
            accessibility Float32,
            best_practices Float32,
            seo Float32,
            pwa Float32,
            first_contentful_paint Float32,
            largest_contentful_paint Float32,
            total_blocking_time Float32,
            cumulative_layout_shift Float32,
            speed_index Float32,
            server_response_time Float32,
            total_audit_duration Float32,
            raw_report String
        ) ENGINE = MergeTree()
        ORDER BY (audit_date, url)
        """
        try:
            self.clickhouse_client.execute(create_table_query)
            logger.info("Таблица lighthouse_audits создана или уже существует")
        except Exception as e:
            logger.error(f"Ошибка при создании таблицы: {e}")
    
    def run_lighthouse(self, url, output_dir='./reports'):
        """Запуск Lighthouse для указанного URL"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_url = url.replace('https://', '').replace('http://', '').replace('/', '_')[:50]
        json_filename = f"{output_dir}/{safe_url}_{timestamp}.json"
        html_filename = f"{output_dir}/{safe_url}_{timestamp}.html"
        
        # Команда запуска Lighthouse
        cmd = [
            'lighthouse',
            url,
            '--chrome-path', self.config['lighthouse']['chrome_path'],
            '--chrome-flags', '--no-sandbox --headless --disable-dev-shm-usage --disable-gpu',
            '--output', 'json',
            '--output', 'html',
            '--output-path', json_filename.replace('.json', ''),
            '--quiet',
            '--no-enable-error-reporting'
        ]
        
        # if 'extra_flags' in self.config['lighthouse']:
         #    cmd.extend(self.config['lighthouse']['extra_flags'])
        
        logger.info(f"Запуск Lighthouse для {url}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                logger.error(f"Lighthouse вернул ошибку: {result.stderr}")
                return None
            
            # Загружаем JSON-отчёт
            with open(json_filename, 'r') as f:
                report = json.load(f)
            
            logger.info(f"Аудит завершён. Отчёт сохранён: {html_filename}")
            return report, html_filename
            
        except subprocess.TimeoutExpired:
            logger.error(f"Таймаут при аудите {url}")
            return None
        except Exception as e:
            logger.error(f"Ошибка при запуске Lighthouse: {e}")
            return None
    
    def extract_metrics(self, report):
        """Извлечение ключевых метрик из отчёта Lighthouse"""
        try:
            categories = report.get('categories', {})
            audits = report.get('audits', {})
            
            metrics = {
                'url': report.get('finalUrl', ''),
                'performance': categories.get('performance', {}).get('score', 0) * 100,
                'accessibility': categories.get('accessibility', {}).get('score', 0) * 100,
                'best_practices': categories.get('best-practices', {}).get('score', 0) * 100,
                'seo': categories.get('seo', {}).get('score', 0) * 100,
                'pwa': categories.get('pwa', {}).get('score', 0) * 100,
                'first_contentful_paint': audits.get('first-contentful-paint', {}).get('numericValue', 0),
                'largest_contentful_paint': audits.get('largest-contentful-paint', {}).get('numericValue', 0),
                'total_blocking_time': audits.get('total-blocking-time', {}).get('numericValue', 0),
                'cumulative_layout_shift': audits.get('cumulative-layout-shift', {}).get('numericValue', 0),
                'speed_index': audits.get('speed-index', {}).get('numericValue', 0),
                'server_response_time': audits.get('server-response-time', {}).get('numericValue', 0),
                'total_audit_duration': report.get('timing', {}).get('total', 0)
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Ошибка при извлечении метрик: {e}")
            return None
    
    def send_to_clickhouse(self, metrics, raw_report_json):
        """Отправка метрик в ClickHouse"""
        if not metrics:
            return False
        
        insert_query = """
        INSERT INTO lighthouse_audits (
            url, performance, accessibility, best_practices, seo, pwa,
            first_contentful_paint, largest_contentful_paint, total_blocking_time,
            cumulative_layout_shift, speed_index, server_response_time,
            total_audit_duration, raw_report
        ) VALUES
        """
        
        values = [
            metrics['url'],
            metrics['performance'],
            metrics['accessibility'],
            metrics['best_practices'],
            metrics['seo'],
            metrics['pwa'],
            metrics['first_contentful_paint'],
            metrics['largest_contentful_paint'],
            metrics['total_blocking_time'],
            metrics['cumulative_layout_shift'],
            metrics['speed_index'],
            metrics['server_response_time'],
            metrics['total_audit_duration'],
            json.dumps(raw_report_json)  # Сохраняем полный отчёт как JSON строку
        ]
        
        try:
            self.clickhouse_client.execute(
                insert_query,
                [values]
            )
            logger.info(f"Метрики для {metrics['url']} отправлены в ClickHouse")
            return True
        except Exception as e:
            logger.error(f"Ошибка при отправке в ClickHouse: {e}")
            return False
    
    def audit_urls(self, urls=None):
        """Аудит списка URL"""
        if urls is None:
            urls = self.config['urls_to_audit']
        
        results = []
        for url in urls:
            logger.info(f"Начинаю аудит: {url}")
            
            # Запускаем Lighthouse
            result = self.run_lighthouse(url)
            if not result:
                logger.warning(f"Пропускаю {url} из-за ошибки")
                continue
            
            report, html_path = result
            
            # Извлекаем метрики
            metrics = self.extract_metrics(report)
            if not metrics:
                logger.warning(f"Не удалось извлечь метрики для {url}")
                continue
            
            # Отправляем в ClickHouse
            if self.send_to_clickhouse(metrics, report):
                results.append({
                    'url': url,
                    'success': True,
                    'html_report': html_path,
                    'metrics': metrics
                })
            else:
                results.append({
                    'url': url,
                    'success': False,
                    'error': 'ClickHouse insert failed'
                })
        
        return results

def main():
    """Основная функция"""
    # Проверяем аргументы командной строки
    config_path = 'config.yaml'
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    if not os.path.exists(config_path):
        logger.error(f"Конфигурационный файл не найден: {config_path}")
        print(f"Создайте конфигурационный файл на основе config.example.yaml")
        sys.exit(1)
    
    # Запускаем аудитор
    auditor = LighthouseToClickHouse(config_path)
    
    # Получаем URL для аудита (можно передать через аргументы)
    urls_to_audit = None
    if len(sys.argv) > 2:
        urls_to_audit = sys.argv[2:]
    
    results = auditor.audit_urls(urls_to_audit)
    
    # Вывод краткой статистики
    successful = sum(1 for r in results if r['success'])
    logger.info(f"Аудит завершён. Успешно: {successful}/{len(results)}")
    
    for result in results:
        if result['success']:
            m = result['metrics']
            logger.info(
                f"{result['url']}: "
                f"Perf={m['performance']:.1f}, "
                f"Access={m['accessibility']:.1f}, "
                f"SEO={m['seo']:.1f}"
            )
        else:
            logger.warning(f"{result['url']}: FAILED - {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
