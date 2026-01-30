#!/usr/bin/env python3
"""
方案A：Gemini 添加文字 + Python 调整尺寸
增加反 AI 痕迹规则
"""
import requests
import base64
import re
from pathlib import Path
from PIL import Image

def add_text_with_gemini_v2(base_image_path, title_text, output_path):
    """
    使用 Gemini 添加文字，包含反 AI 痕迹规则
    """
    # Gemini API 配置
    gemini_url = "https://yunwu.ai/v1/chat/completions"
    gemini_api_key = "sk-UqMsXIWjukWom3cHPkbf5xBqYrnEJHz3J7cdQQNhkFg974X5"

    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }

    # 读取底图
    print(f"📖 读取底图: {base_image_path}")
    with open(base_image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    # 构建 prompt（包含反 AI 痕迹规则）
    prompt = f"""
请在这张图片上添加中文标题文字。

⚠️ 重要：必须保持原图的尺寸和比例（3:4竖版）

标题内容：{title_text}

设计要求：
- 尺寸：保持原图尺寸和3:4竖版比例
- 字体：粗体黑体，易读性强
- 位置：图片上方1/3处，略微偏左或偏右（不要完全居中，避免过度对称）
- 颜色：白色文字 + 黑色描边，或根据背景选择对比度高的颜色
- 背景：文字下方添加半透明背景条，边缘略微不规则（避免完美矩形）
- 风格：小红书封面风格，简洁大气
- 字号：大而醒目，占据图片宽度的70-80%

⚠️ 反 AI 痕迹规则（必须遵守）：
1. 避免完全对称的布局 - 文字位置略微偏移，不要正中央
2. 避免过度完美 - 背景条边缘可以略微不规则
3. 保持自然感 - 文字排版要有呼吸感，不要过于紧凑
4. 避免重复元素 - 不要添加多余的装饰图案
5. 保持真实感 - 像真人设计师做的封面，而不是 AI 生成的

请生成添加了标题后的图片，确保：
1. 保持原图的3:4竖版比例
2. 文字清晰、美观、自然
3. 避免 AI 生成的痕迹（过度对称、过度完美）
"""

    payload = {
        "model": "gemini-3-pro-image-preview",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        print(f"🎨 使用 Gemini 添加文字：{title_text}")
        print("⏳ 请求中...")

        response = requests.post(
            gemini_url,
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # 提取 Base64 图片数据
        match = re.search(r"data:image/\w+;base64,([^)]+)", content)
        if not match:
            print("❌ 未能在响应中找到图片数据")
            return False

        image_data = match.group(1)

        # 保存临时图片
        temp_path = output_path.replace(".png", "_temp.png")
        Path(temp_path).parent.mkdir(parents=True, exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        print(f"✅ Gemini 处理完成")

        # 调整到标准尺寸 1080×1440
        print(f"📐 调整尺寸到 1080×1440...")
        img = Image.open(temp_path)
        img_resized = img.resize((1080, 1440), Image.LANCZOS)
        img_resized.save(output_path, quality=95)

        # 删除临时文件
        Path(temp_path).unlink()

        print(f"✅ 最终封面已保存: {output_path}")

        # 验证尺寸
        final_img = Image.open(output_path)
        print(f"📏 最终尺寸: {final_img.size[0]}×{final_img.size[1]}")

        return True

    except Exception as e:
        print(f"❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🎨 测试方案A：Gemini + 尺寸调整 + 反AI痕迹")
    print("=" * 60)

    # 使用之前生成的图片
    base_image = "/Users/dj/.claude/skills/xiaohongshu-content-generator/tests/test_xiaohongshu_style.png"

    # 测试标题
    title = "春日居家绿植装饰指南"

    # 输出路径
    output = "/Users/dj/.claude/skills/xiaohongshu-content-generator/tests/test_gemini_final.png"

    # 执行测试
    success = add_text_with_gemini_v2(base_image, title, output)

    if success:
        print("\n" + "=" * 60)
        print("✅ 测试完成！")
        print(f"📁 原图: {base_image}")
        print(f"📁 最终封面: {output}")
        print("=" * 60)

        # 自动打开查看
        import subprocess
        subprocess.run(["open", output])
    else:
        print("\n❌ 测试失败")
