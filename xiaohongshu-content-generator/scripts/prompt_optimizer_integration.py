#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt Optimizer Integration Module (Plan 3: Dual-Guarantee Mechanism)

工作流程：
User Input → Prompt Template Optimization → Add Rule Checklists → AI Generation → Quality Check

版本: v1.0.0
创建日期: 2026-02-05
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PromptOptimizerIntegration:
    """
    提示词优化整合器

    整合三层内容：
    1. Prompt Template（结构层）- 提供标准化的提示词结构
    2. Rule Checklists（约束层）- 平台规范和执行规则
    3. User Examples（价值层）- 用户的个性化案例和经验
    """

    def __init__(self, skill_path: str = None):
        """
        初始化整合器

        Args:
            skill_path: xiaohongshu-content-generator skill 的路径
        """
        if skill_path is None:
            skill_path = "/Users/dj/Desktop/小静的skills/xiaohongshu-content-generator"

        self.skill_path = Path(skill_path)
        self.global_config_path = Path("/Users/dj/Desktop/小静的skills/_global_config")

        # 模板路径
        self.text_template_path = self.global_config_path / "prompt-templates/text-optimize/system-prompt-general.md"
        self.image_template_path = self.global_config_path / "prompt-templates/image-optimize/image-prompt-general.md"

        # 检查清单路径
        self.step0_checklist_path = self.skill_path / "knowledge/step0-init-checklist.md"
        self.step5_checklist_path = self.skill_path / "knowledge/step5-content-checklist.md"
        self.step9_checklist_path = self.skill_path / "knowledge/step9-image-checklist.md"

        # 缓存
        self._text_template = None
        self._image_template = None
        self._checklists = {}

    def _load_template(self, template_path: Path) -> str:
        """
        加载模板文件并提取模板内容

        Args:
            template_path: 模板文件路径

        Returns:
            提取的模板内容（去掉说明部分）
        """
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取代码块中的模板内容
        match = re.search(r'```\n(.*?)\n```', content, re.DOTALL)
        if match:
            return match.group(1)
        else:
            raise ValueError(f"无法从 {template_path} 中提取模板内容")

    def _load_checklist(self, checklist_path: Path) -> str:
        """
        加载检查清单文件

        Args:
            checklist_path: 检查清单文件路径

        Returns:
            检查清单内容
        """
        with open(checklist_path, 'r', encoding='utf-8') as f:
            return f.read()

    def get_text_template(self) -> str:
        """获取文本优化模板"""
        if self._text_template is None:
            self._text_template = self._load_template(self.text_template_path)
        return self._text_template

    def get_image_template(self) -> str:
        """获取图像优化模板"""
        if self._image_template is None:
            self._image_template = self._load_template(self.image_template_path)
        return self._image_template

    def get_checklist(self, step: str) -> str:
        """
        获取指定步骤的检查清单

        Args:
            step: 步骤名称 ('step0', 'step5', 'step9')

        Returns:
            检查清单内容
        """
        if step not in self._checklists:
            if step == 'step0':
                path = self.step0_checklist_path
            elif step == 'step5':
                path = self.step5_checklist_path
            elif step == 'step9':
                path = self.step9_checklist_path
            else:
                raise ValueError(f"未知的步骤: {step}")

            self._checklists[step] = self._load_checklist(path)

        return self._checklists[step]

    def optimize_content_prompt(
        self,
        original_prompt: str,
        include_checklists: List[str] = None
    ) -> str:
        """
        优化内容生成提示词（Plan 3: 双重保障机制）

        工作流程：
        1. 使用文本优化模板优化原始提示词（结构层）
        2. 添加相关的规则检查清单（约束层）
        3. 保留用户的个性化案例和规范（价值层）

        Args:
            original_prompt: 原始提示词
            include_checklists: 需要包含的检查清单列表，如 ['step0', 'step5']

        Returns:
            优化后的完整提示词
        """
        # Step 1: 使用模板优化（结构层）
        text_template = self.get_text_template()
        optimized_prompt = text_template.replace("[在这里插入原始提示词]", original_prompt)

        # Step 2: 添加规则检查清单（约束层）
        if include_checklists:
            checklist_section = "\n\n## 执行规则与检查清单\n\n"
            checklist_section += "**重要**: 以下规则和检查清单必须严格遵守，这些是基于平台规范和历史经验总结的约束条件。\n\n"

            for step in include_checklists:
                checklist_content = self.get_checklist(step)
                checklist_section += f"### {step.upper()} 检查清单\n\n"
                checklist_section += checklist_content + "\n\n"

            optimized_prompt += checklist_section

        # Step 3: 添加个性化说明（价值层）
        personalization_note = """
## 个性化要求

**保留用户的个性化内容**：
- 平台规范和限制（如字数限制、格式要求）
- 正面案例参考（成功的内容示例）
- 反面案例警示（需要避免的错误）
- 用户的独特风格和调性

这些个性化内容体现了用户的经验积累和独特价值，必须在生成内容时充分考虑。
"""
        optimized_prompt += personalization_note

        return optimized_prompt

    def optimize_image_prompt(
        self,
        original_description: str,
        include_image_checklist: bool = True
    ) -> str:
        """
        优化图像生成提示词（Plan 3: 双重保障机制）

        工作流程：
        1. 使用图像优化模板优化原始描述（结构层）
        2. 添加图像生成检查清单（约束层）
        3. 保留用户的个性化案例和规范（价值层）

        Args:
            original_description: 原始图像描述
            include_image_checklist: 是否包含 step9 图像检查清单

        Returns:
            优化后的完整图像提示词
        """
        # Step 1: 使用模板优化（结构层）
        image_template = self.get_image_template()
        optimized_prompt = image_template.replace("[在这里插入原始图像描述]", original_description)

        # Step 2: 添加图像检查清单（约束层）
        if include_image_checklist:
            checklist_content = self.get_checklist('step9')
            checklist_section = "\n\n## 图像生成规则与检查清单\n\n"
            checklist_section += "**重要**: 以下规则和检查清单必须严格遵守，这些是基于小红书平台规范和成功案例总结的约束条件。\n\n"
            checklist_section += checklist_content + "\n\n"

            optimized_prompt += checklist_section

        # Step 3: 添加个性化说明（价值层）
        personalization_note = """
## 个性化要求

**保留用户的个性化内容**：
- 小红书平台的图像规范（尺寸、数量、命名）
- 正面案例参考（成功的配图示例）
- 反面案例警示（需要避免的错误效果）
- 用户的独特审美和风格偏好

这些个性化内容体现了用户对小红书平台的深入理解和独特审美，必须在生成图像时充分考虑。
"""
        optimized_prompt += personalization_note

        return optimized_prompt

    def get_full_workflow_prompt(
        self,
        task_description: str,
        task_type: str = "content"
    ) -> str:
        """
        获取完整的工作流提示词（适用于 Skill 调用）

        Args:
            task_description: 任务描述
            task_type: 任务类型 ('content' 或 'image')

        Returns:
            完整的工作流提示词
        """
        if task_type == "content":
            # 内容生成任务：包含 step0, step5 检查清单
            return self.optimize_content_prompt(
                task_description,
                include_checklists=['step0', 'step5']
            )
        elif task_type == "image":
            # 图像生成任务：包含 step9 检查清单
            return self.optimize_image_prompt(
                task_description,
                include_image_checklist=True
            )
        else:
            raise ValueError(f"未知的任务类型: {task_type}")


