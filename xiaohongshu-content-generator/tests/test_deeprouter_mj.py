#!/usr/bin/env python3
"""
DeepRouter Midjourney API 测试
"""
import requests
import json

# DeepRouter API 配置
API_KEY = "sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I"
BASE_URL = "https://api.deeprouter.io/v1"  # 根据文档推测

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 测试简单的 imagine 任务
test_prompt = "A beautiful plant in a living room, natural light --ar 3:4"

print("🎨 测试 DeepRouter Midjourney API...")
print(f"📊 API Key: {API_KEY[:20]}...")
print(f"📊 Base URL: {BASE_URL}")
print("=" * 60)

# 尝试使用 chat completions 格式（类似 OpenAI）
url = f"{BASE_URL}/chat/completions"
payload = {
    "model": "mj_imagine",
    "messages": [
        {"role": "user", "content": test_prompt}
    ]
}

try:
    print(f"\n📤 发送请求...")
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    print(f"📊 响应状态码: {response.status_code}")
    print(f"📊 响应内容: {response.text[:1000]}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ API 调用成功！")
        print(f"📊 完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    else:
        print(f"\n❌ API 调用失败")
        print(f"错误信息: {response.text}")

except Exception as e:
    print(f"\n❌ 请求异常: {e}")
