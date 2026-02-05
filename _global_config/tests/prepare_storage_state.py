#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将保存的 cookies 转换为 Playwright storage state 格式
"""

import json
import os

COOKIES_FILE = '/Users/dj/Desktop/小静的skills/_global_config/wechat_cookies.json'
STORAGE_STATE_FILE = '/Users/dj/Desktop/小静的skills/_global_config/wechat_storage_state.json'

def convert_cookies_to_storage_state():
    """将 cookies 转换为 Playwright storage state 格式"""

    if not os.path.exists(COOKIES_FILE):
        print(f"❌ Cookies 文件不存在: {COOKIES_FILE}")
        return False

    # 读取 cookies
    with open(COOKIES_FILE, 'r') as f:
        cookies = json.load(f)

    # 转换为 storage state 格式
    storage_state = {
        "cookies": cookies,
        "origins": []
    }

    # 保存
    with open(STORAGE_STATE_FILE, 'w') as f:
        json.dump(storage_state, f, indent=2)

    print(f"✅ Storage state 已保存: {STORAGE_STATE_FILE}")
    return True

if __name__ == "__main__":
    convert_cookies_to_storage_state()
