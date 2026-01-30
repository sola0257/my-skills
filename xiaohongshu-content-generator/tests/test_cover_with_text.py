#!/usr/bin/env python3
import requests
import base64
import os
import re

def generate_image_yunwu(prompt: str, output_path: str):
    """使用云雾 API 生成图片"""
    url = "https://yunwu.ai/v1/chat/completions"

    headers = {
        "Authorization": "Bearer sk-UqMsXIWjukWom3cHPkbf5xBqYrnEJHz3J7cdQQNhkFg974X5",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gemini-3-pro-image-preview",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        print(f"🎨 生成图片中...")
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        match = re.search(r"data:image/\w+;base64,([^)]+)", content)
        if not match:
            print("❌ 未能在响应中找到图片数据")
            return False

        image_data = match.group(1)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        print(f"✅ 图片已保存: {os.path.basename(output_path)}")
        return True

    except Exception as e:
        print(f"❌ 图片生成失败: {e}")
        return False

# 测试：生成带文字的封面图
cover_prompt = """A 3:4 photograph in dreamy realistic style with Chinese text overlay.
Scene: Bright living room corner with various green plants on wooden shelves and floor, spring sunlight streaming through sheer curtains.
Lighting: Soft natural light, warm golden hour glow, gentle shadows.
Details: Mix of pothos, monstera, and small succulents in ceramic pots, wooden furniture, cream walls, cozy atmosphere.
Mood: Fresh, peaceful, spring renewal, natural living.
Color palette: Muted Morandi colors, low saturation, cream, sage green, warm wood tones.
Style: Realistic photography with soft focus, film-like quality, Instagram aesthetic.
Text overlay: "绿植这样摆 家秒变春天" in clean Chinese font, positioned at top center, white text with subtle shadow for readability."""

output_path = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/2026-01-13_春日居家绿植装饰/春日居家绿植装饰_封面_v2.png"

print("📸 生成带文字的封面图...")
generate_image_yunwu(cover_prompt, output_path)
print("\n✅ 测试完成！")
