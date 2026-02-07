"""
Skill caller module for integrating Claude Code skills
Calls xiaohongshu-content-generator skill via subprocess

Output Format Contract (v1):
{
    "title": str,        # Required: Content title
    "content": str,      # Required: Main content text
    "images": list       # Required: List of image URLs/paths or objects with {url, prompt}
}
"""

import subprocess
import json
import os
import re
from typing import Dict, Any, List


# Expected output format version
SKILL_OUTPUT_VERSION = 'v1'

# Required fields for v1 format
REQUIRED_FIELDS_V1 = ['title', 'content', 'images']


def validate_skill_output(data: Dict[str, Any], version: str = 'v1') -> None:
    """
    Validate skill output format

    Args:
        data: The parsed skill output data
        version: Expected format version

    Raises:
        ValueError: If output format is invalid
    """
    if version == 'v1':
        # Check required fields
        missing_fields = [field for field in REQUIRED_FIELDS_V1 if field not in data]
        if missing_fields:
            raise ValueError(
                f"Skill output missing required fields: {', '.join(missing_fields)}. "
                f"Expected format: {REQUIRED_FIELDS_V1}"
            )

        # Validate field types
        if not isinstance(data['title'], str):
            raise ValueError(f"Field 'title' must be string, got {type(data['title']).__name__}")

        if not isinstance(data['content'], str):
            raise ValueError(f"Field 'content' must be string, got {type(data['content']).__name__}")

        if not isinstance(data['images'], list):
            raise ValueError(f"Field 'images' must be list, got {type(data['images']).__name__}")
    else:
        raise ValueError(f"Unsupported skill output version: {version}")


def call_xiaohongshu_skill(topic: str, version: str = 'v1') -> Dict[str, Any]:
    """
    Call xiaohongshu-content-generator skill to generate content

    Args:
        topic: The topic to generate content for
        version: Expected output format version (default: 'v1')

    Returns:
        dict: Generated content with title, content, and image prompts
              Format depends on version parameter

    Raises:
        Exception: If skill execution fails
        ValueError: If output format validation fails

    NOTE: Current implementation returns mock data for UI testing.

    ARCHITECTURAL ISSUE:
    xiaohongshu-content-generator is a Claude Code skill designed to run within
    Claude Code sessions, not as a standalone CLI tool. The original approach of
    calling it via subprocess with '--skill' flag doesn't work because:
    1. Claude Code CLI doesn't support '--skill' flag for external invocation
    2. Skills are internal to Claude Code sessions and use the Skill tool

    FUTURE INTEGRATION OPTIONS:
    1. Extract skill logic into a standalone Python library
    2. Use Claude API to invoke the skill programmatically
    3. Create a dedicated content generation service
    4. Use the skill's scripts/ directory if it has callable modules
    """
    try:
        # TODO: Replace with real skill integration
        # For now, return mock content to enable UI workflow testing

        content_data = {
            'title': f'🌿 {topic}养护全攻略',
            'content': f'''# {topic}的日常养护指南

## 🌱 基础养护要点

关于{topic}的养护，最重要的是掌握以下几个核心要素：

**1. 光照需求**
{topic}喜欢明亮的散射光，避免强烈的直射阳光。建议放在室内光线充足但不会被太阳直晒的位置。

**2. 浇水频率**
遵循"见干见湿"的原则，等土壤表面干燥后再浇水。夏季可以适当增加浇水频率，冬季则要减少。

**3. 温度控制**
最适宜的生长温度在18-25℃之间，冬季要注意保暖，避免低于10℃。

## 💡 常见问题解决

**叶子发黄怎么办？**
可能是浇水过多或光照不足导致的，及时调整养护方式。

**生长缓慢？**
检查是否需要换盆或补充肥料，春秋季是最佳生长期。

## ✨ 养护小技巧

- 定期清洁叶片，保持光合作用效率
- 每月施一次稀释的液体肥
- 注意通风，预防病虫害

记住，养护{topic}最重要的是耐心和细心观察，每株植物都有自己的"脾气"，慢慢摸索出最适合它的养护方式吧！

#植物养护 #绿植日记 #{topic}''',
            'images': [
                {'prompt': f'{topic}整体形态展示，自然光线，生活化场景', 'url': ''},
                {'prompt': f'{topic}叶片特写，展示健康状态', 'url': ''},
                {'prompt': f'{topic}养护工具摆放，温馨家居氛围', 'url': ''},
                {'prompt': f'{topic}浇水场景，手部动作特写', 'url': ''},
                {'prompt': f'{topic}生长环境，窗台或桌面布置', 'url': ''}
            ]
        }

        # Validate output format
        try:
            validate_skill_output(content_data, version)
        except ValueError as e:
            raise ValueError(
                f"Skill output format validation failed: {e}\n"
                f"This usually means the skill's output format has changed.\n"
                f"Please check the skill output or update the platform code."
            )

        return content_data

    except ValueError:
        # Re-raise validation errors as-is
        raise
    except Exception as e:
        raise Exception(f"Error calling skill: {e}")
