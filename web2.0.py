import requests
import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

# Ваш VK токен (получите на https://dev.vk.com/)
TOKEN = 'ваш_токен_здесь'
VK_API_VERSION = '5.199'

# Ключевое слово, можно расширить список
QUERY = 'СПбГУ'
MAX_COUNT = 1000  # Максимальное количество постов
BATCH_SIZE = 100  # Количество постов за один запрос (макс. 100)
BASE_URL = 'https://api.vk.com/method/newsfeed.search'

# Структура данных для статистики
stats_by_day = defaultdict(int)
user_ids = set()
likes = comments = reposts = views = 0

# Пагинация и сбор данных
for offset in range(0, MAX_COUNT, BATCH_SIZE):
    params = {
        'q': QUERY,
        'count': BATCH_SIZE,
        'access_token': TOKEN,
        'v': VK_API_VERSION,
        'offset': offset,
    }

    try:
        r = requests.get(BASE_URL, params=params)
        data = r.json().get('response', {}).get('items', [])
        if not data:
            break

        for item in data:
            # Дата публикации
            date = datetime.datetime.fromtimestamp(item['date']).date()
            stats_by_day[date] += 1

            # ID пользователя
            user_ids.add(item.get('from_id'))

            # Статистика взаимодействий
            likes += item.get('likes', {}).get('count', 0)
            comments += item.get('comments', {}).get('count', 0)
            reposts += item.get('reposts', {}).get('count', 0)
            views += item.get('views', {}).get('count', 0)

    except Exception as e:
        print(f"[!] Ошибка запроса: {e}")
        break

# Вывод результатов
print(f"\n📊 Общее количество упоминаний: {sum(stats_by_day.values())}")
print(f"📌 Уникальные пользователи: {len(user_ids)}")
print(f"👍 Всего лайков: {likes}")
print(f"💬 Всего комментариев: {comments}")
print(f"🔁 Всего репостов: {reposts}")
print(f"👁️ Всего просмотров: {views}")

# Визуализация
dates = sorted(stats_by_day.keys())
values = [stats_by_day[date] for date in dates]

plt.figure(figsize=(10, 5))
plt.plot(dates, values, marker='o')
plt.title("Количество публикаций о СПбГУ по дням")
plt.xlabel("Дата")
plt.ylabel("Публикации")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()
