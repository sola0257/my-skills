#!/usr/bin/env python3
"""
飞书多维表格自动优化脚本
自动完成表格优化：增加字段、新建表格
"""

import requests
import json
import time

# 飞书配置
APP_ID = "cli_a9c9443f9278dbd6"
APP_SECRET = "Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4"

# 现有表格
CONTENT_LOG_APP_TOKEN = "N42HbN11JaIxxgstE4gcRdl0nPf"
CONTENT_LOG_TABLE_ID = "tbltqXWK6ozCXAXo"

TOPIC_APP_TOKEN = "Cip1boCZYazTtxstP2Fc8zrYnSb"
TOPIC_TABLE_ID = "tblKTtvpilldLuhG"

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

def add_field_to_table(app_token, table_id, field_name, field_type, access_token, options=None):
    """向表格添加字段"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "field_name": field_name,
        "type": field_type
    }

    # 如果是单选或多选，需要添加选项
    if options and field_type in [3, 4]:  # 3=单选, 4=多选
        data["property"] = {"options": options}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            return True, f"✅ 成功添加字段：{field_name}"
        else:
            return False, f"❌ 添加字段失败：{result.get('msg')}"
    return False, f"❌ 请求失败：{response.status_code}"

def create_new_table(app_token, table_name, fields, access_token):
    """创建新表格"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "table": {
            "name": table_name,
            "fields": fields
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            table_id = result.get("data", {}).get("table_id")
            return True, f"✅ 成功创建表格：{table_name} (ID: {table_id})"
        else:
            return False, f"❌ 创建表格失败：{result.get('msg')}"
    return False, f"❌ 请求失败：{response.status_code}"

def optimize_tables():
    """优化表格"""
    print("=" * 80)
    print("飞书多维表格自动优化")
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

    # ========== 任务1：优化Content log表格 ==========
    print("📋 任务1：优化 Content log 表格")
    print("-" * 80)

    # 添加"是否爆文"字段（复选框）
    success, msg = add_field_to_table(
        CONTENT_LOG_APP_TOKEN,
        CONTENT_LOG_TABLE_ID,
        "是否爆文",
        7,  # 7 = 复选框
        access_token
    )
    print(f"   {msg}")
    time.sleep(0.5)

    # 添加"本地文件路径"字段（文本）
    success, msg = add_field_to_table(
        CONTENT_LOG_APP_TOKEN,
        CONTENT_LOG_TABLE_ID,
        "本地文件路径",
        1,  # 1 = 文本
        access_token
    )
    print(f"   {msg}")
    time.sleep(0.5)

    # 添加"主题分类"字段（单选）
    success, msg = add_field_to_table(
        CONTENT_LOG_APP_TOKEN,
        CONTENT_LOG_TABLE_ID,
        "主题分类",
        3,  # 3 = 单选
        access_token,
        options=[
            {"name": "养护"},
            {"name": "选购"},
            {"name": "搭配"},
            {"name": "知识"}
        ]
    )
    print(f"   {msg}")
    print()

    # ========== 任务2：优化选题清单表格 ==========
    print("📋 任务2：优化 选题清单 表格")
    print("-" * 80)

    # 添加"商品关联"字段（文本，后续可以改为关联字段）
    success, msg = add_field_to_table(
        TOPIC_APP_TOKEN,
        TOPIC_TABLE_ID,
        "商品关联",
        1,  # 1 = 文本
        access_token
    )
    print(f"   {msg}")
    print()

    # ========== 任务3：创建商品库表格 ==========
    print("📋 任务3：创建 商品库 表格")
    print("-" * 80)

    product_fields = [
        {"field_name": "商品名称", "type": 1},  # 文本
        {"field_name": "商品分类", "type": 3, "property": {"options": [
            {"name": "多肉"},
            {"name": "观叶"},
            {"name": "开花"}
        ]}},  # 单选
        {"field_name": "价格", "type": 2},  # 数字
        {"field_name": "库存", "type": 2},  # 数字
        {"field_name": "商品链接", "type": 15},  # URL
        {"field_name": "爆款潜力", "type": 13, "property": {"min": 1, "max": 5}},  # 评分
        {"field_name": "适用平台", "type": 4, "property": {"options": [
            {"name": "小红书"},
            {"name": "公众号"},
            {"name": "视频号"},
            {"name": "快手"},
            {"name": "抖音"}
        ]}},  # 多选
        {"field_name": "创建时间", "type": 5},  # 日期
        {"field_name": "备注", "type": 1}  # 文本
    ]

    success, msg = create_new_table(
        CONTENT_LOG_APP_TOKEN,  # 使用Content log的app token
        "商品库",
        product_fields,
        access_token
    )
    print(f"   {msg}")
    print()

    # ========== 任务4：创建粉丝数记录表格 ==========
    print("📋 任务4：创建 粉丝数记录 表格")
    print("-" * 80)

    follower_fields = [
        {"field_name": "日期", "type": 5},  # 日期
        {"field_name": "平台", "type": 3, "property": {"options": [
            {"name": "小红书"},
            {"name": "公众号"},
            {"name": "视频号"},
            {"name": "快手"},
            {"name": "抖音"}
        ]}},  # 单选
        {"field_name": "粉丝数", "type": 2},  # 数字
        {"field_name": "涨粉数", "type": 2},  # 数字
        {"field_name": "账号阶段", "type": 3, "property": {"options": [
            {"name": "起号期"},
            {"name": "成长期"},
            {"name": "成熟期"}
        ]}},  # 单选
        {"field_name": "备注", "type": 1}  # 文本
    ]

    success, msg = create_new_table(
        CONTENT_LOG_APP_TOKEN,  # 使用Content log的app token
        "粉丝数记录",
        follower_fields,
        access_token
    )
    print(f"   {msg}")
    print()

    print("=" * 80)
    print("✅ 所有任务完成！")
    print("=" * 80)
    print()
    print("📝 后续步骤：")
    print("1. 打开飞书，查看优化后的表格")
    print("2. 检查新增的字段是否正确")
    print("3. 开始使用新的表格结构")
    print()

if __name__ == "__main__":
    optimize_tables()
