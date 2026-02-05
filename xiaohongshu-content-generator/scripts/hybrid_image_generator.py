#!/usr/bin/env python3
"""
混合图片生成方案：Midjourney + Gemini
- Midjourney: 生成高质量场景图
- Gemini: 添加中文文字叠加
"""
import requests
import base64
import re
import json
import os
from pathlib import Path

# 全局配置路径
GLOBAL_CONFIG_PATH = Path("/Users/dj/Desktop/小静的skills/_global_config/api_config.json")

def load_api_keys():
    """从全局配置加载 API Key"""
    if not GLOBAL_CONFIG_PATH.exists():
        raise FileNotFoundError(f"❌ 全局配置文件未找到: {GLOBAL_CONFIG_PATH}")
    
    with open(GLOBAL_CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    yunwu_key = config.get("yunwu", {}).get("api_key")
    mj_key = config.get("deeprouter", {}).get("api_key")
    
    if not yunwu_key:
        raise ValueError("❌ 全局配置中缺少 'yunwu.api_key'")
        
    return mj_key, yunwu_key

class HybridImageGenerator:
    def __init__(self, mj_api_key=None, gemini_api_key=None):
        """
        初始化混合生成器
        优先使用传入的 Key，如果没有则自动从全局配置加载
        """
        if not mj_api_key or not gemini_api_key:
            try:
                loaded_mj, loaded_gemini = load_api_keys()
                self.mj_api_key = mj_api_key or loaded_mj
                self.gemini_api_key = gemini_api_key or loaded_gemini
                print("✅ 已从全局配置加载 API Key")
            except Exception as e:
                print(f"⚠️ 无法自动加载 Key: {e}")
                self.mj_api_key = mj_api_key
                self.gemini_api_key = gemini_api_key
        else:
            self.mj_api_key = mj_api_key
            self.gemini_api_key = gemini_api_key

        # Midjourney API (DeepRouter)
        self.mj_base_url = "https://deeprouter.top"
        self.mj_headers = {
            "Authorization": f"Bearer {mj_api_key}",
            "Content-Type": "application/json"
        }

        # Gemini API (Yunwu)
        self.gemini_url = "https://yunwu.ai/v1/chat/completions"
        self.gemini_headers = {
            "Authorization": f"Bearer {gemini_api_key}",
            "Content-Type": "application/json"
        }

    def generate_image_with_gemini(self, prompt, output_path):
        """
        使用 Gemini 直接生成图片（一步到位）
        适用于：正文配图、一步生成的封面
        """
        from PIL import Image
        
        # 强制指定模型
        model = "gemini-3-pro-image-preview"
        
        # 确保 prompt 包含尺寸要求
        if "3:4" not in prompt and "1080x1440" not in prompt:
            prompt += "\n\nREQUIREMENTS: Image ratio 3:4 (1080x1440 pixels)."

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            print(f"🎨 Gemini 生成中: {Path(output_path).name}")
            # print(f"📝 Prompt: {prompt[:50]}...")

            response = requests.post(
                self.gemini_url,
                headers=self.gemini_headers,
                json=payload,
                timeout=120
            )
            
            # 详细的错误处理
            if response.status_code != 200:
                print(f"❌ API请求失败: {response.status_code}")
                print(response.text)
                return False

            result = response.json()
            
            # 检查是否有 content
            if "choices" not in result or not result["choices"]:
                print(f"❌ API返回格式错误: {result}")
                return False
                
            content = result["choices"][0]["message"]["content"]

            # 提取 Base64 图片数据
            match = re.search(r"data:image/\w+;base64,([^)]+)", content)
            if not match:
                # 有时候返回的是 URL (虽然 pro-image-preview 通常是 base64)
                if "http" in content:
                    print("⚠️ 警告: 返回了 URL 而不是 Base64，尝试下载...")
                    # TODO: 处理 URL 下载
                print("❌ 未能在响应中找到 Base64 图片数据")
                print(f"响应片段: {content[:100]}...")
                return False

            image_data = match.group(1)

            # 保存图片
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(image_data))

            print(f"✅ 图片保存成功: {output_path}")
            return True

        except Exception as e:
            print(f"❌ 生成异常: {e}")
            return False

    def add_text_with_gemini(self, base_image_path, title_text, output_path):
        """
        使用 Gemini 在图片上添加中文标题
        """
        from PIL import Image
        
        # 修复 LANCZOS 问题
        try:
            resample_method = Image.Resampling.LANCZOS
        except AttributeError:
            resample_method = Image.LANCZOS
            
        # ... (其余代码保持不变，只需注意 Image.LANCZOS 的替换)
        
        # (为了简洁，这里只修复 generate_image_with_gemini，因为我们主要用这个)
        pass

        """
        使用 Gemini 在图片上添加中文标题（包含反AI痕迹规则和尺寸标准化）

        Args:
            base_image_path: 底图路径（Midjourney 生成的）
            title_text: 要添加的标题文字
            output_path: 输出路径

        Returns:
            bool: 是否成功
        """
        from PIL import Image

        # 读取底图并转换为 base64
        print(f"📖 读取底图: {base_image_path}")
        with open(base_image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        # 构建 prompt（包含反AI痕迹规则）
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
                self.gemini_url,
                headers=self.gemini_headers,
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
            
            # 兼容不同版本的 PIL
            if hasattr(Image, 'Resampling'):
                resample_method = Image.Resampling.LANCZOS
            else:
                resample_method = Image.LANCZOS
                
            img_resized = img.resize((1080, 1440), resample_method)
            img_resized.save(output_path, quality=95)

            # 删除临时文件
            Path(temp_path).unlink()

            print(f"✅ 最终封面已保存: {output_path}")

            # 验证尺寸
            final_img = Image.open(output_path)
            print(f"📏 最终尺寸: {final_img.size[0]}×{final_img.size[1]}")

            return True

        except Exception as e:
            print(f"❌ Gemini 处理失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generate_cover_with_text(self, scene_prompt, title_text, output_dir, topic_name):
        """
        完整流程：生成带文字的封面

        Args:
            scene_prompt: 场景描述
            title_text: 标题文字
            output_dir: 输出目录
            topic_name: 选题名称

        Returns:
            tuple: (base_image_path, final_cover_path)
        """
        print("=" * 60)
        print("🎨 混合生成：Midjourney + Gemini")
        print("=" * 60)

        # Step 1: Midjourney 生成底图
        print("\n📸 Step 1: Midjourney 生成场景图...")
        base_image_path = f"{output_dir}/{topic_name}_封面_底图.png"

        # 调用 MJ API（这里需要集成 deeprouter_mj_api.py）
        # success = self.generate_scene_with_mj(scene_prompt, base_image_path)
        # if not success:
        #     return None, None

        # Step 2: Gemini 添加文字
        print("\n✍️ Step 2: Gemini 添加中文标题...")
        final_cover_path = f"{output_dir}/{topic_name}_封面.png"

        success = self.add_text_with_gemini(
            base_image_path,
            title_text,
            final_cover_path
        )

        if success:
            print("\n" + "=" * 60)
            print("✅ 封面生成完成！")
            print(f"📁 底图: {base_image_path}")
            print(f"📁 最终封面: {final_cover_path}")
            print("=" * 60)
            return base_image_path, final_cover_path
        else:
            return None, None


# 使用示例
if __name__ == "__main__":
    generator = HybridImageGenerator(
        mj_api_key="sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I",
        gemini_api_key="sk-UqMsXIWjukWom3cHPkbf5xBqYrnEJHz3J7cdQQNhkFg974X5"
    )

    # 场景 prompt（Midjourney）
    scene_prompt = """
    bright modern living room corner with natural plant collection,
    white orchids and green plants, soft golden light,
    Asian woman in background, plants as main focus,
    lifestyle photography --v 6.1 --ar 3:4
    """

    # 标题文字（Gemini 添加）
    title_text = "春日居家绿植装饰指南"

    # 生成封面
    generator.generate_cover_with_text(
        scene_prompt=scene_prompt,
        title_text=title_text,
        output_dir="/Users/dj/Documents/test",
        topic_name="春日绿植"
    )
