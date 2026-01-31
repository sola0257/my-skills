#!/usr/bin/env python3
"""
插画风格转换器 - 核心生成脚本
将真实植物照片转换为多种艺术插画风格
"""
import requests
import base64
import re
import os
import json
from pathlib import Path
from datetime import datetime


def load_env_file(env_path):
    """
    加载 .env 文件中的环境变量

    Args:
        env_path: .env 文件路径

    Returns:
        dict: 环境变量字典
    """
    env_vars = {}
    if not os.path.exists(env_path):
        return env_vars

    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过注释和空行
            if not line or line.startswith('#'):
                continue
            # 解析 KEY=VALUE 格式
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    return env_vars

# 风格-模型映射表（固定配置，保证视觉一致性）
STYLE_MODEL_MAPPING = {
    "watercolor_oriental": "gemini-3-pro-image-preview",
    "watercolor_western": "gemini-3-pro-image-preview",
    "ink_oriental": "gemini-3-pro-image-preview",
    "ink_western": "gemini-3-pro-image-preview",
    "pencil_oriental": "gemini-3-pro-image-preview",
    "pencil_western": "gemini-3-pro-image-preview",
    "pencil_steps": "gemini-3-pro-image-preview",  # 强制（中文标注）
    "oil_oriental": "gemini-3-pro-image-preview",
    "oil_western": "gemini-3-pro-image-preview",
    "gouache_oriental": "gemini-3-pro-image-preview",
    "gouache_western": "gemini-3-pro-image-preview",
}

# 风格名称映射（用户友好名称 → 风格代码）
STYLE_NAME_MAPPING = {
    "清新水彩（东方）": "watercolor_oriental",
    "清新水彩（西方）": "watercolor_western",
    "水墨国画（东方）": "ink_oriental",
    "水墨国画（西方）": "ink_western",
    "细腻彩铅（东方）": "pencil_oriental",
    "细腻彩铅（西方）": "pencil_western",
    "细腻彩铅（步骤图）": "pencil_steps",
    "质感油画（东方）": "oil_oriental",
    "质感油画（西方）": "oil_western",
    "装饰彩绘（东方）": "gouache_oriental",
    "装饰彩绘（西方）": "gouache_western",
}

# 风格代码 → 中文名称（反向映射，用于文件夹命名）
STYLE_CODE_TO_NAME = {
    "watercolor_oriental": "清新水彩东方",
    "watercolor_western": "清新水彩西方",
    "ink_oriental": "水墨国画东方",
    "ink_western": "水墨国画西方",
    "pencil_oriental": "细腻彩铅东方",
    "pencil_western": "细腻彩铅西方",
    "pencil_steps": "细腻彩铅步骤图",
    "oil_oriental": "质感油画东方",
    "oil_western": "质感油画西方",
    "gouache_oriental": "装饰彩绘东方",
    "gouache_western": "装饰彩绘西方",
}


