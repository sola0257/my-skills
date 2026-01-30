#!/usr/bin/env python3
"""
测试 DeepRouter Imagine 完整流程（不带人物参考）
"""
import sys
sys.path.append('/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书')

from deeprouter_mj_api import DeepRouterMJ

# 初始化 API
api = DeepRouterMJ("sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I")

# 植物场景 prompt（不带人物）
prompt = """
Bright living room corner with various green plants on wooden shelves and floor,
spring sunlight streaming through sheer curtains, pothos, monstera, and orchids
in ceramic pots, wooden furniture, cream walls, cozy atmosphere,
lifestyle photography, dreamy realistic style, soft focus, film-like quality,
muted Morandi colors, low saturation
"""

print("🎨 测试完整流程：生成植物场景图（不带人物）")
print("=" * 60)

# 提交任务
task_id = api.submit_imagine(prompt)
if not task_id:
    print("❌ 任务提交失败")
    sys.exit(1)

# 等待完成
image_url = api.wait_for_result(task_id, max_wait=300)
if not image_url:
    print("❌ 生成失败")
    sys.exit(1)

# 下载图片
output_path = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/test_plant_scene.png"
success = api.download_image(image_url, output_path)

if success:
    print("\n✅ 测试成功！图片已保存")
    print(f"📁 位置: {output_path}")
