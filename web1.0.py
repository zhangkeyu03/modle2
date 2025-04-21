import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract
from collections import defaultdict
import time

# Глобальные переменные
visited = set()
broken_links = []
internal_links = set()
external_links = set()
file_links = set()
subdomains = set()
max_pages = 200  # Ограничение количества посещённых страниц

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ['http', 'https']

def crawl(url, base_domain):
    global visited
    if url in visited or len(visited) >= max_pages:
        return
    print(f"[+] Посещаю: {url}")
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print(f"[x] Недоступная ссылка: {url}")
            broken_links.append(url)
            return
    except Exception as e:
        print(f"[!] Ошибка запроса: {url} - {e}")
        broken_links.append(url)
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        full_url = urljoin(url, href)
        if not is_valid_url(full_url):
            continue

        ext = tldextract.extract(full_url)
        base_registered = f"{ext.domain}.{ext.suffix}"

        if base_registered == base_domain:
            internal_links.add(full_url)
            if ext.subdomain and ext.subdomain != 'www':
                subdomains.add(ext.subdomain + '.' + base_registered)
            crawl(full_url, base_domain)
        else:
            external_links.add(full_url)

        # Проверка на ссылку на файл
        if any(full_url.endswith(ext) for ext in ['.pdf', '.doc', '.docx']):
            file_links.add(full_url)

# Точка входа
if __name__ == '__main__':
    start_time = time.time()
    start_url = "https://spbu.ru"
    domain = "spbu.ru"
    crawl(start_url, domain)

    # Вывод результатов
    print("\n --- Результаты ---")
    print(f"Всего посещено страниц: {len(visited)}")
    print(f"Внутренние страницы: {len(internal_links)}")
    print(f"Недоступные страницы: {len(broken_links)}")
    print(f"Поддомены: {len(subdomains)} ({subdomains})")
    print(f"Внешние ссылки: {len(external_links)}")
    print(f"Уникальные ссылки на документы: {len(file_links)}")
    print(f"Время выполнения: {round(time.time() - start_time, 2)} секунд")