class IllustrationGenerator:
    def __init__(self, api_key=None):
        """
        初始化插画生成器

        Args:
            api_key: Yunwu API Key（如果不提供，从全局 .env 文件读取）
        """
        # 优先使用传入的 API Key
        if api_key:
            self.api_key = api_key
        else:
            # 尝试从环境变量读取
            self.api_key = os.getenv("YUNWU_API_KEY")

            # 如果环境变量没有，从全局 .env 文件读取
            if not self.api_key:
                global_env_path = "/Users/dj/Desktop/小静的skills/_global_config/.env"
                env_vars = load_env_file(global_env_path)
                self.api_key = env_vars.get("YUNWU_API_KEY")

        if not self.api_key:
            raise ValueError(
                "未找到 API Key，请检查：\n"
                "1. 环境变量 YUNWU_API_KEY\n"
                "2. 全局配置文件 /Users/dj/Desktop/小静的skills/_global_config/.env"
            )

        self.api_url = "https://yunwu.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 加载 Prompt 模板
        self.templates = self._load_templates()

    def _load_templates(self):
        """加载 Prompt 模板"""
        # 模板路径
        template_path = Path(__file__).parent.parent / "knowledge" / "style-prompt-templates.md"

        if not template_path.exists():
            print(f"⚠️ 警告：未找到模板文件 {template_path}")
            return {}

        # 这里简化处理，实际使用时可以解析 markdown 文件
        # 现在返回空字典，在实际调用时直接使用模板
        return {}

    def get_model_for_style(self, style_code):
        """
        获取风格对应的固定模型

        Args:
            style_code: 风格代码

        Returns:
            str: 模型名称
        """
        model = STYLE_MODEL_MAPPING.get(style_code)
        if not model:
            raise ValueError(f"未知风格代码: {style_code}")
        return model

    def generate_single_image(self, prompt, output_path, reference_image_path=None, max_retries=3):
        """
        生成单张图片

        Args:
            prompt: 生成 prompt
            output_path: 输出路径
            reference_image_path: 参考图片路径（可选，支持 Gemini multimodal）
            max_retries: 最大重试次数

        Returns:
            bool: 是否成功
        """
        for attempt in range(max_retries):
            try:
                print(f"🎨 生成图片 (尝试 {attempt + 1}/{max_retries})...")

                # 构建消息内容
                if reference_image_path and os.path.exists(reference_image_path):
                    # 读取参考图片并转换为 base64
                    with open(reference_image_path, 'rb') as f:
                        image_data = base64.b64encode(f.read()).decode('utf-8')

                    # 检测图片格式
                    ext = Path(reference_image_path).suffix.lower()
                    mime_type = {
                        '.jpg': 'image/jpeg',
                        '.jpeg': 'image/jpeg',
                        '.png': 'image/png',
                        '.webp': 'image/webp'
                    }.get(ext, 'image/jpeg')

                    # Multimodal 消息格式
                    messages = [{
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Reference image provided. Use this as visual reference for composition, subject details, and atmosphere.\n\n{prompt}"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_data}"
                                }
                            }
                        ]
                    }]
                    print(f"📷 使用参考图片: {reference_image_path}")
                else:
                    # 纯文本消息
                    messages = [{"role": "user", "content": prompt}]

                # 调用 API
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json={
                        "model": "gemini-3-pro-image-preview",
                        "messages": messages
                    },
                    timeout=120
                )

                if response.status_code != 200:
                    print(f"❌ API 调用失败: {response.status_code}")
                    print(f"响应内容: {response.text}")
                    continue

                # 提取 Base64 图片（参考 xiaohongshu 实现）
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # 使用正确的正则表达式提取 base64 数据
                base64_match = re.search(r"data:image/\w+;base64,([^)]+)", content)

                if not base64_match:
                    print("❌ 未找到图片数据")
                    print(f"响应内容: {content[:200]}...")
                    continue

                # 解码并保存
                base64_data = base64_match.group(1)
                image_data = base64.b64decode(base64_data)

                # 确保输出目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'wb') as f:
                    f.write(image_data)

                print(f"✅ 图片已保存: {output_path}")
                return True

            except Exception as e:
                print(f"❌ 生成失败: {str(e)}")
                if attempt < max_retries - 1:
                    print("⏳ 重试中...")
                    continue
                else:
                    print("❌ 达到最大重试次数，生成失败")
                    return False

        return False

    def generate_illustration(self, style_code, subject, details="", mood="", output_dir=None):
        """
        生成插画

        Args:
            style_code: 风格代码
            subject: 植物名称
            details: 细节描述
            mood: 情绪关键词
            output_dir: 输出目录

        Returns:
            str: 输出文件路径
        """
        # 获取固定模型
        model = self.get_model_for_style(style_code)
        print(f"📌 使用模型: {model}")

        # 构建 Prompt（这里使用简化版本，实际应该从模板文件读取）
        prompt = self._build_prompt(style_code, subject, details, mood)

        # 输出路径
        if not output_dir:
            output_dir = Path(__file__).parent.parent / ".tmp"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{style_code}_{timestamp}_{subject}.png"
        output_path = Path(output_dir) / filename

        # 生成图片
        success = self.generate_single_image(prompt, str(output_path))

        if success:
            return str(output_path)
        else:
            return None

    def generate_series(self, style_code, subject, details="", mood="", output_dir=None, reference_image_path=None):
        """
        生成4张系列插画（不同构图）

        Args:
            style_code: 风格代码
            subject: 植物名称
            details: 细节描述
            mood: 情绪关键词
            output_dir: 输出目录
            reference_image_path: 参考图片路径（可选）

        Returns:
            list: 输出文件路径列表
        """
        # 4种构图策略
        compositions = [
            {
                "name": "全景",
                "description": "Full view with environment",
                "prompt_addition": "Wide composition showing the complete plant with surrounding environment, establishing context and atmosphere. Include subtle background elements like soil, pot, or natural setting."
            },
            {
                "name": "中景",
                "description": "Medium shot focusing on subject",
                "prompt_addition": "Medium shot focusing on the main subject, showing overall form and key characteristics. Balanced composition with moderate detail."
            },
            {
                "name": "特写",
                "description": "Close-up of texture details",
                "prompt_addition": "Extreme close-up of leaf/petal texture, showing intricate details like veins, surface patterns, color gradations. Fill most of the frame with detailed texture."
            },
            {
                "name": "意境",
                "description": "Atmospheric mood shot",
                "prompt_addition": "Atmospheric composition with generous white space, emphasizing mood and emotion. Minimal subject presence, maximum breathing room, poetic and contemplative."
            }
        ]

        # 输出目录 - 使用发布记录目录
        if not output_dir:
            # 默认输出到发布记录目录
            base_dir = Path("/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/插画类")
            # 创建日期+画风+名称的文件夹
            from datetime import datetime
            date_str = datetime.now().strftime("%Y%m%d")
            # 获取画风的中文名称
            style_name = STYLE_CODE_TO_NAME.get(style_code, style_code)
            folder_name = f"{date_str}_{style_name}_{subject}"
            output_dir = base_dir / folder_name
        else:
            output_dir = Path(output_dir)

        os.makedirs(output_dir, exist_ok=True)

        output_paths = []

        for i, comp in enumerate(compositions, 1):
            print(f"\n{'='*60}")
            print(f"🎨 生成第 {i}/4 张: {comp['name']} - {comp['description']}")
            print(f"{'='*60}")

            # 构建带有构图指导的 Prompt
            base_prompt = self._build_prompt(style_code, subject, details, mood)
            full_prompt = f"{base_prompt}\n\nComposition: {comp['prompt_addition']}"

            # 输出路径 - 使用中文友好的文件名
            # 格式：序号_构图类型_主题简介.png
            filename = f"{i:02d}_{comp['name']}_{subject}.png"
            output_path = output_dir / filename

            # 生成图片
            success = self.generate_single_image(full_prompt, str(output_path), reference_image_path=reference_image_path)

            if success:
                output_paths.append(str(output_path))
            else:
                print(f"❌ 第 {i} 张生成失败")

        return output_paths

    def generate_style_steps(self, style_code, subject, details="", mood="", output_dir=None, reference_image_path=None):
        """
        生成任意风格的步骤图（5个步骤）- 通用方法

        Args:
            style_code: 风格代码
            subject: 植物名称
            details: 细节描述
            mood: 情绪关键词
            output_dir: 输出目录
            reference_image_path: 参考图片路径

        Returns:
            list: 输出文件路径列表
        """
        # 定义各风格的步骤
        style_steps = {
            "watercolor_oriental": [
                {"step": 1, "title": "草稿", "stage": "Light pencil sketch",
                 "details": "Gentle pencil outline, capturing basic composition and main forms."},
                {"step": 2, "title": "第一层水彩", "stage": "First watercolor wash",
                 "details": "Light, transparent wash establishing color zones and atmosphere."},
                {"step": 3, "title": "叠加层次", "stage": "Layering colors",
                 "details": "Building depth with multiple transparent layers, wet-on-wet technique."},
                {"step": 4, "title": "细节刻画", "stage": "Detail refinement",
                 "details": "Adding fine details, textures, and subtle color variations."},
                {"step": 5, "title": "完成", "stage": "Final artwork",
                 "details": f"{details if details else 'Completed watercolor illustration'}, with soft edges and breathing space."}
            ],
            "watercolor_western": [
                {"step": 1, "title": "草稿", "stage": "Detailed sketch",
                 "details": "Precise pencil drawing with clear contours and details."},
                {"step": 2, "title": "第一层水彩", "stage": "Base wash",
                 "details": "First layer of color, establishing light and shadow."},
                {"step": 3, "title": "叠加层次", "stage": "Color building",
                 "details": "Multiple layers for rich, saturated colors."},
                {"step": 4, "title": "细节刻画", "stage": "Fine details",
                 "details": "Botanical accuracy, veins, textures, highlights."},
                {"step": 5, "title": "完成", "stage": "Finished piece",
                 "details": f"{details if details else 'Completed botanical watercolor'}, vibrant and detailed."}
            ],
            "ink_oriental": [
                {"step": 1, "title": "构图", "stage": "Composition planning",
                 "details": "Light sketch establishing placement and negative space."},
                {"step": 2, "title": "墨稿", "stage": "Ink outline",
                 "details": "Expressive brushstrokes defining main forms with varying ink tones."},
                {"step": 3, "title": "淡彩", "stage": "Light color wash",
                 "details": "Subtle color accents, maintaining ink dominance."},
                {"step": 4, "title": "浓彩点睛", "stage": "Color accents",
                 "details": "Strategic color placement for visual interest and depth."},
                {"step": 5, "title": "完成", "stage": "Final artwork",
                 "details": f"{details if details else 'Completed ink painting'}, with poetic simplicity and intentional空白."}
            ],
            "pencil_oriental": [
                {"step": 1, "title": "线稿", "stage": "Line drawing",
                 "details": "Light pencil outline, basic shapes and contours only."},
                {"step": 2, "title": "铺底色", "stage": "Base color layer",
                 "details": "First layer of light color, establishing color zones."},
                {"step": 3, "title": "深化色彩", "stage": "Color deepening",
                 "details": "Adding layers, building color intensity, initial shading."},
                {"step": 4, "title": "细节刻画", "stage": "Detail refinement",
                 "details": "Adding fine details, textures, veins, subtle color variations."},
                {"step": 5, "title": "完成", "stage": "Final artwork",
                 "details": f"{details if details else 'Completed colored pencil illustration'}, polished and refined."}
            ],
            "pencil_western": [
                {"step": 1, "title": "线稿", "stage": "Detailed line work",
                 "details": "Precise pencil drawing with botanical accuracy."},
                {"step": 2, "title": "铺底色", "stage": "Base colors",
                 "details": "Even color application, establishing local colors."},
                {"step": 3, "title": "深化色彩", "stage": "Building values",
                 "details": "Layering for depth, shadows, and dimensional form."},
                {"step": 4, "title": "细节刻画", "stage": "Fine details",
                 "details": "Intricate textures, highlights, botanical precision."},
                {"step": 5, "title": "完成", "stage": "Finished illustration",
                 "details": f"{details if details else 'Completed botanical illustration'}, rich and realistic."}
            ],
            "oil_oriental": [
                {"step": 1, "title": "底稿", "stage": "Underpainting",
                 "details": "Tonal sketch establishing composition and values."},
                {"step": 2, "title": "底色", "stage": "Base colors",
                 "details": "Thin paint layer, establishing color harmony."},
                {"step": 3, "title": "中间色", "stage": "Middle tones",
                 "details": "Building form with medium-thick paint, soft brushwork."},
                {"step": 4, "title": "高光与细节", "stage": "Highlights and details",
                 "details": "Impasto highlights, subtle details, atmospheric depth."},
                {"step": 5, "title": "完成", "stage": "Final painting",
                 "details": f"{details if details else 'Completed oil painting'}, with poetic mood and soft edges."}
            ],
            "oil_western": [
                {"step": 1, "title": "底稿", "stage": "Detailed underpainting",
                 "details": "Precise tonal study, establishing light and shadow."},
                {"step": 2, "title": "底色", "stage": "Color blocking",
                 "details": "Bold color application, establishing composition."},
                {"step": 3, "title": "中间色", "stage": "Form building",
                 "details": "Thick paint application, dramatic brushstrokes."},
                {"step": 4, "title": "高光", "stage": "Highlights and texture",
                 "details": "Impasto highlights, rich textures, dramatic lighting."},
                {"step": 5, "title": "完成", "stage": "Finished oil painting",
                 "details": f"{details if details else 'Completed classical oil painting'}, with rich textures and depth."}
            ],
            "gouache_oriental": [
                {"step": 1, "title": "线稿", "stage": "Line drawing",
                 "details": "Clean outlines, decorative pattern planning."},
                {"step": 2, "title": "平涂底色", "stage": "Flat base colors",
                 "details": "Even color application, establishing color blocks."},
                {"step": 3, "title": "叠加色彩", "stage": "Color layering",
                 "details": "Adding secondary colors, pattern elements."},
                {"step": 4, "title": "装饰细节", "stage": "Decorative details",
                 "details": "Traditional patterns, ornamental elements, gold accents."},
                {"step": 5, "title": "完成", "stage": "Final artwork",
                 "details": f"{details if details else 'Completed decorative painting'}, with folk art charm."}
            ],
            "gouache_western": [
                {"step": 1, "title": "线稿", "stage": "Clean line work",
                 "details": "Precise outlines, modern design planning."},
                {"step": 2, "title": "平涂底色", "stage": "Flat color blocks",
                 "details": "Bold, even color application, graphic quality."},
                {"step": 3, "title": "叠加色彩", "stage": "Color additions",
                 "details": "Secondary colors, creating visual interest."},
                {"step": 4, "title": "装饰细节", "stage": "Design details",
                 "details": "Modern patterns, geometric elements, clean edges."},
                {"step": 5, "title": "完成", "stage": "Final illustration",
                 "details": f"{details if details else 'Completed modern illustration'}, with graphic design appeal."}
            ]
        }

        # 获取对应风格的步骤
        steps = style_steps.get(style_code)
        if not steps:
            print(f"⚠️ 警告：风格 {style_code} 没有定义步骤图，使用默认步骤")
            # 使用默认步骤
            steps = style_steps["pencil_oriental"]

        # 输出目录
        if not output_dir:
            # 默认输出到发布记录目录
            base_dir = Path("/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/插画类")
            date_str = datetime.now().strftime("%Y%m%d")
            style_name = STYLE_CODE_TO_NAME.get(style_code, style_code)
            folder_name = f"{date_str}_{style_name}_步骤图_{subject}"
            output_dir = base_dir / folder_name
        else:
            output_dir = Path(output_dir) / f"步骤图_{subject}"

        os.makedirs(output_dir, exist_ok=True)

        output_paths = []

        for step_info in steps:
            print(f"\n{'='*60}")
            print(f"📝 步骤 {step_info['step']}: {step_info['title']}")
            print(f"{'='*60}")

            # 构建步骤 Prompt
            base_prompt = self._build_prompt(style_code, subject, details, mood)
            step_prompt = f"""{base_prompt}

STEP {step_info['step']}/5: {step_info['stage']}
Stage description: {step_info['details']}
Show this specific stage of the drawing process, not the final result.
IMPORTANT: Based on the reference image, only add the elements for THIS step. Do not add elements from future steps.
Text overlay: Add Chinese text "步骤{step_info['step']}：{step_info['title']}" in upper left corner, clear handwritten style, soft cream color.
"""

            # 输出路径
            filename = f"步骤{step_info['step']}_{step_info['title']}.png"
            output_path = output_dir / filename

            # 生成图片
            success = self.generate_single_image(step_prompt, str(output_path), reference_image_path=reference_image_path)

            if success:
                output_paths.append(str(output_path))
                # 关键修复：将当前步骤的输出作为下一步的参考图
                reference_image_path = str(output_path)
                print(f"✅ 步骤 {step_info['step']} 完成，将作为下一步的参考图")
            else:
                print(f"❌ 步骤 {step_info['step']} 生成失败")

        return output_paths

    def generate_pencil_steps(self, subject, details="", output_dir=None, reference_image_path=None):
        """
        生成彩铅步骤图（5个步骤）- 保留向后兼容

        Args:
            subject: 植物名称
            details: 细节描述
            output_dir: 输出目录
            reference_image_path: 参考图片路径（定稿图）

        Returns:
            list: 输出文件路径列表
        """
        # 调用通用方法
        return self.generate_style_steps("pencil_oriental", subject, details, "", output_dir, reference_image_path)
        steps = [
            {"step": 1, "title": "线稿", "stage": "Initial line drawing",
             "details": "Light pencil outline, basic shapes and contours only."},
            {"step": 2, "title": "铺底色", "stage": "Base color layer",
             "details": "First layer of light color, establishing color zones."},
            {"step": 3, "title": "深化色彩", "stage": "Color deepening",
             "details": "Adding layers, building color intensity, initial shading."},
            {"step": 4, "title": "细节刻画", "stage": "Detail refinement",
             "details": "Adding fine details, textures, veins, subtle color variations."},
            {"step": 5, "title": "完成", "stage": "Final artwork",
             "details": f"{details}, polished and refined." if details else "Completed illustration with all details."}
        ]

        # 输出目录
        if not output_dir:
            output_dir = Path(__file__).parent.parent / ".tmp" / f"pencil_steps_{subject}"
        else:
            output_dir = Path(output_dir) / f"pencil_steps_{subject}"

        os.makedirs(output_dir, exist_ok=True)

        output_paths = []

        for step_info in steps:
            print(f"\n{'='*60}")
            print(f"📝 步骤 {step_info['step']}: {step_info['title']}")
            print(f"{'='*60}")

            # 构建步骤 Prompt
            prompt = f"""
A 3:4 colored pencil illustration - STEP {step_info['step']}: {step_info['stage']}.
Subject: {subject}
Stage: {step_info['details']}
Style: Educational demonstration, showing progression.
Text overlay: Add Chinese text "步骤{step_info['step']}：{step_info['title']}" in upper left corner, clear handwritten style, soft cream color.
Paper: White drawing paper texture.
Image size: 1080x1440 pixels (3:4 vertical format).
"""

            # 输出路径
            filename = f"步骤{step_info['step']}_{step_info['title']}.png"
            output_path = output_dir / filename

            # 生成图片
            success = self.generate_single_image(prompt, str(output_path))

            if success:
                output_paths.append(str(output_path))
            else:
                print(f"❌ 步骤 {step_info['step']} 生成失败")

        return output_paths

    def _build_prompt(self, style_code, subject, details, mood):
        """
        构建 Prompt - 加入艺术家风格参考，优化构图

        Args:
            style_code: 风格代码
            subject: 植物名称
            details: 细节描述
            mood: 情绪关键词

        Returns:
            str: 完整 Prompt
        """
        # 艺术家风格参考映射
        artist_references = {
            "watercolor_oriental": {
                "artist": "Qi Baishi (齐白石)",
                "style_keywords": "Chinese freehand brushwork, expressive simplicity, poetic composition",
                "composition": "Subject occupies 40-50% of frame with intentional negative space for visual breathing room",
                "technique": "Delicate wet-on-wet washes, soft color bleeding, transparent layers, visible brushstrokes"
            },
            "watercolor_western": {
                "artist": "John Singer Sargent",
                "style_keywords": "gestural brushwork, delicate layering, luminous washes, confident strokes",
                "composition": "Subject occupies 60-70% of frame, dynamic composition with strong light-shadow contrast",
                "technique": "Loose but precise brushwork, layered transparent washes, hand-painted texture"
            },
            "ink_oriental": {
                "artist": "Bada Shanren (八大山人)",
                "style_keywords": "minimalist ink, profound simplicity, Zen aesthetics, vast emptiness",
                "composition": "Subject occupies 30-40% of frame, extreme minimalism with meaningful negative space",
                "technique": "Economical brushstrokes, ink gradations, expressive freedom"
            },
            "pencil_oriental": {
                "artist": "Margaret Mee",
                "style_keywords": "botanical illustration, scientific accuracy, delicate shading",
                "composition": "Subject occupies 70-80% of frame, specimen-style with complete details",
                "technique": "Fine pencil strokes, subtle layering, paper texture visible"
            },
            "oil_oriental": {
                "artist": "Henri Fantin-Latour",
                "style_keywords": "French Realism, floral still life, dramatic lighting, classical composition",
                "composition": "Subject occupies 70-80% of frame, classical still life arrangement",
                "technique": "Rich textures, visible brushstrokes, impasto effects, dramatic chiaroscuro"
            },
            "gouache_oriental": {
                "artist": "Dunhuang murals",
                "style_keywords": "decorative patterns, flat colors, ornamental design",
                "composition": "Subject occupies 60-70% of frame, pattern-based layout",
                "technique": "Flat color blocks, clear outlines, decorative elements"
            }
        }

        # 获取艺术家参考（如果没有则使用默认）
        ref = artist_references.get(style_code, {
            "artist": "Contemporary botanical artist",
            "style_keywords": "natural, authentic, hand-painted",
            "composition": "Subject occupies 60% of frame with balanced negative space",
            "technique": "Visible hand-made texture, organic edges, natural imperfections"
        })

        # 构建完整 Prompt
        prompt = f"""
Create a 3:4 vertical botanical illustration inspired by {ref['artist']}'s style.

SUBJECT: {subject}
{f"DETAILS: {details}" if details else ""}
{f"MOOD: {mood}" if mood else ""}

ARTISTIC STYLE:
- Style reference: {ref['style_keywords']}
- Technique: {ref['technique']}
- Avoid: AI-generated perfection, overly smooth gradients, generic stock photo look

COMPOSITION:
- {ref['composition']}
- Include contextual elements: subtle background (soil, pot rim, table surface, or natural setting)
- Avoid: empty void backgrounds, floating subjects with no context
- Balance: Intentional negative space that guides the eye, not meaningless emptiness

QUALITY MARKERS:
- Hand-painted texture: visible brushstrokes, paper grain, authentic feel
- Natural imperfections: organic edges, slight color variations, lived-in atmosphere
- Authentic lighting: soft natural light, gentle shadows, realistic color temperature

TECHNICAL SPECS:
- Format: 1080x1440 pixels (3:4 vertical)
- NO TEXT, NO WORDS, NO LETTERS, NO PEOPLE
- Color: Natural, muted tones (avoid neon, bright, or oversaturated colors)
"""

        return prompt.strip()


def main():
    """测试函数"""
    # 创建生成器
    generator = IllustrationGenerator()

    # 测试生成单张图片
    print("🎨 测试生成清新水彩（东方）风格")
    output_path = generator.generate_illustration(
        style_code="watercolor_oriental",
        subject="多肉植物桃蛋",
        details="圆润饱满的叶片，表面有白霜，粉色渐变",
        mood="治愈、温柔"
    )

    if output_path:
        print(f"\n✅ 生成成功: {output_path}")
    else:
        print("\n❌ 生成失败")

    # 测试生成步骤图
    print("\n" + "="*60)
    print("🎨 测试生成彩铅步骤图")
    print("="*60)
    step_paths = generator.generate_pencil_steps(
        subject="蝴蝶兰",
        details="白色花瓣带淡黄色中心，细腻的纹理，优雅的花型"
    )

    if step_paths:
        print(f"\n✅ 步骤图生成成功，共 {len(step_paths)} 张")
        for path in step_paths:
            print(f"  - {path}")
    else:
        print("\n❌ 步骤图生成失败")


if __name__ == "__main__":
    main()
