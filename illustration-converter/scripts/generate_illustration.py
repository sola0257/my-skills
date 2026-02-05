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

    def generate_series(self, style_code, subject, details="", mood="", output_dir=None, reference_image_path=None, element_description=None, skip_existing=False):
        """
        生成4张系列插画（标准模式：局部、中景、整体全景、意境氛围）

        Args:
            style_code: 风格代码
            subject: 植物名称
            details: 细节描述
            mood: 情绪关键词
            output_dir: 输出目录
            reference_image_path: 参考图片路径（可选）
            element_description: 意境图元素描述（可选，仅用于第4张意境图）
            skip_existing: 是否跳过已存在的文件（默认为 False）

        Returns:
            list: 输出文件路径列表
        """
        # 4张系列图标准结构（v2.0 - 通用优化版）
        # 针对不同风格的特殊强化
        is_pencil = "pencil" in style_code
        is_watercolor = "watercolor" in style_code
        is_ink = "ink" in style_code
        is_oil = "oil" in style_code
        is_gouache = "gouache" in style_code

        # 根据画风选择技法术语
        if is_pencil:
            technique_term = "drawn"
            medium_specific = "COLORED PENCIL SPECIFIC: Show VISIBLE PENCIL STROKES. Paper texture must be evident. Hand-drawn quality with slight natural imperfections. Layered pencil marks creating rich color. This is NOT a photo - it's hand-drawn colored pencil art. CRITICAL: This is the artwork itself filling the entire frame, NOT a photograph of a drawing on paper. No paper edges, no background behind the artwork, no meta-composition."
        elif is_watercolor:
            technique_term = "painted"
            medium_specific = "WATERCOLOR SPECIFIC: Show transparent washes, soft edges, water blooms, and natural color bleeding. Visible brushstrokes and paper texture. This is watercolor painting, not digital art. CRITICAL: This is the artwork itself filling the entire frame, NOT a photograph of a painting. No paper edges, no background behind the artwork."
        elif is_ink:
            technique_term = "painted"
            medium_specific = "INK PAINTING SPECIFIC: Show ink gradations (墨分五色), expressive brushstrokes, and natural ink flow. This is traditional ink painting, not digital art. CRITICAL: This is the artwork itself filling the entire frame, NOT a photograph of a painting. No paper edges, no background behind the artwork."
        elif is_oil:
            technique_term = "painted"
            medium_specific = "OIL PAINTING SPECIFIC: Show visible brushstrokes, impasto texture where appropriate, and rich color layering. This is oil painting, not digital art. CRITICAL: This is the artwork itself filling the entire frame, NOT a photograph of a painting. No canvas edges, no background behind the artwork."
        elif is_gouache:
            technique_term = "painted"
            medium_specific = "GOUACHE SPECIFIC: Show opaque flat colors, clean edges, and matte finish. This is gouache painting, not digital art. CRITICAL: This is the artwork itself filling the entire frame, NOT a photograph of a painting. No paper edges, no background behind the artwork."
        else:
            technique_term = "painted/drawn"
            medium_specific = ""

        compositions = [
            {
                "name": "局部特写",
                "description": "Close-up Detail",
                "prompt_addition": f"""EXTREME CLOSE-UP DETAIL - MACRO VIEW:
- Show ONLY 2-3 individual flowers at extreme close range
- Fill the ENTIRE frame with flower details - petals, stamens, texture
- NO pot visible, NO stems below, NO leaves at bottom
- This is a MACRO botanical study focusing on flower structure
- Think: "looking through a magnifying glass at the flowers"
- The flowers should be so close they fill the frame edge to edge

CRITICAL: This is NOT a mid-range view. This is an extreme close-up where you can see petal veins and texture details.

{medium_specific if medium_specific else "Show intricate details like veins, surface patterns, color gradations."}"""
            },
            {
                "name": "中景视角",
                "description": "Mid-range View",
                "prompt_addition": f"""MID-RANGE VIEW - SHOW THE PLANT GROWING FROM POT:

CRITICAL REQUIREMENT - PLANT CONTINUITY:
- Show the COMPLETE plant growing naturally from the pot
- You must see: flowers at top → stems in middle → leaves → pot (upper half)
- This is ONE continuous plant, not separate elements
- The plant EMERGES from the pot and grows upward naturally

WHAT TO INCLUDE:
- All the flowers and flower spikes (upper portion)
- The stems and leaves connecting everything (middle portion)
- The upper half of the pot showing where the plant grows from (lower portion)
- The pot bottom and base are cropped out (not shown)

COMPOSITION:
- This is closer than "full scene" (which shows complete pot + base)
- This is farther than "extreme close-up" (which shows only 2-3 flowers)
- This shows most of the plant but crops out the pot bottom

Think: "Show the plant growing from its pot, but crop out the pot bottom and base"

BACKGROUND: Clean, simple, neutral

{medium_specific if medium_specific else ""}"""
            },
            {
                "name": "整体全景",
                "description": "Full Scene",
                "prompt_addition": f"""FULL SCENE - COMPLETE BOTANICAL DOCUMENTATION:
- Show 100% of the plant from top to bottom
- Show 100% of the pot from rim to base
- Include the surface the pot sits on (table, ground, etc.)
- This is the "specimen documentation" view - complete and comprehensive
- Think: "botanical reference photo" showing the entire subject

COMPOSITION STRATEGY: Step back to show everything - this is the widest view of the four images.

CRITICAL DIFFERENCE from Mid-range:
- Mid-range is closer, focusing on flowers, pot barely visible
- Full Scene is farther back, showing complete plant-pot-surface unit

{medium_specific if medium_specific else ""}"""
            },
            {
                "name": "意境氛围",
                "description": "Atmospheric Mood",
                "prompt_addition": f"""ATMOSPHERIC MOOD - ARTISTIC INTERPRETATION:

BOTANICAL ACCURACY (MOST IMPORTANT - APPLIES TO ALL STYLES):
- The plant MUST maintain its exact characteristics from the reference photo
- Flower shape, color, and structure must match the reference (e.g., if snapdragons, they must look like snapdragons)
- Do NOT change the plant species or significantly alter its appearance
- The artistic interpretation is in the ENVIRONMENT, not in changing the plant itself

COMPOSITION:
Place the plant-pot unit within an imagined beautiful garden setting, but the plant itself remains botanically accurate to the reference.

IMPORTANT: This is NOT a foreground+background composition.
The entire scene - plant, pot, and environment - should be {technique_term} together as ONE unified artwork with harmonious integration.

The plant-pot unit is thoughtfully placed within a gentle garden atmosphere. The environment and plant are {technique_term} together, creating a cohesive whole. Soft transitions between elements, no harsh separation.

Environment (integrated, not layered):
- Soft garden atmosphere with muted, harmonious colors
- Complementary elements: garden stones, soft moss, gentle foliage in background
- Environment elements {technique_term} with the same technique as the plant
- Everything flows together - plant, pot, ground, atmosphere - as one artwork
- Colors: muted earth tones, soft greens, gentle grays, cream

Natural Logic (CRITICAL):
- Plant MUST grow naturally from the pot
- Plant and pot remain connected, no separation
- Maintain botanical accuracy - the plant species and characteristics must match the reference photo
- Only the environment is imagined, the plant itself is accurate

{medium_specific if medium_specific else ""}"""
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
            
            # 特殊处理：如果是意境图（第4张）且有元素描述，将其添加到 Prompt 中
            if comp['name'] == "意境氛围" and element_description:
                comp['prompt_addition'] += f"\n\nADDITIONAL ELEMENT:\n{element_description}"
                
            full_prompt = f"{base_prompt}\n\nComposition: {comp['prompt_addition']}"

            # 输出路径 - 使用中文友好的文件名
            # 格式：序号_构图类型_主题简介.png
            filename = f"{i:02d}_{comp['name']}_{subject}.png"
            output_path = output_dir / filename

            # 检查是否跳过
            if skip_existing and output_path.exists():
                print(f"⏩ 跳过已存在的文件: {filename}")
                output_paths.append(str(output_path))
                continue

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
        # 定义各风格的步骤（基于专业学术标准 - professional-painting-steps.md）
        style_steps = {
            "watercolor_oriental": [
                {"step": 1, "title": "铅笔稿", "stage": "Pencil Sketch",
                 "details": "Light pencil outline on watercolor paper, capturing basic composition. Lines should be gentle, not too heavy, leaving space for watercolor."},
                {"step": 2, "title": "第一遍淡彩", "stage": "First Light Wash",
                 "details": "Light transparent wash establishing overall color zones and atmosphere. Use wet-on-wet technique with plenty of water."},
                {"step": 3, "title": "第二遍中间色", "stage": "Second Layer - Mid Tones",
                 "details": "Building depth with medium tones on dry base, wet-on-dry technique for control. Colors deeper than first layer but still transparent."},
                {"step": 4, "title": "第三遍深色与细节", "stage": "Third Layer - Darks and Details",
                 "details": "Adding darkest values and fine details with controlled brushwork. Maintain breathing space and Eastern aesthetic."},
                {"step": 5, "title": "完成与调整", "stage": "Final Touches",
                 "details": f"Final adjustments, highlights, and overall refinement. {details if details else 'Completed watercolor with soft edges and poetic atmosphere.'}"}
            ],
            "watercolor_western": [
                {"step": 1, "title": "精细铅笔稿", "stage": "Detailed Pencil Drawing",
                 "details": "Precise pencil drawing with botanical accuracy and clear contours. Include all structural details."},
                {"step": 2, "title": "底色铺设", "stage": "Base Wash",
                 "details": "First color layer establishing light and shadow with controlled washes. Wet-on-dry technique for precision."},
                {"step": 3, "title": "色彩叠加", "stage": "Color Building",
                 "details": "Multiple layers building rich, saturated colors with precision. Botanical illustration tradition."},
                {"step": 4, "title": "细节刻画", "stage": "Fine Details",
                 "details": "Botanical precision - veins, textures, highlights with fine brushwork. Scientific accuracy meets artistic beauty."},
                {"step": 5, "title": "完成", "stage": "Finished Piece",
                 "details": f"Final refinement with vibrant colors and complete details. {details if details else 'Completed botanical watercolor.'}"}
            ],
            "ink_oriental": [
                {"step": 1, "title": "白描", "stage": "Line Drawing - Baimiao",
                 "details": "Ink outline with flowing lines, traditional Chinese line work. Use center-tip brush technique."},
                {"step": 2, "title": "分染", "stage": "Color Separation - Fenran",
                 "details": "Separating color zones with light washes, establishing base tones. Layer by layer approach."},
                {"step": 3, "title": "罩染", "stage": "Glazing - Zhaoyan",
                 "details": "Overall glazing to unify colors and create harmony. Thin and even application."},
                {"step": 4, "title": "提染", "stage": "Highlighting - Tiyan",
                 "details": "Highlighting key areas to enhance dimensionality. Strategic emphasis on focal points."},
                {"step": 5, "title": "完成", "stage": "Final Artwork",
                 "details": f"Final details and optional seal stamp in traditional style. {details if details else 'Completed gongbi painting.'}"}
            ],
            "pencil_oriental": [
                {"step": 1, "title": "线稿", "stage": "Line Drawing",
                 "details": "Light pencil outline with gentle strokes. Lines should be soft, not too heavy."},
                {"step": 2, "title": "铺底色", "stage": "Base Color Layer",
                 "details": "First light color layer with gentle pressure. Even application establishing color zones."},
                {"step": 3, "title": "深化色彩", "stage": "Color Deepening",
                 "details": "Building color intensity through multiple layers. Gradual deepening with soft transitions."},
                {"step": 4, "title": "细节刻画", "stage": "Detail Refinement",
                 "details": "Adding fine details, textures, and subtle color variations. Meticulous attention to transitions."},
                {"step": 5, "title": "完成", "stage": "Final Artwork",
                 "details": f"Final refinement with soft, delicate finish. {details if details else 'Completed with gentle, contemplative mood.'}"}
            ],
            "pencil_western": [
                {"step": 1, "title": "精细线稿", "stage": "Detailed Line Work",
                 "details": "Precise pencil drawing with botanical accuracy. Structural precision and complete details."},
                {"step": 2, "title": "铺底色", "stage": "Base Colors",
                 "details": "Even color application establishing local colors. Foundation for realistic rendering."},
                {"step": 3, "title": "深化明暗", "stage": "Building Values",
                 "details": "Layering for depth, shadows, and dimensional form. Strong contrast for three-dimensionality."},
                {"step": 4, "title": "细节刻画", "stage": "Fine Details",
                 "details": "Intricate textures, highlights, botanical precision. Photorealistic quality and texture expression."},
                {"step": 5, "title": "完成", "stage": "Finished Illustration",
                 "details": f"Photorealistic finish with rich details. {details if details else 'Completed botanical illustration.'}"}
            ],
            "oil_oriental": [
                {"step": 1, "title": "底稿", "stage": "Underpainting",
                 "details": "Monochrome underpainting establishing values and composition. Thin application building structure."},
                {"step": 2, "title": "底色", "stage": "Base Colors",
                 "details": "Thin color layer establishing color harmony with soft tones. Transparent and gentle."},
                {"step": 3, "title": "中间色", "stage": "Middle Tones",
                 "details": "Medium-thick paint building form with gentle brushwork. Restrained strokes, soft colors."},
                {"step": 4, "title": "高光与细节", "stage": "Highlights and Details",
                 "details": "Impasto highlights and subtle details with atmospheric depth. Moderate impasto maintaining Eastern charm."},
                {"step": 5, "title": "完成", "stage": "Final Painting",
                 "details": f"Final refinement with poetic mood and soft edges. {details if details else 'Completed with contemplative atmosphere.'}"}
            ],
            "oil_western": [
                {"step": 1, "title": "底稿", "stage": "Detailed Underpainting",
                 "details": "Precise tonal study establishing light and shadow. Strong contrast in values."},
                {"step": 2, "title": "底色", "stage": "Color Blocking",
                 "details": "Bold color application establishing composition. Rich colors with visible brushwork."},
                {"step": 3, "title": "中间色", "stage": "Form Building",
                 "details": "Thick paint application with dramatic brushstrokes. Heavy texture and expressive strokes."},
                {"step": 4, "title": "高光", "stage": "Highlights and Texture",
                 "details": "Impasto highlights, rich textures, dramatic lighting. Classical oil painting technique."},
                {"step": 5, "title": "完成", "stage": "Finished Oil Painting",
                 "details": f"Classical finish with rich textures and depth. {details if details else 'Completed in Dutch Golden Age style.'}"}
            ],
            "gouache_oriental": [
                {"step": 1, "title": "线稿", "stage": "Line Drawing",
                 "details": "Clean outlines with decorative pattern planning. Flowing lines with pattern sensibility."},
                {"step": 2, "title": "平涂底色", "stage": "Flat Base Colors",
                 "details": "Even opaque color application with clean edges. Establishing color blocks."},
                {"step": 3, "title": "叠加色彩", "stage": "Color Layering",
                 "details": "Adding secondary colors and pattern elements. Clear layers with decorative quality."},
                {"step": 4, "title": "装饰细节", "stage": "Decorative Details",
                 "details": "Traditional patterns, ornamental elements, possible gold accents. Folk art style."},
                {"step": 5, "title": "完成", "stage": "Final Artwork",
                 "details": f"Folk art charm with decorative finish. {details if details else 'Completed with pattern and ornamental quality.'}"}
            ],
            "gouache_western": [
                {"step": 1, "title": "线稿", "stage": "Clean Line Work",
                 "details": "Precise outlines with modern design planning. Strong design sensibility and clean lines."},
                {"step": 2, "title": "平涂底色", "stage": "Flat Color Blocks",
                 "details": "Bold even color application with graphic quality. Opaque with sharp edges."},
                {"step": 3, "title": "叠加色彩", "stage": "Color Additions",
                 "details": "Secondary colors creating visual interest. Design-forward with color contrast."},
                {"step": 4, "title": "装饰细节", "stage": "Design Details",
                 "details": "Modern patterns, geometric elements, clean edges. Mid-century modern style."},
                {"step": 5, "title": "完成", "stage": "Final Illustration",
                 "details": f"Graphic design appeal with modern illustration style. {details if details else 'Completed with contemporary aesthetic.'}"}
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

        # 保存原始参考图路径
        original_reference = reference_image_path
        current_reference = reference_image_path

        for step_info in steps:
            print(f"\n{'='*60}")
            print(f"📝 步骤 {step_info['step']}: {step_info['title']}")
            print(f"{'='*60}")

            # 构建步骤 Prompt
            base_prompt = self._build_prompt(style_code, subject, details, mood)

            # 步骤1需要特别强调：精确复制参考图的构图
            if step_info['step'] == 1:
                # 获取画风的英文名称（用于 prompt）
                style_type_map = {
                    "watercolor_oriental": "watercolor",
                    "watercolor_western": "watercolor",
                    "ink_oriental": "Chinese ink painting",
                    "ink_western": "ink painting",
                    "pencil_oriental": "colored pencil",
                    "pencil_western": "colored pencil",
                    "oil_oriental": "oil painting",
                    "oil_western": "oil painting",
                    "gouache_oriental": "gouache",
                    "gouache_western": "gouache",
                }
                style_type = style_type_map.get(style_code, "painting")

                # 获取步骤1的具体要求（根据画种不同）
                step1_requirements_map = {
                    "watercolor_oriental": "ONLY light pencil lines - NO color, NO shading, NO wash",
                    "watercolor_western": "ONLY light pencil lines - NO color, NO shading, NO wash",
                    "ink_oriental": "ONLY light ink outlines - NO heavy ink, NO shading, NO color",
                    "ink_western": "ONLY light ink outlines - NO heavy ink, NO shading, NO color",
                    "pencil_oriental": "ONLY light line drawing - NO color, NO shading, NO blending",
                    "pencil_western": "ONLY light line drawing - NO color, NO shading, NO blending",
                    "oil_oriental": "ONLY charcoal or pencil sketch - NO paint, NO color, NO shading",
                    "oil_western": "ONLY charcoal or pencil sketch - NO paint, NO color, NO shading",
                    "gouache_oriental": "ONLY light line work - NO paint, NO color, NO shading",
                    "gouache_western": "ONLY light line work - NO paint, NO color, NO shading",
                }
                step1_requirement = step1_requirements_map.get(style_code, "ONLY basic outlines - NO color, NO shading, NO rendering")

                step_prompt = f"""CRITICAL: This is a step-by-step {style_type} tutorial based on the reference photo.

ARTISTIC APPROACH:
You are an artist creating a {style_type} artwork inspired by the reference photo:
- Study the main subject ({subject}) carefully
- Capture the essence and key features of the subject
- Simplify or redesign the background to better showcase the subject
- Adjust composition for artistic effect while keeping the subject recognizable
- This is artistic interpretation, not photographic reproduction

REFERENCE PHOTO GUIDANCE:
- Main subject: {subject} - capture its form, structure, and character
- Background: Simplify or redesign as needed - you don't need to copy every detail
- Composition: Adjust to create a more artistic, balanced composition
- Focus: Emphasize what makes the subject beautiful and interesting

{base_prompt}

STEP {step_info['step']}/5: {step_info['stage']}
Stage description: {step_info['details']}

CRITICAL REQUIREMENTS FOR THIS STEP:
This is ONLY the first stage - {step_info['title']}:
- {step1_requirement}
- Just outlines and basic structure
- Very light, delicate lines
- Capture the main forms and composition
- This is preparatory work for the painting/coloring that will come in later steps

WHAT TO INCLUDE:
- {subject} (main subject)
- Simplified background elements if needed for composition
- Basic spatial relationships

WHAT TO AVOID:
- NO color or paint of any kind
- NO shading or tonal work
- NO detailed rendering
- This is just the foundation sketch/outline

Text overlay: Add Chinese text "步骤{step_info['step']}：{step_info['title']}" in upper left corner, clear handwritten style, soft cream color.
"""
            # 步骤5（完成）需要特殊处理：基于步骤4，但要求达到完成图的效果
            elif step_info['step'] == 5:
                # 获取画风的英文名称
                style_type_map = {
                    "watercolor_oriental": "watercolor",
                    "watercolor_western": "watercolor",
                    "ink_oriental": "Chinese ink painting",
                    "ink_western": "ink painting",
                    "pencil_oriental": "colored pencil",
                    "pencil_western": "colored pencil",
                    "oil_oriental": "oil painting",
                    "oil_western": "oil painting",
                    "gouache_oriental": "gouache",
                    "gouache_western": "gouache",
                }
                style_type = style_type_map.get(style_code, "artwork")

                step_prompt = f"""{base_prompt}

STEP {step_info['step']}/5: {step_info['stage']} - FINAL ARTWORK
Stage description: {step_info['details']}

CRITICAL INSTRUCTIONS FOR FINAL STEP:
This is the natural completion of Step 4. Build upon what's already there:
- Keep the same composition and subject structure from the reference (Step 4)
- Add final refinements: brighten highlights, deepen shadows, enhance color saturation
- Bring colors to FULL vibrancy - this is the finished artwork, not a study
- Add final details: subtle texture, color accents, finishing touches
- The result should feel like a polished, completed {style_type} with rich, saturated colors
- Override "muted tones" - allow vibrant, lively colors appropriate for a finished piece

Think of this as: "Take Step 4 and bring it to 100% completion with full color intensity"
Text overlay: Add Chinese text "步骤{step_info['step']}：{step_info['title']}" in upper left corner, clear handwritten style, soft cream color.
"""
            else:
                step_prompt = f"""{base_prompt}

STEP {step_info['step']}/5: {step_info['stage']}
Stage description: {step_info['details']}
Show this specific stage of the drawing process, not the final result.
IMPORTANT: Maintain the EXACT same composition and subject structure as the reference. Only add the painting elements for THIS step.
Text overlay: Add Chinese text "步骤{step_info['step']}：{step_info['title']}" in upper left corner, clear handwritten style, soft cream color.
"""

            # 输出路径
            filename = f"步骤{step_info['step']}_{step_info['title']}.png"
            output_path = output_dir / filename

            # 生成图片（所有步骤都使用当前参考图，保持连贯性）
            success = self.generate_single_image(step_prompt, str(output_path), reference_image_path=current_reference)

            if success:
                output_paths.append(str(output_path))
                # 将当前步骤的输出作为下一步的参考图
                current_reference = str(output_path)
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
        # 艺术家风格参考映射（基于专业学术标准 - professional-painting-steps.md v2.0）
        artist_references = {
            "watercolor_oriental": {
                "artist": "Qi Baishi (齐白石)",
                "style_keywords": "Chinese freehand brushwork, expressive simplicity, poetic composition",
                "composition": "Subject occupies 40-50% of frame with intentional negative space for visual breathing room",
                "technique": "Light to dark progression (从淡到深). Wet-on-wet washes for soft bleeding, transparent layering building depth gradually, visible brushstrokes with breathing space. Multiple transparent washes, each layer drying before next application."
            },
            "watercolor_western": {
                "artist": "John Singer Sargent",
                "style_keywords": "gestural brushwork, delicate layering, luminous washes, confident strokes",
                "composition": "Subject occupies 60-70% of frame, dynamic composition with strong light-shadow contrast",
                "technique": "Light to dark progression. Wet-on-dry for controlled edges, multiple transparent layers building rich saturated colors, botanical precision with fine brushwork. Layered washes creating luminosity and depth."
            },
            "ink_oriental": {
                "artist": "Bada Shanren (八大山人) for Xieyi, Song Dynasty masters for Gongbi",
                "style_keywords": "Gongbi: meticulous line work, layered染色. Xieyi: minimalist ink, expressive freedom, Zen aesthetics",
                "composition": "Gongbi: 60-70% of frame. Xieyi: 30-40% of frame with extreme minimalism and meaningful negative space",
                "technique": "Gongbi: Baimiao outline (白描), Fenran separation (分染 from edges inward), Zhaoyan glazing (罩染 transparent overall wash), Tiyan highlighting (提染). Xieyi: Ink gradations (墨分五色), expressive brushstrokes, color as accent not dominance, spontaneous yet controlled."
            },
            "pencil_oriental": {
                "artist": "Japanese botanical illustration tradition",
                "style_keywords": "botanical illustration, delicate shading, soft transitions, gentle aesthetic",
                "composition": "Subject occupies 70-80% of frame, specimen-style with complete details",
                "technique": "Light to dark layering (从浅到深). Gentle pressure for base layers, gradual color building through multiple layers, soft blending for smooth transitions. Avoid heavy burnishing, maintain delicate Japanese aesthetic with soft finish."
            },
            "pencil_western": {
                "artist": "Ann Swan, Janie Gildow (professional botanical colored pencil artists)",
                "style_keywords": "HAND-DRAWN colored pencil art, visible pencil strokes, paper texture, layered technique, botanical accuracy with artistic soul",
                "composition": "Subject occupies 70-80% of frame, botanical specimen style with complete details",
                "technique": "CRITICAL - This must look like REAL COLORED PENCIL ART, not a photo filter. Light to dark layering (从浅到深). Multiple layers building from lightest colors, gradual pressure increase, burnishing technique for smooth areas while maintaining visible pencil texture. VISIBLE PENCIL STROKES throughout, paper tooth texture showing, hand-drawn quality with natural variations. Cross-hatching for texture, layered color application, authentic colored pencil marks. This is hand-drawn art, not digital manipulation."
            },
            "oil_oriental": {
                "artist": "Classical oil painting with Eastern aesthetic",
                "style_keywords": "poetic atmosphere, soft edges, subtle mood, restrained elegance",
                "composition": "Subject occupies 70-80% of frame, classical arrangement with atmospheric depth",
                "technique": "Dark to light progression (从暗到明). Monochrome underpainting establishing values, transparent glazing layers preserving underpainting, feathering edges for soft transitions. Each glaze layer must dry completely. Final transparent glaze unifying tones with poetic atmosphere."
            },
            "oil_western": {
                "artist": "Dutch Golden Age masters (Rembrandt, Vermeer)",
                "style_keywords": "dramatic lighting, rich textures, classical realism, chiaroscuro",
                "composition": "Subject occupies 70-80% of frame, classical still life with dramatic lighting",
                "technique": "Dark to light progression (从暗到明). Dark underpainting with strong value contrast, multiple transparent glazing layers, feathering edges to prevent harsh lines. Semi-opaque form building, thick impasto highlights creating texture. Final transparent glaze for depth and unity."
            },
            "gouache_oriental": {
                "artist": "Chinese folk art and Japanese Meiji aesthetics",
                "style_keywords": "decorative patterns, flat colors, ornamental design, folk art charm",
                "composition": "Subject occupies 60-70% of frame, pattern-based layout",
                "technique": "Wet-on-wet blending for soft backgrounds, opaque flat color application with clean edges (covering underlayers completely), thin glazing for depth, decorative details. High pigment concentration allowing opaque coverage."
            },
            "gouache_western": {
                "artist": "Mid-century modern illustration",
                "style_keywords": "graphic design appeal, bold colors, clean edges, modern aesthetic",
                "composition": "Subject occupies 60-70% of frame, modern graphic layout",
                "technique": "Wet-on-wet blending for atmospheric backgrounds, opaque color blocks with sharp edges (complete coverage of underlayers), scumbling with dry brush for broken texture allowing underlayer to show through. Combination of opaque and transparent techniques."
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
