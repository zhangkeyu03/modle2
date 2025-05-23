# Python Сканер Веб-сайтов

Этот проект представляет собой простой и эффективный инструмент на Python для сканирования веб-сайтов. Он автоматически обходит внутренние и внешние ссылки, находит неработающие страницы, поддомены и ссылки на документы.

## Описание

Сканер:
- посещает страницы сайта (до 200 по умолчанию)
- собирает внутренние и внешние ссылки
- определяет поддомены
- выявляет неработающие (broken) ссылки
- находит документы (.pdf, .doc, .docx)

## Используемые библиотеки

- `requests` — для отправки HTTP-запросов
- `BeautifulSoup` (`bs4`) — для парсинга HTML
- `urllib.parse` — для обработки URL-адресов
- `tldextract` — для извлечения доменной зоны

Установка зависимостей:

```bash
pip install requests beautifulsoup4 tldextract
```

## Как использовать

1. Убедитесь, что у вас установлен Python 3.6+
2. Клонируйте репозиторий или скачайте `.py` файл
3. Запустите скрипт:

```bash
python web1.0.py
```

(в коде уже установлен сайт по умолчанию: `https://spbu.ru`)

## Изменение стартового сайта

Чтобы сканировать другой сайт, измените в коде:

```python
start_url = "https://spbu.ru"
domain = "spbu.ru"
```

## Выходные данные

После выполнения программа выведет:

- Всего посещено страниц
- Количество внутренних ссылок
- Количество неработающих страниц
- Найденные поддомены
- Внешние ссылки
- Документы (.pdf, .doc, .docx)
- Общее время выполнения

## Пример вывода

```
[+] Посещаю: https://spbu.ru
...

 --- Результаты ---
Всего посещено страниц: 173
Внутренние страницы: 132
Недоступные страницы: 9
Поддомены: 2 ({'news.spbu.ru', 'admission.spbu.ru'})
Внешние ссылки: 26
Уникальные ссылки на документы: 7
Время выполнения: 43.27 секунд
```

## Лицензия

Проект доступен под лицензией MIT.
