import json
import requests
import time

# 飞书配置信息
APP_ID = 'cli_a9c9443f9278dbd6'
APP_SECRET = 'Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4'
APP_TOKEN = 'N42HbN11JaIxxgstE4gcRdl0nPf'
TABLE_ID = 'tbltqXWK6ozCXAXo'

# 获取 tenant_access_token
def get_tenant_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
        'app_id': APP_ID,
        'app_secret': APP_SECRET
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if result.get('code') == 0:
        return result.get('tenant_access_token')
    else:
        raise Exception(f'获取token失败: {result}')

# 添加记录到飞书多维表格
def add_record(access_token, record_data):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=utf-8'
    }

    data = {
        'fields': record_data
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# 批量添加记录
def batch_add_records(access_token, records_list):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/batch_create'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=utf-8'
    }

    # 飞书API限制每次最多500条记录
    batch_size = 500
    all_results = []

    for i in range(0, len(records_list), batch_size):
        batch = records_list[i:i + batch_size]
        data = {
            'records': [{'fields': record} for record in batch]
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        all_results.append(result)

        print(f'已导入 {min(i + batch_size, len(records_list))}/{len(records_list)} 条记录')

        # 避免API限流
        if i + batch_size < len(records_list):
            time.sleep(1)

    return all_results

# 主函数
def main():
    print('开始导入数据到飞书...')

    # 1. 获取access token
    print('1. 获取access token...')
    access_token = get_tenant_access_token()
    print('   ✓ Token获取成功')

    # 2. 读取数据
    print('2. 读取微信文章数据...')
    with open('wechat_articles_data_with_collections.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    print(f'   ✓ 读取到 {len(articles)} 篇文章')

    # 3. 转换数据格式
    print('3. 转换数据格式...')
    records = []
    for article in articles:
        views = article.get('views', 0)
        likes = article.get('likes', 0)
        shares = article.get('shares', 0)

        # 计算点赞率和在看率
        like_rate = round(likes / views * 100, 2) if views > 0 else 0
        share_rate = round(shares / views * 100, 2) if views > 0 else 0

        record = {
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
        records.append(record)
    print(f'   ✓ 数据格式转换完成')

    # 4. 批量导入
    print('4. 批量导入到飞书...')
    results = batch_add_records(access_token, records)

    # 5. 检查结果
    print('\n导入结果：')
    success_count = 0
    fail_count = 0

    for result in results:
        if result.get('code') == 0:
            success_count += len(result.get('data', {}).get('records', []))
        else:
            fail_count += 1
            print(f'   ✗ 批次导入失败: {result}')

    print(f'\n✓ 导入完成！')
    print(f'  - 成功: {success_count} 条')
    print(f'  - 失败: {fail_count} 条')
    print(f'\n表格链接: https://example.feishu.cn/base/{APP_TOKEN}')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'\n✗ 导入失败: {str(e)}')
        import traceback
        traceback.print_exc()
