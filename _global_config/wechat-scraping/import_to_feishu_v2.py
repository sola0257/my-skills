import json
import requests
import time
from datetime import datetime

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

# 转换发布时间格式
def convert_publish_time(publish_time_str):
    """将微信的发布时间转换为时间戳（毫秒）"""
    try:
        # 处理不同的时间格式
        if '今天' in publish_time_str:
            # 今天的时间，使用当前日期
            time_part = publish_time_str.replace('今天', '').strip()
            today = datetime.now().strftime('%Y-%m-%d')
            dt_str = f'{today} {time_part}'
            dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        elif '昨天' in publish_time_str:
            # 昨天的时间
            time_part = publish_time_str.replace('昨天', '').strip()
            from datetime import timedelta
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            dt_str = f'{yesterday} {time_part}'
            dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        elif '星期' in publish_time_str:
            # 本周的时间，暂时返回None
            return None
        elif '月' in publish_time_str and '日' in publish_time_str:
            # 格式：01月30日
            parts = publish_time_str.replace('月', '-').replace('日', '').split('-')
            if len(parts) == 2:
                month, day = parts
                year = datetime.now().year
                dt = datetime(year, int(month), int(day))
            else:
                return None
        elif '年' in publish_time_str:
            # 格式：2025年12月31日
            dt_str = publish_time_str.replace('年', '-').replace('月', '-').replace('日', '')
            dt = datetime.strptime(dt_str, '%Y-%m-%d')
        else:
            return None

        # 转换为毫秒时间戳
        return int(dt.timestamp() * 1000)
    except Exception as e:
        print(f'时间转换失败: {publish_time_str}, 错误: {e}')
        return None

# 主函数
def main():
    print('开始导入数据到飞书...\n')

    # 1. 获取access token
    print('1. 获取access token...')
    access_token = get_tenant_access_token()
    print('   ✓ Token获取成功\n')

    # 2. 读取数据
    print('2. 读取微信文章数据...')
    with open('wechat_articles_data_with_collections.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    print(f'   ✓ 读取到 {len(articles)} 篇文章\n')

    # 3. 转换数据格式（映射到飞书表格字段）
    print('3. 转换数据格式...')
    records = []
    for article in articles:
        # 转换发布时间
        publish_timestamp = convert_publish_time(article.get('publishTime', ''))

        record = {
            '发布时间': publish_timestamp,  # 时间戳（毫秒）
            '标题': article.get('title', ''),  # 文章标题
            '平台': '微信公众号',  # 固定值
            '内容类型': article.get('collection_type', ''),  # 文章/图文
            '曝光量': article.get('views', 0),  # 阅读数
            '点击量': article.get('views', 0),  # 使用阅读数
            '互动量': article.get('likes', 0) + article.get('shares', 0) + article.get('favorites', 0) + article.get('comments', 0),  # 总互动
            '合集': article.get('collection_name', ''),  # 合集名称
        }
        records.append(record)
    print(f'   ✓ 数据格式转换完成\n')

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
