#!/usr/bin/env python3
"""
智能重复检测：使用相似度匹配
"""

import requests
from difflib import SequenceMatcher

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

def normalize_title(title):
    """标准化标题：去除表情符号、标点符号差异"""
    import re
    # 去除表情符号
    title = re.sub(r'[^\w\s\u4e00-\u9fff]', '', title)
    # 去除多余空格
    title = ' '.join(title.split())
    return title.strip()

def similarity(a, b):
    """计算两个字符串的相似度"""
    return SequenceMatcher(None, a, b).ratio()

def find_similar_duplicates(records, threshold=0.85):
    """查找相似的重复记录"""
    duplicates = []
    processed = set()

    for i, record1 in enumerate(records):
        if i in processed:
            continue

        title1 = record1['fields'].get('标题', '')
        if not title1:
            continue

        norm_title1 = normalize_title(title1)
        similar_group = [record1]

        for j, record2 in enumerate(records[i+1:], i+1):
            if j in processed:
                continue

            title2 = record2['fields'].get('标题', '')
            if not title2:
                continue

            norm_title2 = normalize_title(title2)

            # 计算相似度
            sim = similarity(norm_title1, norm_title2)

            if sim >= threshold:
                similar_group.append(record2)
                processed.add(j)

        if len(similar_group) > 1:
            duplicates.append(similar_group)
            processed.add(i)

    return duplicates

def update_record(access_token, record_id, fields):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {'fields': fields}
    response = requests.put(url, headers=headers, json=data)
    return response.json()

def delete_record(access_token, record_id):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.delete(url, headers=headers)
    return response.json()

def handle_similar_duplicates(access_token, duplicates):
    """
    处理相似重复：
    1. 保留无路径的记录（准确数据）
    2. 复制有路径记录的路径
    3. 删除有路径的记录
    """
    processed_count = 0

    for group in duplicates:
        print(f"\n发现相似重复组 ({len(group)}条):")

        for record in group:
            title = record['fields'].get('标题', '')
            file_path = record['fields'].get('本地文件路径', '无')
            views = record['fields'].get('曝光量', '无')
            print(f"  - {title}")
            print(f"    ID: {record['record_id']}")
            print(f"    路径: {file_path}")
            print(f"    曝光量: {views}")

        records_with_path = [r for r in group if r['fields'].get('本地文件路径')]
        records_without_path = [r for r in group if not r['fields'].get('本地文件路径')]

        if records_with_path and records_without_path:
            # 保留无路径的记录
            keep_record = records_without_path[0]
            print(f"\n  保留: {keep_record['record_id']} (无路径，准确数据)")

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
                print(f"  删除: {record['record_id']} (有路径)")
                result = delete_record(access_token, record['record_id'])
                if result.get('code') == 0:
                    print(f"    ✓ 已删除")
                    processed_count += 1
                else:
                    print(f"    ✗ 删除失败: {result}")

            # 删除多余的无路径记录
            for record in records_without_path[1:]:
                print(f"  删除: {record['record_id']} (多余)")
                result = delete_record(access_token, record['record_id'])
                if result.get('code') == 0:
                    print(f"    ✓ 已删除")
                    processed_count += 1
                else:
                    print(f"    ✗ 删除失败: {result}")

        elif records_with_path and not records_without_path:
            # 只有有路径的记录，保留第一条
            keep_record = records_with_path[0]
            print(f"\n  保留: {keep_record['record_id']} (第一条)")
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
            print(f"\n  保留: {keep_record['record_id']} (第一条)")
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
    print("=== 智能重复检测（相似度匹配）===\n")

    access_token = get_tenant_access_token()
    print("✓ 获取访问令牌成功\n")

    records = list_all_records(access_token)
    print(f"✓ 共 {len(records)} 条记录\n")

    duplicates = find_similar_duplicates(records, threshold=0.85)
    print(f"✓ 发现 {len(duplicates)} 组相似重复\n")

    if not duplicates:
        print("没有相似重复记录")
        return

    print("="*50)
    print("开始处理...")
    print("="*50)

    processed = handle_similar_duplicates(access_token, duplicates)
    print(f"\n✓ 处理完成，共处理 {processed} 条记录")

if __name__ == '__main__':
    main()
