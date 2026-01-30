#!/usr/bin/env python3
"""
真实植物场景：多样化 + 自然摆放
"""
import sys
sys.path.append('/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书')

from deeprouter_mj_api import DeepRouterMJ

api = DeepRouterMJ("sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I")

# 真实多样化的植物场景
prompt = """
bright living room corner with diverse indoor plants naturally arranged,
large monstera and rubber plant on the floor near window,
trailing pothos hanging from wooden shelf,
white orchids and peace lilies with flowers on mid-level shelf,
small succulents and African violets on lower shelf,
plants in various ceramic and terracotta pots,
an Asian woman with long black hair in loose bun, wearing cream linen dress,
standing with back to camera, watering plants with a small watering can,
soft natural morning light through sheer curtains,
realistic home plant collection, varied heights and textures,
lifestyle photography, dreamy style, muted warm tones, film grain
"""

print("🎨 测试真实多样化植物场景")
print("=" * 60)

task_id = api.submit_imagine(prompt)
if not task_id:
    sys.exit(1)

image_url = api.wait_for_result(task_id, max_wait=300)
if not image_url:
    sys.exit(1)

output_path = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/test_realistic_variety.png"
api.download_image(image_url, output_path)
print(f"\n✅ 完成: {output_path}")
