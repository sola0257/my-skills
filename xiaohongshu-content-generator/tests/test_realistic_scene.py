#!/usr/bin/env python3
"""
改进版：真实场景 + 亚洲人物 + 环境为主
"""
import sys
sys.path.append('/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书')

from deeprouter_mj_api import DeepRouterMJ

api = DeepRouterMJ("sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I")

# 改进的 prompt - 强调真实性和亚洲人物特征
prompt = """
cozy living room corner with lush green plants, pothos and monstera in ceramic pots
on low wooden shelves and floor level, easy to reach and water,
an Asian woman with long black hair in a bun, wearing cream linen dress,
standing with her back to camera, gently touching plant leaves,
soft natural window light, peaceful home atmosphere,
plants are the main focus, realistic and practical plant arrangement,
lifestyle photography, dreamy style, muted Morandi colors, film grain,
warm and inviting mood
"""

print("🎨 测试改进版生成（真实场景 + 亚洲人物）")
print("=" * 60)

task_id = api.submit_imagine(prompt)
if not task_id:
    sys.exit(1)

image_url = api.wait_for_result(task_id, max_wait=300)
if not image_url:
    sys.exit(1)

output_path = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/test_realistic_asian.png"
api.download_image(image_url, output_path)
print(f"\n✅ 完成: {output_path}")
