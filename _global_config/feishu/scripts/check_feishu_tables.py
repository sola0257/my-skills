#!/usr/bin/env python3
"""
飞书多维表格结构检查脚本
检查现有表格的字段结构，评估是否需要优化
"""

import requests
import json
import time

# 飞书配置
APP_ID = "cli_a9c9443f9278dbd6"
APP_SECRET = "Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4"

# 表格配置
TABLES = [
    {
        "name": "Content log—慢养四季内容记录",
        "app_token": "N42HbN11JaIxxgstE4gcRdl0nPf",
        "table_id": "tbltqXWK6ozCXAXo",
        "purpose": "记录已发布内容"
    },
    {
        "name": "content production_sheet--内容素材清单",
        "app_token": "KONxbVeHIaAGMXsuow0cnPJqnCf",
        "table_id": "tbl1O5MsUyH2a6k9",
        "purpose": "管理内容素材"
    },
    {
        "name": "选题清单—慢养四季选题库",
        "app_token": "Cip1boCZYazTtxstP2Fc8zrYnSb",
        "table_id": "tblKTtvpilldLuhG",
        "purpose": "管理选题"
    }
]

def get_tenant_access_token():
    """获取tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            return result.get("tenant_access_token")
    return None

def get_table_fields(app_token, table_id, access_token):
    """获取表格字段信息"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            return result.get("data", {}).get("items", [])
    return None

def analyze_table_structure():
    """分析表格结构"""
    print("=" * 80)
    print("飞书多维表格结构分析")
    print("=" * 80)
    print()

    # 获取access token
    print("正在获取访问令牌...")
    access_token = get_tenant_access_token()
    if not access_token:
        print("❌ 获取访问令牌失败")
        return
    print("✅ 访问令牌获取成功")
    print()

    # 分析每个表格
    for table in TABLES:
        print(f"📊 表格：{table['name']}")
        print(f"   用途：{table['purpose']}")
        print(f"   App Token：{table['app_token']}")
        print(f"   Table ID：{table['table_id']}")
        print()

        # 获取字段信息
        fields = get_table_fields(table['app_token'], table['table_id'], access_token)
        if fields:
            print(f"   字段列表（共{len(fields)}个字段）：")
            for i, field in enumerate(fields, 1):
                field_name = field.get("field_name", "未知")
                field_type = field.get("type", "未知")
                print(f"   {i}. {field_name} ({field_type})")
            print()
        else:
            print("   ❌ 无法获取字段信息")
            print()

        time.sleep(0.5)  # 避免请求过快

    print("=" * 80)
    print("分析完成")
    print("=" * 80)

if __name__ == "__main__":
    analyze_table_structure()
