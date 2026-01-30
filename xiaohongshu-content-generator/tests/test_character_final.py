#!/usr/bin/env python3
"""
测试使用 ImgBB URL 生成带人物的图片
"""
import sys
sys.path.append('/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书')

from deeprouter_mj_api import DeepRouterMJ

# 初始化 API
api = DeepRouterMJ("sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I")

# 植物场景 prompt（带人物）
prompt = """
A woman in cream linen dress standing in a bright living room corner,
surrounded by green plants including pothos, monstera, and orchids in ceramic pots,
gently touching plant leaves, soft natural window light streaming through sheer curtains,
warm golden hour glow, wooden furniture, cream walls, peaceful and fresh mood,
lifestyle photography, dreamy realistic style, soft focus, film-like quality,
muted Morandi colors, low saturation
"""

# 使用 ImgBB 上传的照片 URL
character_url = "https://i.ibb.co/WNTZrtcQ/primary-ref.jpg"

print("🎨 测试带人物一致性的图片生成")
print(f"📷 参考照片: {character_url}")
print("=" * 60)

# 提交任务（带 --cref）
task_id = api.submit_imagine(prompt, character_url)
if not task_id:
    print("❌ 任务提交失败")
    sys.exit(1)

# 等待完成
image_url = api.wait_for_result(task_id, max_wait=300)
if not image_url:
    print("❌ 生成失败")
    sys.exit(1)

# 下载图片
output_path = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/test_character_ref_final.png"
success = api.download_image(image_url, output_path)

if success:
    print("\n✅ 测试成功！带人物的图片已生成")
    print(f"📁 位置: {output_path}")
