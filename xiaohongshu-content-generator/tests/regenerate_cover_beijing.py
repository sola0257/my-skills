#!/usr/bin/env python3
"""
重新生成小红书封面图 - 北京家庭真实阳台版
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

    print(f"🎨 正在生成封面图（北京家庭真实阳台版）...")
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
    # 封面 Prompt - 北京家庭真实阳台
    cover_prompt = """Generate an image: A 3:4 photograph in dreamy realistic style.

Scene: A typical Beijing apartment enclosed balcony in winter, warm and cozy inside with heating. The balcony has white aluminum window frames with large glass panels, showing a glimpse of winter cityscape outside. Inside, the balcony is transformed into a vibrant spring flower garden.

Space: A compact but well-organized balcony space (about 3-4 square meters), typical of Beijing apartments. Beige or light gray ceramic tile flooring. The space feels lived-in and practical.

Plants: Various colorful spring flowering plants arranged on simple wooden shelves and metal plant stands at different heights. Pink hydrangeas, white orchids, purple petunias, yellow primroses, red geraniums, and other blooming flowers in ceramic and plastic pots. The plants are lush and healthy, thriving in the warm indoor environment.

Details: Simple wooden ladder-style plant shelf against the wall, a small metal rolling cart with plants, ceramic pots in cream and terracotta colors, some plastic nursery pots. A small watering can on the floor. Maybe a folded drying rack visible in the corner (typical Beijing balcony element). Everything is practical and achievable for regular families.

Lighting: Soft natural daylight coming through the large windows, creating a warm and bright atmosphere despite the winter outside. Gentle shadows on the tile floor.

Mood: Warm, cozy, hopeful - the contrast between cold winter outside and vibrant spring flowers inside. The scene conveys "bringing spring indoors" and "anyone can create this beautiful space."

Color palette: Soft spring flower colors (pink, purple, yellow, white) against neutral backgrounds (white window frames, beige tiles, cream walls). Muted Morandi tones with pops of vibrant flower colors. Low saturation, warm undertones.

Style: Realistic lifestyle photography, authentic Beijing apartment aesthetic. Slightly dreamy but very achievable and relatable. Film-like quality with soft focus.

NO TEXT. NO WORDS. NO LETTERS. NO WATERMARKS."""

    # 输出路径
    output_dir = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/2026-01-14_春季必买8种开花植物"
    output_path = os.path.join(output_dir, "春季必买8种开花植物_封面_v3.png")

    # 生成图片
    success = generate_image_yunwu(cover_prompt, output_path)

    if success:
        print("\n" + "="*60)
        print("✅ 封面图生成完成！")
        print(f"📁 保存位置: {output_path}")
        print("\n🏠 场景特点：")
        print("  - 北京典型封闭式阳台")
        print("  - 白色铝合金窗框")
        print("  - 瓷砖地面")
        print("  - 紧凑但温馨的空间")
        print("  - 窗外冬景，室内春意盎然")
        print("="*60)
    else:
        print("\n❌ 封面图生成失败，请检查错误信息")


if __name__ == "__main__":
    main()
