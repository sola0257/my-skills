#!/usr/bin/env python3
"""
正确的重复记录处理逻辑：
1. 保留无路径的记录（从后台抓取的准确数据）
2. 把有路径记录的"本地文件路径"复制到无路径记录
3. 删除有路径的记录
"""

import requests
import json
from datetime import datetime

# Configuration
APP_ID = 'cli_a9c9443f9278dbd6'
APP_SECRET = 'Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4'
APP_TOKEN = 'N42HbN11JaIxxgstE4gcRdl0nPf'
TABLE_ID = 'tbltqXWK6ozCXAXo'

def get_tenant_access_token():
    """Get Feishu tenant access token"""
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    data = {'app_id': APP_ID, 'app_secret': APP_SECRET}
    response = requests.post(url, json=data)
    result = response.json()
    if result.get('code') == 0:
        return result['tenant_access_token']
    else:
        raise Exception(f"获取token失败: {result}")

def list_all_records(access_token):
    """List all records"""
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
    """Update a record"""
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {'fields': fields}
    response = requests.put(url, headers=headers, json=data)
    return response.json()

def delete_record(access_token, record_id):
    """Delete a record"""
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.delete(url, headers=headers)
    return response.json()

def find_duplicates(records):
    """Find duplicate records by title"""
    title_groups = {}
    for record in records:
        title = record['fields'].get('标题', '')
        if not title:
            continue
        if title not in title_groups:
            title_groups[title] = []
        title_groups[title].append(record)

    duplicates = {title: group for title, group in title_groups.items() if len(group) > 1}
    return duplicates

def handle_duplicates_correct_logic(access_token, duplicates):
    """
    正确的处理逻辑：
    1. 保留无路径的记录（准确数据）
    2. 复制有路径记录的路径字段
    3. 删除有路径的记录
    """
    processed_count = 0

    for title, group in duplicates.items():
        print(f"\n处理重复: {title} ({len(group)}条)")

        records_with_path = [r for r in group if r['fields'].get('本地文件路径')]
        records_without_path = [r for r in group if not r['fields'].get('本地文件路径')]

        if records_with_path and records_without_path:
            # 保留无路径的记录
            keep_record = records_without_path[0]
            print(f"  保留: {keep_record['record_id']} (无路径，准确数据)")

            # 从有路径的记录中获取路径
            source_record = records_with_path[0]
            file_path = source_record['fields'].get('本地文件路径')

            if file_path:
                print(f"  复制路径: {file_path}")
                result = update_record(access_token, keep_record['record_id'], {
                    '本地文件路径': file_path
                })
                if result.get('code') == 0:
                    print(f"    ✓ 路径已复制")
                else:
                    print(f"    ✗ 复制失败: {result}")

            # 删除所有有路径的记录
            for record in records_with_path:
                print(f"  删除: {record['record_id']} (有路径，本地添加)")
                result = delete_record(access_token, record['record_id'])
                if result.get('code') == 0:
                    print(f"    ✓ 已删除")
                    processed_count += 1
                else:
                    print(f"    ✗ 删除失败: {result}")

            # 删除多余的无路径记录（保留第一条）
            for record in records_without_path[1:]:
                print(f"  删除: {record['record_id']} (多余的无路径记录)")
                result = delete_record(access_token, record['record_id'])
                if result.get('code') == 0:
                    print(f"    ✓ 已删除")
                    processed_count += 1
                else:
                    print(f"    ✗ 删除失败: {result}")

        elif records_with_path and not records_without_path:
            # 只有有路径的记录，保留第一条
            keep_record = records_with_path[0]
            print(f"  保留: {keep_record['record_id']} (第一条)")
            for record in records_with_path[1:]:
                print(f"  删除: {record['record_id']}")
                result = delete_record(access_token, record['record_id'])
                if result.get('code') == 0:
                    print(f"    ✓ 已删除")
                    processed_count += 1
                else:
                    print(f"    ✗ 删除失败: {result}")

        elif records_without_path and not records_with_path:
            # 只有无路径的记录，保留第一条
            keep_record = records_without_path[0]
            print(f"  保留: {keep_record['record_id']} (第一条)")
            for record in records_without_path[1:]:
                print(f"  删除: {record['record_id']}")
                result = delete_record(access_token, record['record_id'])
                if result.get('code') == 0:
                    print(f"    ✓ 已删除")
                    processed_count += 1
                else:
                    print(f"    ✗ 删除失败: {result}")

    return processed_count

def main():
    print("=== 正确的重复记录处理 ===\n")

    access_token = get_tenant_access_token()
    print("✓ 获取访问令牌成功\n")

    records = list_all_records(access_token)
    print(f"✓ 共 {len(records)} 条记录\n")

    duplicates = find_duplicates(records)
    print(f"✓ 发现 {len(duplicates)} 组重复记录\n")

    if not duplicates:
        print("没有重复记录")
        return

    print("重复记录详情:")
    for title, group in duplicates.items():
        print(f"\n【{title}】")
        for record in group:
            fields = record['fields']
            file_path = fields.get('本地文件路径', '无')
            views = fields.get('曝光量', '无')
            print(f"  - ID: {record['record_id']}")
            print(f"    路径: {file_path}")
            print(f"    曝光量: {views}")

    print("\n" + "="*50)
    print("开始处理...")
    print("="*50)

    processed = handle_duplicates_correct_logic(access_token, duplicates)
    print(f"\n✓ 处理完成，共处理 {processed} 条记录")

if __name__ == '__main__':
    main()
