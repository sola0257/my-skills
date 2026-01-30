#!/usr/bin/env python3
"""
小红书风格：真实家居植物场景
基于参考图片分析的改进版本
"""
import sys
sys.path.append('/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书')

from deeprouter_mj_api import DeepRouterMJ

api = DeepRouterMJ("sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I")

# 基于小红书参考图片风格的 prompt
prompt = """
bright modern living room corner with natural plant collection,
white phalaenopsis orchids in ceramic pots on wooden shelf,
large monstera deliciosa and boston ferns on floor near window,
trailing pothos in woven basket hanging from shelf,
pink hydrangeas and white lilies in glass vase on side table,
plants arranged at accessible heights with varied textures,
an Asian woman with long black hair in loose bun, wearing cream linen dress,
standing with back to camera, gently touching orchid petals,
soft golden hour sunlight through sheer white curtains,
warm peachy tones, clean minimalist interior, wooden furniture,
plants are the main subject, woman is ambient element in the scene,
lifestyle photography, natural authentic feel, slightly dreamy,
professional but lived-in atmosphere
"""

print("🎨 测试小红书风格场景")
print("=" * 60)

task_id = api.submit_imagine(prompt)
if not task_id:
    sys.exit(1)

image_url = api.wait_for_result(task_id, max_wait=300)
if not image_url:
    sys.exit(1)

output_path = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/test_xiaohongshu_style.png"
api.download_image(image_url, output_path)
print(f"\n✅ 完成: {output_path}")
