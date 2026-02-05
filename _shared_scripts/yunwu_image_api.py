#!/usr/bin/env python3
"""
云雾图片生成 API 统一客户端 v1.0
强制使用 Gemini 模型，所有 skills 必须通过此客户端调用
"""
import os
import sys
import json
import requests
import base64
import re
from pathlib import Path

# 加载全局配置
SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "_global_config"

# 读取 API 配置
with open(CONFIG_DIR / "api_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# 云雾 API 配置
YUNWU_CONFIG = config["yunwu"]
API_BASE_URL = YUNWU_CONFIG["base_url"]
API_ENDPOINT = YUNWU_CONFIG["chat_endpoint"]
FORCED_MODEL = config["image_generation"]["force_model"]

# 从环境变量或 .env 文件读取 API Key
def load_api_key():
    """加载 API Key（优先从环境变量，其次从 .env 文件）"""
    # 优先从环境变量读取
    api_key = os.getenv("YUNWU_API_KEY")
    if api_key:
        return api_key

    # 从 .env 文件读取
    env_file = CONFIG_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("YUNWU_API_KEY="):
                    return line.split("=", 1)[1].strip()

    raise ValueError("❌ 未找到 YUNWU_API_KEY，请检查环境变量或 .env 文件")

API_KEY = load_api_key()

def generate_image(prompt, output_path, aspect_ratio="3:4", allow_text=False):
    """
    使用云雾 API 生成图片（强制使用 Gemini 模型）

    Args:
        prompt: 图片生成提示词（应该已经包含完整的规范）
        output_path: 输出路径
        aspect_ratio: 图片比例，默认3:4（小红书竖版）
        allow_text: 是否允许图片中包含文字，默认False

    Returns:
        bool: 生成是否成功
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 添加尺寸约束
    if aspect_ratio == "3:4":
        size_hint = "Image size: 1080x1440 pixels (3:4 vertical format for Xiaohongshu)."
    elif aspect_ratio == "16:9":
        size_hint = "Image size: 900x506 pixels (16:9 horizontal format for WeChat)."
    elif aspect_ratio == "2.35:1":
        size_hint = "Image size: 900x383 pixels (2.35:1 horizontal format for WeChat cover)."
    else:
        size_hint = ""

    # 根据 allow_text 参数决定是否添加 NO TEXT 限制
    if allow_text:
        # 如果允许文字，不添加 NO TEXT 限制
        # Prompt 中应该已经包含了文字要求（如果需要的话）
        full_prompt = f"{prompt}\n\n{size_hint}"
    else:
        # 如果不允许文字，添加 NO TEXT 限制
        full_prompt = f"{prompt}\n\n{size_hint}\n\nNO TEXT, NO WORDS, NO LETTERS in the image."

    payload = {
        "model": FORCED_MODEL,  # 强制使用 Gemini 模型
        "messages": [
            {"role": "user", "content": full_prompt}
        ]
    }

    try:
        print(f"🎨 生成图片: {os.path.basename(output_path)}...")
        print(f"📌 使用模型: {FORCED_MODEL}")

        response = requests.post(
            f"{API_BASE_URL}{API_ENDPOINT}",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        match = re.search(r"data:image/\w+;base64,([^)]+)", content)
        if not match:
            print("❌ 未找到图片数据")
            return False

        image_data = match.group(1)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        print(f"✅ 图片已保存: {output_path}")
        return True

    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return False

def batch_generate(prompts_dict, base_dir, text_config=None, aspect_ratio="3:4"):
    """
    批量生成图片

    Args:
        prompts_dict: {filename: prompt} 字典
        base_dir: 输出目录
        text_config: {filename: allow_text} 字典，指定哪些图片需要文字
        aspect_ratio: 图片比例

    Returns:
        dict: {filename: success} 结果字典
    """
    if text_config is None:
        text_config = {}

    os.makedirs(base_dir, exist_ok=True)
    results = {}

    print("=" * 60)
    print(f"开始批量生成配图")
    print(f"目标目录: {base_dir}")
    print(f"总共 {len(prompts_dict)} 张图片")
    print(f"强制使用模型: {FORCED_MODEL}")
    print("=" * 60)

    for filename, prompt in prompts_dict.items():
        output_path = os.path.join(base_dir, filename)
        allow_text = text_config.get(filename, False)

        success = generate_image(prompt, output_path, aspect_ratio, allow_text)
        results[filename] = success
        print()

    print("=" * 60)
    success_count = sum(1 for v in results.values() if v)
    print(f"✅ 完成：{success_count}/{len(results)} 张图片生成成功")
    print("=" * 60)

    return results

if __name__ == "__main__":
    # 命令行测试接口
    if len(sys.argv) < 3:
        print("用法: python yunwu_image_api.py <prompt> <output_path> [aspect_ratio] [allow_text]")
        sys.exit(1)

    prompt = sys.argv[1]
    output_path = sys.argv[2]
    aspect_ratio = sys.argv[3] if len(sys.argv) > 3 else "3:4"
    allow_text = sys.argv[4].lower() == "true" if len(sys.argv) > 4 else False

    success = generate_image(prompt, output_path, aspect_ratio, allow_text)
    sys.exit(0 if success else 1)
