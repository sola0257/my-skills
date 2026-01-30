#!/usr/bin/env python3
"""
测试 Gemini 添加中文文字叠加效果
"""
import requests
import base64
import re
from pathlib import Path

def add_text_with_gemini(base_image_path, title_text, output_path):
    """
    使用 Gemini 在图片上添加中文标题
    """
    # Gemini API 配置
    gemini_url = "https://yunwu.ai/v1/chat/completions"
    gemini_api_key = "sk-UqMsXIWjukWom3cHPkbf5xBqYrnEJHz3J7cdQQNhkFg974X5"

    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }

    # 读取底图并转换为 base64
    print(f"📖 读取底图: {base_image_path}")
    with open(base_image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    # 构建 prompt
    prompt = f"""
请在这张图片上添加中文标题文字。

⚠️ 重要：必须保持原图的尺寸和比例（3:4竖版，1080×1440或更高分辨率）

标题内容：{title_text}

设计要求：
- 尺寸：保持原图尺寸和3:4竖版比例，不要改变
- 字体：粗体黑体，易读性强
- 位置：图片上方1/3处，居中对齐
- 颜色：白色文字 + 黑色描边，或根据背景自动选择对比度最高的颜色
- 背景：文字下方添加半透明黑色或白色背景条，确保文字清晰可读
- 风格：小红书封面风格，简洁大气，吸引眼球
- 字号：大而醒目，占据图片宽度的70-80%

请生成添加了标题后的图片，确保：
1. 保持原图的3:4竖版比例
2. 文字清晰、美观、符合小红书平台风格
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

        print(f"📝 Gemini 响应: {content[:200]}...")

        # 提取 Base64 图片数据
        match = re.search(r"data:image/\w+;base64,([^)]+)", content)
        if not match:
            print("❌ 未能在响应中找到图片数据")
            print(f"完整响应: {content}")
            return False

        image_data = match.group(1)

        # 保存图片
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        print(f"✅ 带文字的封面已保存: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Gemini 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🎨 测试 Gemini 文字叠加功能")
    print("=" * 60)

    # 使用之前生成的小红书风格图片作为底图
    base_image = "/Users/dj/.claude/skills/xiaohongshu-content-generator/tests/test_xiaohongshu_style.png"

    # 测试标题
    title = "春日居家绿植装饰指南"

    # 输出路径
    output = "/Users/dj/.claude/skills/xiaohongshu-content-generator/tests/test_gemini_text_overlay.png"

    # 执行测试
    success = add_text_with_gemini(base_image, title, output)

    if success:
        print("\n" + "=" * 60)
        print("✅ 测试完成！")
        print(f"📁 原图: {base_image}")
        print(f"📁 带文字: {output}")
        print("=" * 60)

        # 自动打开查看
        import subprocess
        subprocess.run(["open", output])
    else:
        print("\n❌ 测试失败")
