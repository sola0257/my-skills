#!/usr/bin/env python3
import argparse
import json
import os
import sys
import requests
import base64
import re

# API 配置
YUNWU_API_URL = "https://yunwu.ai/v1/chat/completions"
YUNWU_API_KEY = "sk-UqMsXIWjukWom3cHPkbf5xBqYrnEJHz3J7cdQQNhkFg974X5"
YUNWU_MODEL = "gemini-3-pro-image-preview"

def generate_image_yunwu(prompt, output_path, aspect_ratio="3:4"):
    """使用云雾 API 生成图片

    Args:
        prompt: 图片生成提示词
        output_path: 输出路径
        aspect_ratio: 图片比例，默认3:4（小红书竖版）
    """
    headers = {
        "Authorization": f"Bearer {YUNWU_API_KEY}",
        "Content-Type": "application/json"
    }

    # 添加尺寸约束
    size_hint = "Image size: 1080x1440 pixels (3:4 vertical format for Xiaohongshu)." if aspect_ratio == "3:4" else ""
    full_prompt = f"{prompt}\n\n{size_hint}\n\nCRITICAL: NO TEXT, NO WORDS, NO LETTERS in the image."

    payload = {
        "model": YUNWU_MODEL,
        "messages": [
            {"role": "user", "content": full_prompt}
        ]
    }

    try:
        print(f"🎨 Generating image for {os.path.basename(output_path)}...")
        response = requests.post(YUNWU_API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        match = re.search(r"data:image/\w+;base64,([^)]+)", content)
        if not match:
            print("❌ No image data found in response")
            return False

        image_data = match.group(1)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_data))
            
        print(f"✅ Image saved: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Image generation failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate Xiaohongshu post content")
    parser.add_argument("--data", required=True, help="JSON string containing all post data")
    args = parser.parse_args()

    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        sys.exit(1)

    # 解析数据
    base_dir = data.get("base_dir")
    prompts = data.get("prompts", {})
    image_labels = data.get("image_labels", {})  # 中文文字说明

    if not base_dir:
        print("❌ base_dir is required")
        sys.exit(1)

    os.makedirs(base_dir, exist_ok=True)

    # 1. 生成封面（只生成底图，不叠加文字）
    cover_prompt = prompts.get("cover")
    if cover_prompt:
        cover_path = os.path.join(base_dir, "cover.png")
        generate_image_yunwu(cover_prompt, cover_path, aspect_ratio="3:4")

    # 2. 生成配图（支持中文标签命名）
    for key, prompt in prompts.items():
        if key == "cover":
            continue

        # 构建文件名：序号_中文标签.png
        label = image_labels.get(key, "")
        filename = f"{key}_{label}.png" if label else f"{key}.png"

        output_path = os.path.join(base_dir, filename)
        generate_image_yunwu(prompt, output_path, aspect_ratio="3:4")

    print("\n🎉 All tasks completed!")

if __name__ == "__main__":
    main()
