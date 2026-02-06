#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt Optimizer Integration - 自动化测试套件

运行方式：
    python3 test_prompt_optimizer_integration.py
"""

import sys
import os
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from prompt_optimizer_integration import (
    PromptOptimizerIntegration,
    optimize_xiaohongshu_content_prompt,
    optimize_xiaohongshu_image_prompt
)


class TestPromptOptimizerIntegration:
    """测试套件"""

    def __init__(self):
        self.optimizer = PromptOptimizerIntegration()
        self.passed = 0
        self.failed = 0
        self.errors = []

    def assert_true(self, condition, message):
        """断言为真"""
        if condition:
            self.passed += 1
            print(f"  ✅ {message}")
        else:
            self.failed += 1
            self.errors.append(message)
            print(f"  ❌ {message}")

    def assert_contains(self, text, substring, message):
        """断言包含子字符串"""
        self.assert_true(substring in text, message)

    def test_load_templates(self):
        """测试加载模板"""
        print("\n📋 测试1: 加载模板")

        # 测试加载文本模板
        text_template = self.optimizer.get_text_template()
        self.assert_contains(text_template, "Role:", "文本模板包含 Role 字段")
        self.assert_contains(text_template, "Profile", "文本模板包含 Profile 字段")
        self.assert_contains(text_template, "Skills", "文本模板包含 Skills 字段")

        # 测试加载图像模板
        image_template = self.optimizer.get_image_template()
        self.assert_contains(image_template, "原始描述", "图像模板包含原始描述字段")
        self.assert_contains(image_template, "优化后的提示词", "图像模板包含优化提示")

    def test_load_checklists(self):
        """测试加载检查清单"""
        print("\n📋 测试2: 加载检查清单")

        # 测试加载 step0
        step0 = self.optimizer.get_checklist('step0')
        self.assert_contains(step0, "粉丝数", "step0 包含粉丝数相关内容")

        # 测试加载 step5
        step5 = self.optimizer.get_checklist('step5')
        self.assert_contains(step5, "标题", "step5 包含标题相关内容")

        # 测试加载 step9
        step9 = self.optimizer.get_checklist('step9')
        self.assert_contains(step9, "配图", "step9 包含配图相关内容")

    def test_optimize_content_prompt(self):
        """测试优化内容提示词"""
        print("\n📋 测试3: 优化内容提示词")

        original = "生成一篇关于多肉植物养护的小红书笔记"
        optimized = self.optimizer.optimize_content_prompt(
            original,
            include_checklists=['step0', 'step5']
        )

        # 检查是否包含三层内容
        self.assert_contains(optimized, "Role:", "包含结构层（模板）")
        self.assert_contains(optimized, "执行规则与检查清单", "包含约束层（检查清单）")
        self.assert_contains(optimized, "个性化要求", "包含价值层（个性化）")

        # 检查是否包含原始提示词
        self.assert_contains(optimized, original, "包含原始提示词")

    def test_optimize_image_prompt(self):
        """测试优化图像提示词"""
        print("\n📋 测试4: 优化图像提示词")

        original = "一盆多肉植物放在窗台上"
        optimized = self.optimizer.optimize_image_prompt(
            original,
            include_image_checklist=True
        )

        # 检查是否包含三层内容
        self.assert_contains(optimized, "原始描述", "包含结构层（模板）")
        self.assert_contains(optimized, "图像生成规则与检查清单", "包含约束层（检查清单）")
        self.assert_contains(optimized, "个性化要求", "包含价值层（个性化）")

        # 检查是否包含原始描述
        self.assert_contains(optimized, original, "包含原始描述")

    def test_convenience_functions(self):
        """测试便捷函数"""
        print("\n📋 测试5: 便捷函数")

        # 测试内容优化便捷函数
        content_result = optimize_xiaohongshu_content_prompt(
            "测试内容"
        )
        self.assert_true(len(content_result) > 0, "内容优化便捷函数返回非空结果")

        # 测试图像优化便捷函数
        image_result = optimize_xiaohongshu_image_prompt(
            "测试图像"
        )
        self.assert_true(len(image_result) > 0, "图像优化便捷函数返回非空结果")

    def test_backward_compatibility(self):
        """测试向后兼容性"""
        print("\n📋 测试6: 向后兼容性")

        # 测试不包含检查清单的情况
        optimized = self.optimizer.optimize_content_prompt(
            "测试",
            include_checklists=None
        )
        self.assert_true(len(optimized) > 0, "不包含检查清单时仍能正常工作")

        # 测试不包含图像检查清单的情况
        optimized = self.optimizer.optimize_image_prompt(
            "测试",
            include_image_checklist=False
        )
        self.assert_true(len(optimized) > 0, "不包含图像检查清单时仍能正常工作")

    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("🧪 Prompt Optimizer Integration - 自动化测试")
        print("=" * 80)

        self.test_load_templates()
        self.test_load_checklists()
        self.test_optimize_content_prompt()
        self.test_optimize_image_prompt()
        self.test_convenience_functions()
        self.test_backward_compatibility()

        print("\n" + "=" * 80)
        print("📊 测试结果")
        print("=" * 80)
        print(f"✅ 通过: {self.passed}")
        print(f"❌ 失败: {self.failed}")

        if self.failed > 0:
            print("\n失败的测试:")
            for error in self.errors:
                print(f"  - {error}")
            return False
        else:
            print("\n🎉 所有测试通过！")
            return True


if __name__ == "__main__":
    tester = TestPromptOptimizerIntegration()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
