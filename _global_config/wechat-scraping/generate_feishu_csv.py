import json
import csv

# 读取完整数据
with open('wechat_articles_data_with_collections.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# 定义CSV字段
fieldnames = [
    '文章标题',
    '文章链接',
    '发布时间',
    '是否原创',
    '阅读数',
    '点赞数',
    '分享数',
    '收藏数',
    '评论数',
    '点赞率',
    '在看率',
    '合集名称',
    '合集类型',
    '抓取时间'
]

# 生成CSV文件
with open('wechat_articles_complete.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for article in articles:
        # 计算点赞率和在看率
        views = article.get('views', 0)
        likes = article.get('likes', 0)
        shares = article.get('shares', 0)

        like_rate = f'{(likes / views * 100):.2f}%' if views > 0 else '0%'
        share_rate = f'{(shares / views * 100):.2f}%' if views > 0 else '0%'

        row = {
            '文章标题': article.get('title', ''),
            '文章链接': article.get('url', ''),
            '发布时间': article.get('publishTime', ''),
            '是否原创': '是' if article.get('isOriginal') else '否',
            '阅读数': article.get('views', 0),
            '点赞数': article.get('likes', 0),
            '分享数': article.get('shares', 0),
            '收藏数': article.get('favorites', 0),
            '评论数': article.get('comments', 0),
            '点赞率': like_rate,
            '在看率': share_rate,
            '合集名称': article.get('collection_name', ''),
            '合集类型': article.get('collection_type', ''),
            '抓取时间': article.get('extractedAt', '')
        }
        writer.writerow(row)

print(f'成功生成CSV文件，包含 {len(articles)} 篇文章')
print('文件名：wechat_articles_complete.csv')
print('\n字段说明：')
for field in fieldnames:
    print(f'  - {field}')
