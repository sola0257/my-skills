#!/usr/bin/env python3
"""
测试 Midjourney API - 生成带人物的植物场景封面
"""
import sys
sys.path.append('/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书')

from midjourney_api import MidjourneyAPI

# 初始化 API
api = MidjourneyAPI("sk-92m3Pkv3lmHSHrtg3NFHalSOTJr4wUSeeqIfPLft959Fu3AS")

# 植物场景 prompt（参考之前分析的8张图片风格）
prompt = """
A woman in cream linen dress standing in a bright living room corner,
surrounded by green plants including pothos, monstera, and orchids in ceramic pots,
gently touching plant leaves, soft natural window light streaming through sheer curtains,
warm golden hour glow, wooden furniture, cream walls, peaceful and fresh mood,
lifestyle photography, dreamy realistic style, soft focus, film-like quality,
muted Morandi colors, low saturation
"""

# 使用最佳参考照片
character_image = "/Users/dj/Downloads/IMG_4267.HEIC"

# 输出路径
output_path = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/test_mj_character_ref.png"

# 执行生成
print("🎨 开始测试 Midjourney 人物一致性生成...")
print(f"📸 参考照片: IMG_4267.HEIC")
print(f"🌿 场景: 春日居家绿植装饰")
print("=" * 60)

api.generate_with_character(prompt, character_image, output_path)
