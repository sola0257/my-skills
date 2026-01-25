#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取微信公众号列表
"""

import requests
import json

# API配置
API_BASE = "https://wx.limyai.com/api/openapi"
SUBSCRIPTION_API_KEY = "xhs_1beb09d01e1f7600af37b438a845a07c"
SERVICE_API_KEY = "xhs_1a04cc8001bc87b37cc032bdde2517b0"

def get_wechat_accounts(api_key):
    """获取公众号列表"""
    try:
        response = requests.get(
            f"{API_BASE}/wechat-accounts",
            headers={
                'X-API-Key': api_key
            },
            timeout=30
        )

        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            return response.json()
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

print("📋 获取订阅号列表...")
print("="*50)
result = get_wechat_accounts(SUBSCRIPTION_API_KEY)
if result:
    print(json.dumps(result, indent=2, ensure_ascii=False))

print("\n📋 获取服务号列表...")
print("="*50)
result = get_wechat_accounts(SERVICE_API_KEY)
if result:
    print(json.dumps(result, indent=2, ensure_ascii=False))
