#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信API测试脚本
用于测试API连接和端点
"""

import requests
import json

# API配置
API_BASE = "https://wx.limyai.com/api/openapi"
SUBSCRIPTION_API_KEY = "xhs_1beb09d01e1f7600af37b438a845a07c"

# 测试不同的端点
endpoints = [
    "/draft/add",
    "/material/add_draft",
    "/draft",
    "/api/draft/add",
    "/wechat/draft/add"
]

print("🔍 测试微信API端点...\n")

for endpoint in endpoints:
    url = f"{API_BASE}{endpoint}"
    print(f"📡 测试: {url}")

    try:
        # 尝试GET请求
        response = requests.get(
            url,
            headers={
                'Authorization': f'Bearer {SUBSCRIPTION_API_KEY}'
            },
            timeout=10
        )
        print(f"   GET Status: {response.status_code}")
        if response.status_code != 404:
            print(f"   Response: {response.text[:200]}")

        # 尝试POST请求
        response = requests.post(
            url,
            headers={
                'Authorization': f'Bearer {SUBSCRIPTION_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'articles': [{
                    'title': '测试标题',
                    'content': '<p>测试内容</p>'
                }]
            },
            timeout=10
        )
        print(f"   POST Status: {response.status_code}")
        if response.status_code != 404:
            print(f"   Response: {response.text[:200]}")

    except Exception as e:
        print(f"   Error: {e}")

    print()

print("\n💡 提示：请查看微绿流量宝的API文档，确认正确的端点路径")
