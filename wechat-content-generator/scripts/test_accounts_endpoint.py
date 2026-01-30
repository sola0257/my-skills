#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试获取公众号列表的不同端点
"""

import requests

API_BASE = "https://wx.limyai.com/api/openapi"
API_KEY = "xhs_1beb09d01e1f7600af37b438a845a07c"

endpoints = [
    ("GET", "/wechat-accounts"),
    ("POST", "/wechat-accounts"),
    ("GET", "/accounts"),
    ("POST", "/accounts"),
    ("GET", "/wechat/accounts"),
    ("GET", "/account/list"),
    ("GET", "/wechat-account/list"),
]

print("🔍 测试获取公众号列表端点...\n")

for method, endpoint in endpoints:
    url = f"{API_BASE}{endpoint}"
    print(f"📡 {method} {url}")

    try:
        if method == "GET":
            response = requests.get(
                url,
                headers={'X-API-Key': API_KEY},
                timeout=10
            )
        else:
            response = requests.post(
                url,
                headers={'X-API-Key': API_KEY, 'Content-Type': 'application/json'},
                json={},
                timeout=10
            )

        print(f"   Status: {response.status_code}")
        if response.status_code not in [404, 405]:
            print(f"   Response: {response.text[:300]}")

    except Exception as e:
        print(f"   Error: {e}")

    print()
