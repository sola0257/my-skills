#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书内容记录填充脚本
功能：
1. 重命名多维表格应用
2. 重命名子表
3. 扫描已发布内容并填充到内容记录表
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

# 飞书配置
APP_ID = "cli_a9c9443f9278dbd6"
APP_SECRET = "Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4"
APP_TOKEN = "N42HbN11JaIxxgstE4gcRdl0nPf"
TABLE_ID = "tbltqXWK6ozCXAXo"  # 全部内容表单

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

def rename_app(app_token, new_name, access_token):
    """重命名多维表格应用"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {"name": new_name}

    response = requests.put(url, headers=headers, json=data)
    result = response.json()

    if result.get("code") == 0:
        print(f"✅ 应用重命名成功: {new_name}")
        return True
    else:
        print(f"❌ 应用重命名失败: {result}")
        return False

def rename_table(app_token, table_id, new_name, access_token):
    """重命名子表"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {"name": new_name}

    response = requests.patch(url, headers=headers, json=data)
    result = response.json()

    if result.get("code") == 0:
        print(f"✅ 子表重命名成功: {new_name}")
        return True
    else:
        print(f"❌ 子表重命名失败: {result}")
        return False

def scan_published_content(base_dir):
    """扫描已发布内容目录，提取元数据"""
    content_records = []

    # 遍历目录
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)

        # 跳过非目录和特殊文件夹
        if not os.path.isdir(folder_path) or folder_name.startswith('.') or folder_name == '已发布':
            continue

        # 解析文件夹名称: YYYY-MM-DD_标题
        try:
            date_str, title = folder_name.split('_', 1)
            publish_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print(f"⚠️  跳过无效文件夹: {folder_name}")
            continue

        # 查找推送结果文件
        push_result_file = os.path.join(folder_path, '推送结果.json')
        markdown_file = None

        # 查找 markdown 文件
        for file in os.listdir(folder_path):
            if file.endswith('.md'):
                markdown_file = os.path.join(folder_path, file)
                break

        # 读取推送结果
        push_data = {}
        if os.path.exists(push_result_file):
            with open(push_result_file, 'r', encoding='utf-8') as f:
                push_data = json.load(f)

        # 读取 markdown 文件获取摘要
        summary = ""
        if markdown_file and os.path.exists(markdown_file):
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取摘要（第一个 > 引用块）
                for line in content.split('\n'):
                    if line.startswith('> '):
                        summary = line[2:].strip()
                        break

        # 构建记录（匹配实际字段名）
        # 日期字段需要转换为Unix时间戳（毫秒）
        date_timestamp = int(publish_date.timestamp() * 1000)

        record = {
            "日期": date_timestamp,  # Unix时间戳（毫秒）
            "标题": push_data.get('title', title),
            "平台": "微信公众号-订阅号",
            "内容类型": "长文",
            "本地文件路径": folder_path,
        }

        # 如果有发布时间，也转换为时间戳
        if push_data.get('push_time'):
            try:
                push_time_str = push_data.get('push_time').split('T')[0]  # 只取日期部分
                push_time = datetime.strptime(push_time_str, '%Y-%m-%d')
                record["发布时间"] = int(push_time.timestamp() * 1000)
            except:
                pass  # 如果转换失败，跳过这个字段

        content_records.append(record)
        print(f"📄 提取记录: {record['日期']} - {record['标题']}")

    return content_records

def get_table_fields(app_token, table_id, access_token):
    """获取表格字段信息"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    result = response.json()

    if result.get("code") == 0:
        return result.get("data", {}).get("items", [])
    else:
        print(f"❌ 获取字段失败: {result}")
        return []

def add_record_to_table(app_token, table_id, record_data, field_mapping, access_token):
    """添加记录到表格"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 直接使用字段名，不需要映射到字段ID
    data = {"fields": record_data}

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if result.get("code") == 0:
        return True
    else:
        print(f"❌ 添加记录失败: {result}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("飞书内容记录填充脚本")
    print("=" * 60)

    # 获取 access token
    print("\n🔑 获取访问令牌...")
    access_token = get_tenant_access_token()
    print(f"✅ 访问令牌获取成功")

    # Step 1: 重命名应用
    print("\n📝 Step 1: 重命名多维表格应用...")
    rename_app(APP_TOKEN, "慢养四季运营数据库", access_token)

    # Step 2: 重命名子表
    print("\n📝 Step 2: 重命名子表...")
    rename_table(APP_TOKEN, TABLE_ID, "内容记录", access_token)

    # Step 3: 获取表格字段
    print("\n📋 Step 3: 获取表格字段...")
    fields = get_table_fields(APP_TOKEN, TABLE_ID, access_token)
    field_mapping = {}
    for field in fields:
        field_mapping[field['field_name']] = field['field_id']
    print(f"✅ 获取到 {len(fields)} 个字段")
    print("\n字段映射:")
    for name, fid in field_mapping.items():
        print(f"  {name} → {fid}")

    # Step 4: 扫描已发布内容
    print("\n📂 Step 4: 扫描已发布内容...")
    content_records = scan_published_content(PUBLISHED_DIR)
    print(f"✅ 扫描到 {len(content_records)} 条记录")

    # Step 5: 填充数据到表格
    print("\n💾 Step 5: 填充数据到表格...")
    success_count = 0
    for record in content_records:
        if add_record_to_table(APP_TOKEN, TABLE_ID, record, field_mapping, access_token):
            success_count += 1
            print(f"  ✅ {record['日期']} - {record['标题']}")
        else:
            print(f"  ❌ {record['日期']} - {record['标题']}")

    # 总结
    print("\n" + "=" * 60)
    print(f"✅ 完成！成功填充 {success_count}/{len(content_records)} 条记录")
    print("=" * 60)

if __name__ == "__main__":
    main()