# 便捷函数
def optimize_xiaohongshu_content_prompt(original_prompt: str) -> str:
    """
    优化小红书内容生成提示词的便捷函数

    Args:
        original_prompt: 原始提示词

    Returns:
        优化后的提示词
    """
    optimizer = PromptOptimizerIntegration()
    return optimizer.optimize_content_prompt(
        original_prompt,
        include_checklists=['step0', 'step5']
    )


def optimize_xiaohongshu_image_prompt(original_description: str) -> str:
    """
    优化小红书图像生成提示词的便捷函数

    Args:
        original_description: 原始图像描述

    Returns:
        优化后的提示词
    """
    optimizer = PromptOptimizerIntegration()
    return optimizer.optimize_image_prompt(
        original_description,
        include_image_checklist=True
    )


if __name__ == "__main__":
    # 测试代码
    optimizer = PromptOptimizerIntegration()

    # 测试内容优化
    print("=" * 80)
    print("测试内容提示词优化")
    print("=" * 80)
    content_prompt = "生成一篇关于多肉植物养护的小红书笔记"
    optimized_content = optimizer.optimize_content_prompt(
        content_prompt,
        include_checklists=['step0', 'step5']
    )
    print(optimized_content[:500] + "...\n")

    # 测试图像优化
    print("=" * 80)
    print("测试图像提示词优化")
    print("=" * 80)
    image_description = "一盆多肉植物放在窗台上"
    optimized_image = optimizer.optimize_image_prompt(
        image_description,
        include_image_checklist=True
    )
    print(optimized_image[:500] + "...")
