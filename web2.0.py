import requests
import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

# 你的 VK token
TOKEN = '在https://dev.vk.com/创建获取'
VK_API_VERSION = '5.199'

# 关键词，可以扩展为多个
QUERY = 'СПбГУ'
MAX_COUNT = 1000  # 总条数上限（建议分批）
BATCH_SIZE = 100  # 每次请求数量（最多100）
BASE_URL = 'https://api.vk.com/method/newsfeed.search'

# 统计数据结构
stats_by_day = defaultdict(int)
user_ids = set()
likes = comments = reposts = views = 0

# 分页获取数据
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
            # 日期
            date = datetime.datetime.fromtimestamp(item['date']).date()
            stats_by_day[date] += 1

            # 用户ID
            user_ids.add(item.get('from_id'))

            # 互动统计
            likes += item.get('likes', {}).get('count', 0)
            comments += item.get('comments', {}).get('count', 0)
            reposts += item.get('reposts', {}).get('count', 0)
            views += item.get('views', {}).get('count', 0)

    except Exception as e:
        print(f"[!] 请求失败: {e}")
        break

# 输出结果
print(f"\n📊 总提及数：{sum(stats_by_day.values())}")
print(f"📌 发布用户数：{len(user_ids)}")
print(f"👍 总点赞数：{likes}")
print(f"💬 总评论数：{comments}")
print(f"🔁 总转发数：{reposts}")
print(f"👁️ 总浏览数：{views}")

# 画图
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
