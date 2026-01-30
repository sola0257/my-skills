#!/usr/bin/env python3
"""
DeepRouter Midjourney API 测试 - 使用正确端点
"""
import requests
import json
import time

# DeepRouter API 配置
API_KEY = "sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I"
BASE_URL = "https://deeprouter.top"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("🎨 测试 DeepRouter Midjourney API...")
print("=" * 60)

# 测试提交 Imagine 任务
imagine_url = f"{BASE_URL}/mj/submit/imagine"
test_prompt = "A beautiful plant in a living room, natural light --ar 3:4"

payload = {
    "prompt": test_prompt
}

try:
    print(f"\n📤 提交 Imagine 任务...")
    print(f"📊 Prompt: {test_prompt}")

    response = requests.post(imagine_url, headers=headers, json=payload, timeout=30)
    print(f"📊 响应状态码: {response.status_code}")
    print(f"📊 响应内容: {response.text}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ 任务提交成功！")
        print(f"📊 完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")

        # 如果返回了任务 ID，可以查询状态
        if "result" in result:
            task_id = result["result"]
            print(f"\n📋 任务 ID: {task_id}")
    else:
        print(f"\n❌ 任务提交失败")

except Exception as e:
    print(f"\n❌ 请求异常: {e}")
