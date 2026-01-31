#!/usr/bin/env python3
"""
小红书标题和话题标签生成器
为插画系列生成吸引人的标题和话题标签
"""

import os
import json
import requests
from typing import Dict, List, Tuple

class TitleTagGenerator:
    """小红书标题和话题标签生成器"""

    def __init__(self):
        """初始化生成器"""
        self.api_base_url = "https://yunwu.ai/v1"
        self.api_key = os.getenv("YUNWU_API_KEY")

        if not self.api_key:
            raise ValueError("未找到 YUNWU_API_KEY 环境变量")

    def generate_title_and_tags(
        self,
        style_name: str,
        subject: str,
        aesthetic: str
    ) -> Dict[str, any]:
        """
        生成标题和话题标签

        Args:
            style_name: 插画风格名称（如"水彩"）
            subject: 主题（如"多肉植物"）
            aesthetic: 美学风格（"东方" 或 "西方"）

        Returns:
            包含标题和标签的字典
        """
        prompt = self._build_prompt(style_name, subject, aesthetic)

        try:
            response = self._call_api(prompt)
            result = self._parse_response(response)
            return result
        except Exception as e:
            print(f"生成失败: {e}")
            return self._get_fallback_result(style_name, subject)

    def _build_prompt(self, style_name: str, subject: str, aesthetic: str) -> str:
        """构建生成提示词"""
        return f"""请为一组{aesthetic}风格的{style_name}插画生成小红书标题和话题标签。

主题：{subject}
风格：{style_name}（{aesthetic}美学）

要求：

1. **标题**（1个）：
   - 长度：严格控制在20个字符以内（包括标点符号）
   - 风格：诗意、有意境、能引发情感共鸣
   - 避免：过度营销化、夸张、使用感叹号
   - 示例风格："春日里的多肉时光" "水彩下的绿意生活" "一株植物的四季诗"

2. **话题标签**（10个）：
   - 3-4个大流量标签（用于进入流量池）：
     * 如：#植物 #插画 #水彩 #手绘
   - 6-7个长尾标签（用于精准搜索）：
     * 如：#多肉养护日记 #水彩植物插画 #东方美学插画

   标签要求：
   - 每个标签前加 # 号
   - 标签之间用空格分隔
   - 结合风格、主题、美学特点
   - 避免过于宽泛或过于冷门

请以JSON格式返回：
{{
  "title": "标题文本",
  "tags": ["#标签1", "#标签2", ...],
  "tag_strategy": {{
    "broad_tags": ["#大流量标签1", ...],
    "longtail_tags": ["#长尾标签1", ...]
  }}
}}

只返回JSON，不要其他说明文字。"""

    def _call_api(self, prompt: str) -> str:
        """调用API生成内容"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gemini-3-pro-preview",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.8,  # 提高创意性
            "max_tokens": 500
        }

        response = requests.post(
            f"{self.api_base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        return result["choices"][0]["message"]["content"]

    def _parse_response(self, response: str) -> Dict[str, any]:
        """解析API响应"""
        # 提取JSON内容
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()

        try:
            data = json.loads(response)

            # 验证标题长度
            title = data.get("title", "")
            if len(title) > 20:
                print(f"警告：标题超过20字符（{len(title)}字符），将截断")
                title = title[:20]

            # 验证标签数量
            tags = data.get("tags", [])
            if len(tags) > 10:
                print(f"警告：标签超过10个（{len(tags)}个），将截断")
                tags = tags[:10]

            return {
                "title": title,
                "tags": tags,
                "tag_strategy": data.get("tag_strategy", {
                    "broad_tags": tags[:4],
                    "longtail_tags": tags[4:]
                })
            }
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            print(f"原始响应: {response}")
            raise

    def _get_fallback_result(self, style_name: str, subject: str) -> Dict[str, any]:
        """获取备用结果（API失败时使用）"""
        return {
            "title": f"{style_name}下的{subject}",
            "tags": [
                "#插画", "#手绘", f"#{style_name}",
                f"#{subject}", "#艺术", "#绘画",
                f"#{style_name}插画", f"#{subject}插画",
                "#植物插画", "#治愈系插画"
            ],
            "tag_strategy": {
                "broad_tags": ["#插画", "#手绘", f"#{style_name}", f"#{subject}"],
                "longtail_tags": [
                    "#艺术", "#绘画",
                    f"#{style_name}插画", f"#{subject}插画",
                    "#植物插画", "#治愈系插画"
                ]
            }
        }

    def save_to_file(self, result: Dict[str, any], output_path: str):
        """保存结果到文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n标题和标签已保存到: {output_path}")
        print(f"\n标题: {result['title']}")
        print(f"标签: {' '.join(result['tags'])}")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="生成小红书标题和话题标签")
    parser.add_argument("--style", required=True, help="插画风格名称")
    parser.add_argument("--subject", required=True, help="主题")
    parser.add_argument("--aesthetic", required=True, choices=["东方", "西方"], help="美学风格")
    parser.add_argument("--output", required=True, help="输出文件路径")

    args = parser.parse_args()

    generator = TitleTagGenerator()
    result = generator.generate_title_and_tags(
        style_name=args.style,
        subject=args.subject,
        aesthetic=args.aesthetic
    )

    generator.save_to_file(result, args.output)


if __name__ == "__main__":
    main()
