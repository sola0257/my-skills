#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清空并重新填充飞书内容记录
"""

import requests
import json
import os
from datetime import datetime

# 飞书配置
APP_ID = "cli_a9c9443f9278dbd6"
APP_SECRET = "Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4"
APP_TOKEN = "N42HbN11JaIxxgstE4gcRdl0nPf"
TABLE_ID = "tbltqXWK6ozCXAXo"

# 已发布内容目录
PUBLISHED_DIR = "/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/订阅号"

def get_tenant_access_token():
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {"app_id": APP_ID, "app_secret": APP_SECRET}

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if result.get("code") == 0:
        return result.get("tenant_access_token")
    else:
        raise Exception(f"获取 token 失败: {result}")

def get_all_records(app_token, table_id, access_token):
    """获取表格中的所有记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {"Authorization": f"Bearer {access_token}"}

    all_records = []
    page_token = None

    while True:
        params = {"page_size": 500}
        if page_token:
            params["page_token"] = page_token

        response = requests.get(url, headers=headers, params=params)
        result = response.json()

        if result.get("code") == 0:
            items = result.get("data", {}).get("items", [])
            all_records.extend(items)

            # 检查是否还有更多数据
            page_token = result.get("data", {}).get("page_token")
            if not page_token:
                break
        else:
            print(f"❌ 获取记录失败: {result}")
            break

    return all_records

def delete_record(app_token, table_id, record_id, access_token):
    """删除单条记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.delete(url, headers=headers)
    result = response.json()

    return result.get("code") == 0

def scan_published_content(base_dir):
    """扫描已发布内容目录，提取元数据"""
    content_records = []

    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)

        if not os.path.isdir(folder_path) or folder_name.startswith('.') or folder_name == '已发布':
            continue

        try:
            date_str, title = folder_name.split('_', 1)
            publish_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print(f"⚠️  跳过无效文件夹: {folder_name}")
            continue

        push_result_file = os.path.join(folder_path, '推送结果.json')
        push_data = {}
        if os.path.exists(push_result_file):
            with open(push_result_file, 'r', encoding='utf-8') as f:
                push_data = json.load(f)

        date_timestamp = int(publish_date.timestamp() * 1000)

        record = {
            "日期": date_timestamp,
            "标题": push_data.get('title', title),
            "平台": "微信公众号-订阅号",
            "内容类型": "长文",
            "本地文件路径": folder_path,
        }

        if push_data.get('push_time'):
            try:
                push_time_str = push_data.get('push_time').split('T')[0]
                push_time = datetime.strptime(push_time_str, '%Y-%m-%d')
                record["发布时间"] = int(push_time.timestamp() * 1000)
            except:
                pass

        content_records.append(record)

    return content_records

def add_record_to_table(app_token, table_id, record_data, access_token):
    """添加记录到表格"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {"fields": record_data}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    return result.get("code") == 0

def main():
    print("=" * 60)
    print("清空并重新填充飞书内容记录")
    print("=" * 60)

    # 获取 access token
    print("\n🔑 获取访问令牌...")
    access_token = get_tenant_access_token()
    print(f"✅ 访问令牌获取成功")

    # Step 1: 获取所有现有记录
    print("\n📋 Step 1: 获取现有记录...")
    existing_records = get_all_records(APP_TOKEN, TABLE_ID, access_token)
    print(f"✅ 找到 {len(existing_records)} 条现有记录")

    # Step 2: 删除所有现有记录
    if existing_records:
        print("\n🗑️  Step 2: 删除现有记录...")
        deleted_count = 0
        for record in existing_records:
            record_id = record.get("record_id")
            if delete_record(APP_TOKEN, TABLE_ID, record_id, access_token):
                deleted_count += 1
                print(f"  ✅ 已删除记录: {record_id}")
            else:
                print(f"  ❌ 删除失败: {record_id}")
        print(f"✅ 成功删除 {deleted_count}/{len(existing_records)} 条记录")
    else:
        print("\n✅ Step 2: 表格为空，无需删除")

    # Step 3: 扫描已发布内容
    print("\n📂 Step 3: 扫描已发布内容...")
    content_records = scan_published_content(PUBLISHED_DIR)
    print(f"✅ 扫描到 {len(content_records)} 条记录")

    # Step 4: 填充数据到表格
    print("\n💾 Step 4: 填充数据到表格...")
    success_count = 0
    for record in content_records:
        if add_record_to_table(APP_TOKEN, TABLE_ID, record, access_token):
            success_count += 1
            title = record.get('标题', '')
            print(f"  ✅ {title}")
        else:
            title = record.get('标题', '')
            print(f"  ❌ {title}")

    # 总结
    print("\n" + "=" * 60)
    print(f"✅ 完成！成功填充 {success_count}/{len(content_records)} 条记录")
    print("=" * 60)

if __name__ == "__main__":
    main()
