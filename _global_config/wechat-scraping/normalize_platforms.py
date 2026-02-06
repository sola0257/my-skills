#!/usr/bin/env python3
"""
检查并统一平台命名
"""

import requests
from collections import Counter

APP_ID = 'cli_a9c9443f9278dbd6'
APP_SECRET = 'Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4'
APP_TOKEN = 'N42HbN11JaIxxgstE4gcRdl0nPf'
TABLE_ID = 'tbltqXWK6ozCXAXo'

def get_tenant_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    data = {'app_id': APP_ID, 'app_secret': APP_SECRET}
    response = requests.post(url, json=data)
    result = response.json()
    if result.get('code') == 0:
        return result['tenant_access_token']
    else:
        raise Exception(f"获取token失败: {result}")

def list_all_records(access_token):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records'
    headers = {'Authorization': f'Bearer {access_token}'}

    all_records = []
    page_token = None

    while True:
        params = {'page_size': 500}
        if page_token:
            params['page_token'] = page_token

        response = requests.get(url, headers=headers, params=params)
        result = response.json()

        if result.get('code') == 0:
            items = result.get('data', {}).get('items', [])
            all_records.extend(items)
            page_token = result.get('data', {}).get('page_token')
            if not page_token:
                break
        else:
            raise Exception(f"获取记录失败: {result}")

    return all_records

def update_record(access_token, record_id, fields):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {'fields': fields}
    response = requests.put(url, headers=headers, json=data)
    return response.json()

def main():
    print("=== 平台字段统一规范 ===\n")

    access_token = get_tenant_access_token()
    print("✓ 获取访问令牌成功\n")

    records = list_all_records(access_token)
    print(f"✓ 共 {len(records)} 条记录\n")

    # 统计当前平台分布
    platforms = [r['fields'].get('平台', '未知') for r in records]
    platform_counts = Counter(platforms)

    print("当前平台分布:")
    for platform, count in platform_counts.items():
        print(f"  - {platform}: {count}条")

    print("\n" + "="*50)
    print("建议的平台命名规范:")
    print("  - 微信公众号-订阅号")
    print("  - 微信公众号-服务号")
    print("  - 视频号")
    print("="*50)

    # 统一平台命名
    print("\n开始统一平台命名...")

    platform_mapping = {
        '微信公众号': '微信公众号-订阅号',  # 默认订阅号
        '微信公众号-订阅号': '微信公众号-订阅号',  # 保持不变
    }

    updated_count = 0
    for record in records:
        current_platform = record['fields'].get('平台', '')

        if current_platform in platform_mapping:
            new_platform = platform_mapping[current_platform]

            if current_platform != new_platform:
                print(f"\n更新记录: {record['record_id']}")
                print(f"  标题: {record['fields'].get('标题', '无')}")
                print(f"  {current_platform} → {new_platform}")

                result = update_record(access_token, record['record_id'], {
                    '平台': new_platform
                })

                if result.get('code') == 0:
                    print(f"  ✓ 更新成功")
                    updated_count += 1
                else:
                    print(f"  ✗ 更新失败: {result}")

    print(f"\n✓ 完成！共更新 {updated_count} 条记录")

    # 再次统计
    records = list_all_records(access_token)
    platforms = [r['fields'].get('平台', '未知') for r in records]
    platform_counts = Counter(platforms)

    print("\n更新后的平台分布:")
    for platform, count in platform_counts.items():
        print(f"  - {platform}: {count}条")

if __name__ == '__main__':
    main()
