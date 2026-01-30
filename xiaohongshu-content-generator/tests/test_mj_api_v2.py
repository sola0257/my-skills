#!/usr/bin/env python3
"""
Midjourney API 集成脚本 v2
基于云雾平台的实际 API 结构
"""
import requests
import base64
import time
import json
from pathlib import Path

class MidjourneyAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://yunwu.ai/v1"  # 使用 v1 端点
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def generate_with_prompt(self, prompt: str, output_path: str):
        """
        直接使用 prompt 生成图片（不上传参考图）
        测试 API 是否可用
        """
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": "mj_imagine",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            print(f"📤 发送请求到: {url}")
            print(f"📊 Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

            response = requests.post(url, headers=self.headers, json=payload, timeout=120)
            print(f"📊 响应状态码: {response.status_code}")
            print(f"📊 响应内容: {response.text[:1000]}")

            response.raise_for_status()
            result = response.json()

            print(f"✅ API 调用成功")
            print(f"📊 完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")

            return result

        except Exception as e:
            print(f"❌ 请求失败: {e}")
            if 'response' in locals():
                print(f"📊 响应文本: {response.text}")
            return None


# 测试
if __name__ == "__main__":
    api = MidjourneyAPI("sk-92m3Pkv3lmHSHrtg3NFHalSOTJr4wUSeeqIfPLft959Fu3AS")

    # 简单测试 prompt
    test_prompt = "A beautiful plant in a living room, natural light, 3:4 aspect ratio --ar 3:4"

    print("🎨 测试 Midjourney API 连接...")
    print("=" * 60)

    result = api.generate_with_prompt(test_prompt, "/tmp/test.png")
