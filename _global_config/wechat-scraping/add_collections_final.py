import json

# Collection mappings extracted from screenshots
# Format: {title_pattern: {'collection_name': str, 'collection_type': str}}
collection_mappings = {
    # 绿植软装 (文章)
    '室内空气差？这5种植物堪称天然净化器': {'collection_name': '绿植软装', 'collection_type': '文章'},
    '卧室放绿植，治愈还是致郁？': {'collection_name': '绿植软装', 'collection_type': '文章'},
    '卧室做绿植，治愈还是"致郁"？': {'collection_name': '绿植软装', 'collection_type': '文章'},

    # 欣赏 (图文)
    '立春赏花图鉴：把春天最早的消息带给你': {'collection_name': '欣赏', 'collection_type': '图文'},
    '累了吗？给眼睛做个绿色SPA': {'collection_name': '欣赏', 'collection_type': '图文'},
    '累了吗？给眼睛做个"绿色SPA"': {'collection_name': '欣赏', 'collection_type': '图文'},

    # 节气与绿植 (文章)
    '立春至，3个小仪式唤醒沉睡的植物与生活热爱': {'collection_name': '节气与绿植', 'collection_type': '文章'},

    # 年宵花 (文章)
    '春节必备！精选年宵花，让喜庆持续到正月十五': {'collection_name': '年宵花', 'collection_type': '文章'},
    '新春好运来！5种年宵花寓意大揭秘，让家宅旺气满满！': {'collection_name': '年宵花', 'collection_type': '文章'},
    '春节送礼攻略：别送烟酒了，这5盆"吉利花"长辈更喜欢': {'collection_name': '年宵花', 'collection_type': '文章'},

    # 修剪整形 (文章)
    '手把手教你修剪龟背竹气生根，三招打造茁壮植株，新手也能轻松上手！': {'collection_name': '修剪整形', 'collection_type': '文章'},
    '一盆变十盆：4种常见植物的扦插技巧': {'collection_name': '修剪整形', 'collection_type': '文章'},

    # 城市绿洲 (文章)
    '慢养四季：在城市中心种下一片节气花园': {'collection_name': '城市绿洲', 'collection_type': '文章'},
    '慢养四季 | 大棚动工，都市绿洲正在成长': {'collection_name': '城市绿洲', 'collection_type': '文章'},

    # 知识分享 (图文)
    '冬季施肥必看！3大常见错误，你中招了吗？': {'collection_name': '知识分享', 'collection_type': '图文'},
    '"望闻问切"四招，轻松辨别植物需水': {'collection_name': '知识分享', 'collection_type': '图文'},
    '你买回家的不是"永久花"，是时间的胶囊': {'collection_name': '知识分享', 'collection_type': '图文'},
    '慢养四季：新手植愈系养护指南': {'collection_name': '知识分享', 'collection_type': '图文'},

    # 阳台种植 (文章)
    '阳台春季种植规划指南：从选址到配置': {'collection_name': '阳台种植', 'collection_type': '文章'},
    '春日阳台变菜园，超实用准备攻略': {'collection_name': '阳台种植', 'collection_type': '文章'},
    '北京阳台全年种养日历：12个月该种什么，一篇说清': {'collection_name': '阳台种植', 'collection_type': '文章'},

    # #智能园艺 (文章)
    '养花杀手逆袭指南！你的24小时「植物急诊室」上线了！': {'collection_name': '#智能园艺', 'collection_type': '文章'},
}

# Read existing data
with open('wechat_articles_data_with_stats.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Function to normalize title for matching (remove emojis, extra spaces, quotes)
def normalize_title(title):
    import re
    # Remove emojis
    title = re.sub(r'[^\w\s\u4e00-\u9fff，。！？：；、""''（）《》【】…—·]', '', title)
    # Normalize quotes
    title = title.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")
    # Remove extra spaces
    title = ' '.join(title.split())
    return title.strip()

# Add collection information to articles
updated_count = 0
matched_articles = []

for article in articles:
    title = article['title']
    normalized_title = normalize_title(title)

    # Try exact match first
    if title in collection_mappings:
        article['collection_name'] = collection_mappings[title]['collection_name']
        article['collection_type'] = collection_mappings[title]['collection_type']
        updated_count += 1
        matched_articles.append(title)
    else:
        # Try normalized match
        matched = False
        for pattern, collection_info in collection_mappings.items():
            if normalize_title(pattern) == normalized_title:
                article['collection_name'] = collection_info['collection_name']
                article['collection_type'] = collection_info['collection_type']
                updated_count += 1
                matched_articles.append(title)
                matched = True
                break

        if not matched:
            # Assign remaining articles to 养护技巧 (Maintenance Tips) collection
            # These are general plant care articles that don't fit other specific collections
            article['collection_name'] = '养护技巧'
            article['collection_type'] = '文章'

# Save updated data
with open('wechat_articles_data_with_collections.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f'Successfully added collection information to all {len(articles)} articles')
print(f'\nCollection distribution:')

# Count articles by collection
from collections import Counter
collection_counts = Counter([a['collection_name'] for a in articles])
for collection_name, count in sorted(collection_counts.items()):
    collection_type = next(a['collection_type'] for a in articles if a['collection_name'] == collection_name)
    print(f'  {collection_name} ({collection_type}): {count} articles')
