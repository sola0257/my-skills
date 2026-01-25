#!/usr/bin/env python3
import argparse
import json
import os
import sys
import requests
import base64
import re
from cover_generator import CoverGenerator

# API 配置
YUNWU_API_URL = "https://yunwu.ai/v1/chat/completions"
YUNWU_API_KEY = "sk-UqMsXIWjukWom3cHPkbf5xBqYrnEJHz3J7cdQQNhkFg974X5"
YUNWU_MODEL = "gemini-3-pro-image-preview"

def generate_image_yunwu(prompt, output_path):
    """使用云雾 API 生成图片"""
    headers = {
        "Authorization": f"Bearer {YUNWU_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 强制添加中文约束和清晰度要求
    full_prompt = f"{prompt}\n\nCRITICAL: Use ONLY Chinese characters for ALL text - must be CLEAR and LEGIBLE - Text must NOT be distorted or blurry."

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
    visual_title = data.get("visual_title")
    search_title = data.get("search_title") # 副标题用搜索标题
    prompts = data.get("prompts", {})
    
    if not base_dir:
        print("❌ base_dir is required")
        sys.exit(1)
        
    os.makedirs(base_dir, exist_ok=True)
    
    # 1. 生成封面底图
    cover_prompt = prompts.get("cover")
    if cover_prompt:
        base_cover_path = os.path.join(base_dir, "cover_base.png")
        if generate_image_yunwu(cover_prompt, base_cover_path):
            # 2. 合成封面 (调用 CoverGenerator)
            print("🎨 Composing cover with text...")
            generator = CoverGenerator()
            final_cover_path = os.path.join(base_dir, "cover_final.png")
            
            success = generator.generate(
                base_image_path=base_cover_path,
                title=visual_title,
                subtitle=search_title, # 使用长尾关键词作为副标题
                output_path=final_cover_path,
                layout_type="auto"
            )
            
            if success:
                print(f"✅ Final cover created: {final_cover_path}")
                # 能够成功合成后，可以选择删除底图，或者保留作为备份
                # os.remove(base_cover_path) 
            else:
                print("❌ Cover composition failed")
    
    # 3. 生成其他配图
    for key, prompt in prompts.items():
        if key == "cover":
            continue
        
        output_path = os.path.join(base_dir, f"{key}.png")
        generate_image_yunwu(prompt, output_path)

    print("\n🎉 All tasks completed!")

if __name__ == "__main__":
    main()
