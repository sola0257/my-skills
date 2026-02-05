#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试添加记录到飞书表格
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

def add_simple_record(app_token, table_id, access_token):
    """添加一条简单记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 只填充最基本的字段
    data = {
        "fields": {
            "标题": "测试标题"
        }
    }

    print(f"发送数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")

    return result.get("code") == 0

def main():
    print("测试添加记录到飞书表格")
    print("=" * 60)

    # 获取 access token
    print("\n🔑 获取访问令牌...")
    access_token = get_tenant_access_token()
    print(f"✅ 访问令牌获取成功")

    # 获取字段列表
    print("\n📋 获取表格字段...")
    fields = get_table_fields(APP_TOKEN, TABLE_ID, access_token)
    print(f"✅ 获取到 {len(fields)} 个字段")
    print("\n字段列表:")
    for field in fields:
        print(f"  {field['field_name']} (ID: {field['field_id']}, Type: {field['type']})")

    # 尝试添加记录
    print("\n💾 尝试添加记录...")
    success = add_simple_record(APP_TOKEN, TABLE_ID, access_token)

    if success:
        print("\n✅ 成功添加记录！")
    else:
        print("\n❌ 添加记录失败")

if __name__ == "__main__":
    main()
