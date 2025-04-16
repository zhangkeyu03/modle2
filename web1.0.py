import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract
from collections import defaultdict
import time

# 设置全局变量
visited = set()
broken_links = []
internal_links = set()
external_links = set()
file_links = set()
subdomains = set()
max_pages = 200  # 限制访问页面数，防止爬爆

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ['http', 'https']

def crawl(url, base_domain):
    global visited
    if url in visited or len(visited) >= max_pages:
        return
    print(f"[+] 访问：{url}")
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print(f"[x] 失效链接：{url}")
            broken_links.append(url)
            return
    except Exception as e:
        print(f"[!] 请求错误：{url} - {e}")
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

        # 检查是否是文件链接
        if any(full_url.endswith(ext) for ext in ['.pdf', '.doc', '.docx']):
            file_links.add(full_url)

# 主入口
if __name__ == '__main__':
    start_time = time.time()
    start_url = "https://spbu.ru"
    domain = "spbu.ru"
    crawl(start_url, domain)

    # 输出统计结果
    print("\n --- 统计结果 ---")
    print(f"总访问页面数: {len(visited)}")
    print(f"内部页面数: {len(internal_links)}")
    print(f"失效页面数: {len(broken_links)}")
    print(f"子域名数: {len(subdomains)} ({subdomains})")
    print(f"外部链接数: {len(external_links)}")
    print(f"唯一文档链接数: {len(file_links)}")
    print(f"耗时：{round(time.time() - start_time, 2)} 秒")
