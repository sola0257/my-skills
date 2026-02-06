#!/usr/bin/env python3
"""
列出所有记录，检查是否有重复
"""

import requests
import json

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

def main():
    print("=== 所有记录列表 ===\n")

    access_token = get_tenant_access_token()
    records = list_all_records(access_token)

    print(f"共 {len(records)} 条记录\n")
    print("="*80)

    # 按标题排序，方便查看重复
    records_sorted = sorted(records, key=lambda r: r['fields'].get('标题', ''))

    for i, record in enumerate(records_sorted, 1):
        fields = record['fields']
        title = fields.get('标题', '无标题')
        file_path = fields.get('本地文件路径', '无')
        views = fields.get('曝光量', '无')
        platform = fields.get('平台', '无')

        print(f"{i}. {title}")
        print(f"   ID: {record['record_id']}")
        print(f"   平台: {platform}")
        print(f"   路径: {file_path}")
        print(f"   曝光量: {views}")
        print()

if __name__ == '__main__':
    main()
