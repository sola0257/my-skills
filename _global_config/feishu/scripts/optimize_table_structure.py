#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化飞书表格结构
1. 删除"轨道"字段
2. 添加"合集"字段
3. 添加"发布状态"字段
"""

import requests
import json

# 飞书配置
APP_ID = "cli_a9c9443f9278dbd6"
APP_SECRET = "Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4"
APP_TOKEN = "N42HbN11JaIxxgstE4gcRdl0nPf"
TABLE_ID = "tbltqXWK6ozCXAXo"

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

def delete_field(app_token, table_id, field_id, access_token):
    """删除字段"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields/{field_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.delete(url, headers=headers)
    result = response.json()

    return result.get("code") == 0

def add_field(app_token, table_id, field_name, field_type, access_token, options=None):
    """添加字段"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "field_name": field_name,
        "type": field_type
    }

    if options and field_type in [3, 4]:  # 单选或多选
        data["property"] = {"options": options}

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if result.get("code") == 0:
        return result.get("data", {}).get("field", {}).get("field_id")
    else:
        print(f"❌ 添加字段失败: {result}")
        return None

def main():
    print("=" * 60)
    print("优化飞书表格结构")
    print("=" * 60)

    # 获取 access token
    print("\n🔑 获取访问令牌...")
    access_token = get_tenant_access_token()
    print(f"✅ 访问令牌获取成功")

    # Step 1: 获取所有字段
    print("\n📋 Step 1: 获取现有字段...")
    fields = get_table_fields(APP_TOKEN, TABLE_ID, access_token)
    print(f"✅ 获取到 {len(fields)} 个字段")

    # 找到"轨道"字段
    guidao_field_id = None
    for field in fields:
        if field['field_name'] == '轨道':
            guidao_field_id = field['field_id']
            print(f"  找到'轨道'字段: {guidao_field_id}")
            break

    # Step 2: 删除"轨道"字段
    if guidao_field_id:
        print("\n🗑️  Step 2: 删除'轨道'字段...")
        if delete_field(APP_TOKEN, TABLE_ID, guidao_field_id, access_token):
            print("✅ '轨道'字段已删除")
        else:
            print("❌ '轨道'字段删除失败")
    else:
        print("\n⚠️  Step 2: 未找到'轨道'字段，跳过删除")

    # Step 3: 添加"合集"字段（文本类型）
    print("\n➕ Step 3: 添加'合集'字段...")
    heji_field_id = add_field(APP_TOKEN, TABLE_ID, "合集", 1, access_token)
    if heji_field_id:
        print(f"✅ '合集'字段已添加 (ID: {heji_field_id})")
    else:
        print("❌ '合集'字段添加失败")

    # Step 4: 添加"发布状态"字段（单选类型）
    print("\n➕ Step 4: 添加'发布状态'字段...")
    status_options = [
        {"name": "草稿"},
        {"name": "已发布"},
        {"name": "已删除"}
    ]
    status_field_id = add_field(APP_TOKEN, TABLE_ID, "发布状态", 3, access_token, status_options)
    if status_field_id:
        print(f"✅ '发布状态'字段已添加 (ID: {status_field_id})")
    else:
        print("❌ '发布状态'字段添加失败")

    # 总结
    print("\n" + "=" * 60)
    print("✅ 表格结构优化完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
