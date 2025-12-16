import subprocess
import json
import os
import sys
import time

def check_system():
    print("=" * 60)
    print("ПРОВЕРКА СИСТЕМЫ")
    print("=" * 60)
    
    # Проверка Chrome
    chrome_paths = [
        '/usr/bin/google-chrome-stable',
        '/usr/bin/google-chrome',
        '/usr/bin/chromium-browser',
        '/usr/bin/chromium'
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✓ Найден: {path}")
            try:
                version = subprocess.run([path, '--version'], 
                                       capture_output=True, text=True, timeout=5)
                print(f"  Версия: {version.stdout.strip()}")
                return path
            except:
                print(f"  Не удалось получить версию")
    
    print("✗ Chrome/Chromium не найден")
    return None

def test_lighthouse_simple(url):
    print(f"\n{'='*60}")
    print(f"ТЕСТ LIGHTHOUSE: {url}")
    print(f"{'='*60}")
    
    chrome_path = check_system()
    if not chrome_path:
        print("✗ Chrome не найден, тест прерван")
        return False
    
    try:
        # Простая команда Lighthouse
        cmd = [
            'lighthouse',
            url,
            '--output=json',
            '--output-path=test_report.json',
            '--chrome-flags=--no-sandbox --headless',
            f'--chrome-path={chrome_path}',
            '--only-categories=performance',
            '--quiet'
        ]
        
        print(f"Команда: {' '.join(cmd)}")
        
        # Запуск с таймаутом
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(f"Код возврата: {result.returncode}")
        print(f"STDOUT (первые 500 символов):\n{result.stdout[:500]}")
        print(f"STDERR (первые 500 символов):\n{result.stderr[:500]}")
        
        if result.returncode == 0 and os.path.exists('test_report.json'):
            with open('test_report.json', 'r') as f:
                data = json.load(f)
            
            if 'categories' in data and 'performance' in data['categories']:
                score = data['categories']['performance']['score'] * 100
                print(f"✓ Успех! Performance score: {score}")
                os.remove('test_report.json')
                return True
            else:
                print("✗ Отчет не содержит ожидаемых данных")
        else:
            print("✗ Lighthouse завершился с ошибкой")
            
    except subprocess.TimeoutExpired:
        print("✗ Таймаут (60 секунд)")
    except Exception as e:
        print(f"✗ Исключение: {e}")
    
    return False

def test_direct_chrome():
    print(f"\n{'='*60}")
    print("ПРЯМОЙ ТЕСТ CHROME")
    print(f"{'='*60}")
    
    chrome_path = '/usr/bin/google-chrome-stable'
    if not os.path.exists(chrome_path):
        chrome_path = '/usr/bin/chromium-browser'
    
    if os.path.exists(chrome_path):
        try:
            # Пробуем запустить Chrome напрямую
            cmd = [
                chrome_path,
                '--headless',
                '--no-sandbox',
                '--disable-gpu',
                '--dump-dom',
                'https://example.com'
            ]
            
            print(f"Команда: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            print(f"Код возврата: {result.returncode}")
            print(f"Размер вывода: {len(result.stdout)} символов")
            print(f"Размер ошибок: {len(result.stderr)} символов")
            
            if result.returncode == 0:
                print("✓ Chrome успешно запущен в headless режиме")
                return True
            else:
                print(f"✗ Ошибка Chrome: {result.stderr[:200]}")
        except Exception as e:
            print(f"✗ Исключение: {e}")
    
    return False

def main():
    print("ЗАПУСК ТЕСТОВ LIGHTHOUSE")
    print("=" * 60)
    
    # Тест 1: Проверка Chrome
    if not test_direct_chrome():
        print("\n⚠️ Chrome не запускается, проверьте установку")
        return
    
    # Тест 2: Простой сайт
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ НА ПРОСТОМ САЙТЕ")
    print("="*60)
    
    test_urls = [
        'https://example.com',
        'https://google.com'
    ]
    
    for url in test_urls:
        success = test_lighthouse_simple(url)
        if success:
            print(f"\n✓ Lighthouse работает с {url}")
            break
        else:
            print(f"\n✗ Lighthouse не работает с {url}")
            time.sleep(5)

if __name__ == "__main__":
    main()
