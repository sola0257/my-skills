#!/usr/bin/env python3
"""
案例库自动管理脚本
自动添加正面/反面案例，更新索引文档
"""
import os
import json
from datetime import datetime
from pathlib import Path

class CaseManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.cases_dir = self.base_dir / "knowledge" / "cases"
        self.positive_dir = self.cases_dir / "positive"
        self.negative_dir = self.cases_dir / "negative"
        self.index_file = self.cases_dir / "INDEX.md"

    def get_next_case_number(self, case_type="positive"):
        """获取下一个案例编号"""
        target_dir = self.positive_dir if case_type == "positive" else self.negative_dir

        existing_cases = list(target_dir.glob("case-*.md"))
        if not existing_cases:
            return 1

        # 提取编号
        numbers = []
        for case_file in existing_cases:
            try:
                num = int(case_file.stem.split("-")[1])
                numbers.append(num)
            except:
                continue

        return max(numbers) + 1 if numbers else 1

    def add_positive_case(self, image_path, style_code, style_name, subject,
                         prompt, rating=5, notes=""):
        """
        自动添加正面案例

        Args:
            image_path: 生成的图片路径
            style_code: 风格代码
            style_name: 风格名称
            subject: 植物名称
            prompt: 完整 Prompt
            rating: 评分（1-5）
            notes: 备注
        """
        case_num = self.get_next_case_number("positive")
        case_id = f"{case_num:03d}"

        # 生成案例文件名
        filename = f"case-{case_id}-{style_code}-{subject}.md"
        case_file = self.positive_dir / filename

        # 复制图片到案例目录
        case_image = self.base_dir / ".tmp" / f"case-{case_id}.png"
        if Path(image_path).exists():
            import shutil
            shutil.copy(image_path, case_image)

        # 生成案例内容
        stars = "⭐" * rating
        today = datetime.now().strftime("%Y-%m-%d")

        content = f"""# 案例 {case_id}：{style_name} - {subject}

## 基本信息

- **案例编号**：{case_id}
- **风格**：{style_name}
- **风格代码**：{style_code}
- **植物**：{subject}
- **生成日期**：{today}
- **评分**：{stars}
- **标签**：excellent, reference

## 效果展示

![生成效果](../../../.tmp/case-{case_id}.png)

**视觉描述**：
{notes if notes else "（待补充）"}

## 成功要素

### 1. Prompt 关键点

**完整 Prompt**：
```
{prompt}
```

### 2. 视觉效果分析

**优点**：
- ✅ 视觉效果优秀
- ✅ 完全符合风格特征
- ✅ 可作为参考标准

## 经验总结

1. 此案例展示了{style_name}的典型特征
2. Prompt 结构合理，关键词使用准确
3. 可作为后续生成的参考标准

---

**创建时间**：{today}
**最后更新**：{today}
**自动生成**：由 case_manager.py 自动创建
"""

        # 写入案例文件
        with open(case_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # 更新索引
        self._update_index_positive(case_id, filename, style_name, subject, rating, today)

        print(f"✅ 正面案例已添加: {filename}")
        return case_file

    def add_negative_case(self, image_path, style_code, style_name, subject,
                         prompt, problem_type, problem_desc):
        """
        自动添加反面案例

        Args:
            image_path: 问题图片路径
            style_code: 风格代码
            style_name: 风格名称
            subject: 植物名称
            prompt: 导致问题的 Prompt
            problem_type: 问题类型
            problem_desc: 问题描述
        """
        case_num = self.get_next_case_number("negative")
        case_id = f"{case_num:03d}"

        # 生成案例文件名
        filename = f"case-{case_id}-{problem_type}.md"
        case_file = self.negative_dir / filename

        # 复制图片
        case_image = self.base_dir / ".tmp" / f"negative-case-{case_id}.png"
        if Path(image_path).exists():
            import shutil
            shutil.copy(image_path, case_image)

        # 生成案例内容
        today = datetime.now().strftime("%Y-%m-%d")

        content = f"""# 反面案例 {case_id}：{problem_desc}

## 基本信息

- **案例编号**：{case_id}
- **问题类型**：{problem_type}
- **风格**：{style_name}
- **植物**：{subject}
- **生成日期**：{today}
- **标签**：{problem_type}

## 问题展示

![问题效果](../../../.tmp/negative-case-{case_id}.png)

**问题描述**：
{problem_desc}

## 问题分析

### 1. 主要问题

- ❌ 生成效果不符合预期
- ❌ 需要避免重复此类问题

### 2. Prompt 问题

**导致问题的 Prompt**：
```
{prompt}
```

**问题分析**：
（待补充具体分析）

## 避免方法

### 检查清单

- [ ] 检查 Prompt 是否包含问题词汇
- [ ] 验证风格特征是否明确
- [ ] 确认参数设置是否正确

---

**创建时间**：{today}
**最后更新**：{today}
**自动生成**：由 case_manager.py 自动创建
"""

        # 写入案例文件
        with open(case_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # 更新索引
        self._update_index_negative(case_id, filename, problem_desc, today)

        print(f"✅ 反面案例已添加: {filename}")
        return case_file

    def _update_index_positive(self, case_id, filename, style_name, subject, rating, date):
        """更新索引文档（正面案例）"""
        # 读取现有索引
        with open(self.index_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 生成案例链接
        stars = "⭐" * rating
        case_link = f"- [案例 {case_id}：{subject}](./positive/{filename}) {stars}\n"
        case_link += f"  - 简介：{style_name}风格的优秀案例\n"
        case_link += f"  - 日期：{date}\n\n"

        # 找到对应风格的位置并插入
        style_header = f"### {style_name}"
        if style_header in content:
            # 在风格标题后插入
            parts = content.split(style_header)
            # 找到下一个空行
            lines = parts[1].split('\n')
            insert_pos = 2  # 跳过标题行和空行
            lines.insert(insert_pos, case_link)
            parts[1] = '\n'.join(lines)
            content = style_header.join(parts)

        # 更新统计
        content = self._update_statistics(content, "positive")

        # 写回文件
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(content)

    def _update_index_negative(self, case_id, filename, problem_desc, date):
        """更新索引文档（反面案例）"""
        # 读取现有索引
        with open(self.index_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 生成案例链接
        case_link = f"- [反面案例 {case_id}：{problem_desc}](./negative/{filename})\n"
        case_link += f"  - 日期：{date}\n\n"

        # 在"常见问题"部分插入
        problem_header = "### 常见问题"
        if problem_header in content:
            parts = content.split(problem_header)
            lines = parts[1].split('\n')
            insert_pos = 2
            lines.insert(insert_pos, case_link)
            parts[1] = '\n'.join(lines)
            content = problem_header.join(parts)

        # 更新统计
        content = self._update_statistics(content, "negative")

        # 写回文件
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(content)

    def _update_statistics(self, content, case_type):
        """更新案例统计"""
        # 统计案例数量
        positive_count = len(list(self.positive_dir.glob("case-*.md")))
        negative_count = len(list(self.negative_dir.glob("case-*.md")))
        total_count = positive_count + negative_count
        today = datetime.now().strftime("%Y-%m-%d")

        # 更新统计表格
        stats_lines = [
            "| 类型 | 数量 | 最后更新 |",
            "|------|------|---------|",
            f"| ✅ 正面案例 | {positive_count} | {today} |",
            f"| ❌ 反面案例 | {negative_count} | {today} |",
            f"| **总计** | **{total_count}** | {today} |"
        ]

        # 替换统计部分
        lines = content.split('\n')
        start_idx = None
        end_idx = None

        for i, line in enumerate(lines):
            if '| 类型 | 数量 | 最后更新 |' in line:
                start_idx = i
            if start_idx and line.startswith('---') and i > start_idx + 2:
                end_idx = i + 1
                break

        if start_idx and end_idx:
            lines[start_idx:end_idx] = stats_lines
            content = '\n'.join(lines)

        return content


def main():
    """命令行接口"""
    import sys

    manager = CaseManager()

    if len(sys.argv) < 2:
        print("用法: python case_manager.py [add-positive|add-negative]")
        return

    command = sys.argv[1]

    if command == "add-positive":
        # 示例：添加正面案例
        manager.add_positive_case(
            image_path=".tmp/test.png",
            style_code="watercolor_oriental",
            style_name="清新水彩（东方）",
            subject="测试植物",
            prompt="测试 Prompt",
            rating=5,
            notes="这是一个测试案例"
        )
    elif command == "add-negative":
        # 示例：添加反面案例
        manager.add_negative_case(
            image_path=".tmp/test.png",
            style_code="watercolor_oriental",
            style_name="清新水彩（东方）",
            subject="测试植物",
            prompt="测试 Prompt",
            problem_type="color-issue",
            problem_desc="色彩过饱和"
        )
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
