#!/usr/bin/env python3
"""
重新生成小红书封面图
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

    print(f"🎨 正在生成封面图...")
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
    # 封面 Prompt - 春季花园氛围
    cover_prompt = """Generate an image: A 3:4 photograph in dreamy realistic style.

Scene: A bright sunlit corner of a spring garden or balcony, filled with various colorful blooming flowers and plants. The scene shows a beautiful collection of spring flowering plants arranged on wooden shelves and plant stands at different heights.

Plants: A diverse mix of colorful spring flowers including pink hydrangeas, white orchids, purple petunias, yellow daffodils, red geraniums, and various other blooming plants in ceramic and terracotta pots. The flowers are lush and abundant, creating a vibrant spring garden atmosphere.

Details: Wooden plant shelves and simple metal plant stands, ceramic pots in cream and terracotta tones, some woven baskets, a small watering can visible in the corner. The arrangement feels natural and lived-in, not overly staged.

Lighting: Soft natural morning light streaming through, creating a warm golden glow. Gentle shadows and highlights on the flower petals.

Mood: Dreamy, warm, inviting, full of spring vitality and joy. The scene conveys "spring is here, it's the perfect time to grow flowers."

Color palette: Soft pastels with pops of vibrant spring colors - pink, purple, yellow, white, red. Muted Morandi tones for the background and pots. Low saturation, cream and sage undertones.

Style: Realistic lifestyle photography with soft focus, film-like quality, slightly dreamy aesthetic. The scene should feel authentic and achievable for home gardeners.

NO TEXT. NO WORDS. NO LETTERS. NO WATERMARKS."""

    # 输出路径
    output_dir = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/2026-01-14_春季必买8种开花植物"
    output_path = os.path.join(output_dir, "春季必买8种开花植物_封面_v2.png")

    # 生成图片
    success = generate_image_yunwu(cover_prompt, output_path)

    if success:
        print("\n" + "="*60)
        print("✅ 封面图生成完成！")
        print(f"📁 保存位置: {output_path}")
        print("="*60)
    else:
        print("\n❌ 封面图生成失败，请检查错误信息")


if __name__ == "__main__":
    main()
