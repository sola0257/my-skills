#!/usr/bin/env python3
"""
简化 prompt 测试人物一致性
"""
import sys
sys.path.append('/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书')

from deeprouter_mj_api import DeepRouterMJ

api = DeepRouterMJ("sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I")

# 简化的 prompt
prompt = "woman in cream dress with plants in living room, natural light, lifestyle photography"

# ImgBB URL
character_url = "https://i.ibb.co/WNTZrtcQ/primary-ref.jpg"

print("🎨 测试简化 prompt + 人物参考")
print("=" * 60)

task_id = api.submit_imagine(prompt, character_url)
if not task_id:
    sys.exit(1)

image_url = api.wait_for_result(task_id, max_wait=300)
if not image_url:
    sys.exit(1)

output_path = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/test_simple_prompt.png"
api.download_image(image_url, output_path)
print(f"\n✅ 完成: {output_path}")
