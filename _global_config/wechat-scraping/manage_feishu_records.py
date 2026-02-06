#!/usr/bin/env python3
"""
Feishu Records Management Script
Handles duplicate detection, deletion, and record updates
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Any

# Configuration
APP_ID = 'cli_a9c9443f9278dbd6'
APP_SECRET = 'Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4'
APP_TOKEN = 'N42HbN11JaIxxgstE4gcRdl0nPf'
TABLE_ID = 'tbltqXWK6ozCXAXo'  # 内容记录表

def get_tenant_access_token():
    """Get Feishu tenant access token"""
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    data = {
        'app_id': APP_ID,
        'app_secret': APP_SECRET
    }
    response = requests.post(url, json=data)
    result = response.json()

    if result.get('code') == 0:
        return result['tenant_access_token']
    else:
        raise Exception(f"获取token失败: {result}")

def list_all_records(access_token):
    """List all records from the table (handles pagination)"""
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

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

def delete_record(access_token, record_id):
    """Delete a record"""
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.delete(url, headers=headers)
    return response.json()

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

    # Filter to only duplicates
    duplicates = {title: group for title, group in title_groups.items() if len(group) > 1}

    return duplicates

def handle_duplicates(access_token, duplicates, dry_run=True):
    """
    Handle duplicate records
    Strategy: Keep records with local file path, delete others
    If none have file path, keep the first one
    """
    deleted_count = 0
    updated_count = 0

    for title, group in duplicates.items():
        print(f"\n处理重复记录: {title} ({len(group)}条)")

        # Separate records with and without file paths
        records_with_path = [r for r in group if r['fields'].get('本地文件路径')]
        records_without_path = [r for r in group if not r['fields'].get('本地文件路径')]

        if records_with_path:
            # Keep records with file path, delete others
            keep_record = records_with_path[0]
            delete_records = records_with_path[1:] + records_without_path

            print(f"  保留: {keep_record['record_id']} (有本地路径)")

            for record in delete_records:
                print(f"  删除: {record['record_id']}")
                if not dry_run:
                    result = delete_record(access_token, record['record_id'])
                    if result.get('code') == 0:
                        deleted_count += 1
                    else:
                        print(f"    删除失败: {result}")
        else:
            # No records have file path, keep the first one
            keep_record = group[0]
            delete_records = group[1:]

            print(f"  保留: {keep_record['record_id']} (第一条)")

            for record in delete_records:
                print(f"  删除: {record['record_id']}")
                if not dry_run:
                    result = delete_record(access_token, record['record_id'])
                    if result.get('code') == 0:
                        deleted_count += 1
                    else:
                        print(f"    删除失败: {result}")

    return deleted_count, updated_count

def merge_duplicate_info(access_token, duplicates, dry_run=True):
    """
    Merge information from duplicate records
    Keep the record with file path, but merge other fields from duplicates
    """
    merged_count = 0

    for title, group in duplicates.items():
        records_with_path = [r for r in group if r['fields'].get('本地文件路径')]
        records_without_path = [r for r in group if not r['fields'].get('本地文件路径')]

        if records_with_path and records_without_path:
            # Merge info from records without path into the one with path
            keep_record = records_with_path[0]
            merge_from = records_without_path[0]  # Take the first one

            # Fields to potentially merge
            merge_fields = {}

            # If keep_record is missing publish_status, get it from merge_from
            if not keep_record['fields'].get('发布状态') and merge_from['fields'].get('发布状态'):
                merge_fields['发布状态'] = merge_from['fields']['发布状态']

            # If keep_record is missing metrics, get them from merge_from
            if not keep_record['fields'].get('曝光量') and merge_from['fields'].get('曝光量'):
                merge_fields['曝光量'] = merge_from['fields']['曝光量']

            if not keep_record['fields'].get('点击量') and merge_from['fields'].get('点击量'):
                merge_fields['点击量'] = merge_from['fields']['点击量']

            if not keep_record['fields'].get('互动量') and merge_from['fields'].get('互动量'):
                merge_fields['互动量'] = merge_from['fields']['互动量']

            if merge_fields:
                print(f"\n合并信息到: {title}")
                print(f"  更新字段: {list(merge_fields.keys())}")

                if not dry_run:
                    result = update_record(access_token, keep_record['record_id'], merge_fields)
                    if result.get('code') == 0:
                        merged_count += 1
                    else:
                        print(f"    更新失败: {result}")

    return merged_count

def main():
    """Main function"""
    print("=== Feishu 记录管理工具 ===\n")

    # Get access token
    print("获取访问令牌...")
    access_token = get_tenant_access_token()
    print("✓ 成功\n")

    # List all records
    print("获取所有记录...")
    records = list_all_records(access_token)
    print(f"✓ 共 {len(records)} 条记录\n")

    # Find duplicates
    print("查找重复记录...")
    duplicates = find_duplicates(records)
    print(f"✓ 发现 {len(duplicates)} 组重复记录\n")

    if not duplicates:
        print("没有重复记录，无需处理")
        return

    # Display duplicates
    print("重复记录详情:")
    for title, group in duplicates.items():
        print(f"\n标题: {title}")
        for record in group:
            fields = record['fields']
            file_path = fields.get('本地文件路径', '无')
            publish_status = fields.get('发布状态', '无')
            print(f"  - ID: {record['record_id']}")
            print(f"    本地路径: {file_path}")
            print(f"    发布状态: {publish_status}")

    # Ask for confirmation
    print("\n" + "="*50)
    print("处理策略:")
    print("1. 先合并信息（将无路径记录的字段合并到有路径的记录）")
    print("2. 再删除重复（保留有本地路径的记录，删除其他）")
    print("="*50)

    response = input("\n是否执行？(yes/no): ")

    if response.lower() == 'yes':
        # Step 1: Merge information
        print("\n步骤1: 合并信息...")
        merged_count = merge_duplicate_info(access_token, duplicates, dry_run=False)
        print(f"✓ 合并了 {merged_count} 条记录的信息\n")

        # Step 2: Delete duplicates
        print("步骤2: 删除重复...")
        deleted_count, _ = handle_duplicates(access_token, duplicates, dry_run=False)
        print(f"\n✓ 删除了 {deleted_count} 条重复记录")
    else:
        print("\n已取消操作")

if __name__ == '__main__':
    main()
