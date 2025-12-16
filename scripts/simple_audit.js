// Минимальный рабочий скрипт Lighthouse
const chromeLauncher = require('chrome-launcher');
const lighthouse = require('lighthouse');

async function main() {
  const url = process.argv[2] || 'https://example.com';
  console.log(`Запуск Lighthouse для ${url}...`);
  
  try {
    // Запускаем Chrome
    const chrome = await chromeLauncher.launch({
      chromeFlags: ['--headless', '--no-sandbox']
    });
    
    console.log(`Chrome запущен (порт: ${chrome.port})`);
    
    // Опции аудита
    const options = {
      output: 'json',
      port: chrome.port,
      onlyCategories: ['performance']
    };
    
    // Запускаем Lighthouse
    const results = await lighthouse(url, options);
    
    // Выводим результат
    const score = results.lhr.categories.performance.score * 100;
    console.log(`Performance score: ${score.toFixed(1)}`);
    
    // Закрываем Chrome
    await chrome.kill();
    console.log('Готово!');
    
  } catch (error) {
    console.error('Ошибка:', error.message);
  }
}

main();
