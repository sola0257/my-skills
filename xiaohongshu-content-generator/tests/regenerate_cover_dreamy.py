#!/usr/bin/env python3
"""
重新生成小红书封面图 - 强化柔焦和胶片感
选题：春天养这8种花，美到邻居天天来问品种🌸
"""

import requests
import base64
import os
import re

def generate_image_yunwu(prompt: str, output_path: str):
    """
    使用云雾 API (Gemini) 生成图片
    """
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

    print(f"🎨 正在生成封面图（强化柔焦和胶片感）...")
    print(f"📝 Prompt: {prompt[:100]}...")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # 提取 Base64 数据
        match = re.search(r"data:image/\w+;base64,([^)]+)", content)
        if not match:
            print("❌ 未能在响应中找到图片数据")
            return False

        image_data = match.group(1)

        # 保存图片
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        print(f"✅ 封面图已保存: {output_path}")
        return True

    except Exception as e:
        print(f"❌ 图片生成失败: {e}")
        return False


def main():
    # 封面 Prompt - 强化柔焦、胶片感、梦幻氛围
    cover_prompt = """Generate an image: A 3:4 photograph in dreamy realistic style with strong soft focus and film aesthetic.

Scene: A Beijing apartment enclosed balcony corner, white aluminum window frames with soft natural light streaming in. The balcony is filled with various colorful spring flowering plants on simple wooden shelves and stands.

Plants: Pink hydrangeas, white orchids, purple petunias, yellow primroses, and other spring blooms in ceramic pots. The flowers are slightly out of focus, creating a dreamy, romantic atmosphere. Some flowers in foreground are blurred, some in background are softly focused.

Details: Simple wooden ladder shelf, small metal plant stand, ceramic pots in cream and terracotta. Beige tile floor. Everything has a soft, gentle appearance with natural imperfections - slightly asymmetric arrangement, casual placement.

Lighting: Soft golden hour light, warm peachy glow filtering through the windows. Gentle lens flare, subtle light leaks. The light creates a hazy, dreamy atmosphere.

Mood: Dreamy, romantic, nostalgic, peaceful. Like a memory of spring. Soft and gentle, not sharp or clinical.

Color palette: Muted Morandi colors with very low saturation. Cream, dusty pink, soft lavender, pale yellow, sage green. Desaturated pastels. Warm peachy undertones. Faded vintage color grading.

Style: SOFT FOCUS film photography aesthetic. Shot on vintage film camera (Fujifilm or Kodak). Visible film grain texture. Gentle bokeh effect. Slightly blurred, dreamy, ethereal quality. NOT sharp or crisp. The image should feel soft, romantic, and slightly hazy - like looking through a dreamy filter. Imperfect focus adds to the beauty.

Technical: Shallow depth of field, f/1.8 aperture, 35mm film, soft vignetting, gentle blur, romantic atmosphere.

NO TEXT. NO WORDS. NO LETTERS. NO WATERMARKS."""

    # 输出路径
    output_dir = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/2026-01-14_春季必买8种开花植物"
    output_path = os.path.join(output_dir, "春季必买8种开花植物_封面_v4.png")

    # 生成图片
    success = generate_image_yunwu(cover_prompt, output_path)

    if success:
        print("\n" + "="*60)
        print("✅ 封面图生成完成！")
        print(f"📁 保存位置: {output_path}")
        print("\n🎨 风格特点：")
        print("  - 强化柔焦效果（soft focus）")
        print("  - 胶片质感（film grain）")
        print("  - 低饱和度莫兰迪色调")
        print("  - 梦幻、浪漫的氛围")
        print("  - 自然的不完美感")
        print("="*60)
    else:
        print("\n❌ 封面图生成失败，请检查错误信息")


if __name__ == "__main__":
    main()
