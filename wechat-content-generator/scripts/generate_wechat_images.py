#!/usr/bin/env python3
"""
微信公众号配图生成器 (动态版 v4.3)
支持根据 Markdown 内容动态提取知识点并生成配图
"""
import os
import sys
import json
import base64
import requests
import re
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def load_env_file(env_path):
    env_vars = {}
    if not os.path.exists(env_path):
        return env_vars
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

class WeChatImageGenerator:
    def __init__(self):
        # 加载配置
        self.api_key = os.getenv("YUNWU_API_KEY")
        if not self.api_key:
            global_env_path = "/Users/dj/Desktop/小静的skills/_global_config/.env"
            env_vars = load_env_file(global_env_path)
            self.api_key = env_vars.get("YUNWU_API_KEY")
        
        self.api_url = "https://yunwu.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_image(self, prompt, output_path):
        """生成单张图片"""
        print(f"🎨 生成图片: {os.path.basename(output_path)}...")
        
        try:
            payload = {
                "model": "gemini-3-pro-image-preview",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code != 200:
                print(f"❌ API 调用失败: {response.status_code}")
                return False
                
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            base64_match = re.search(r"data:image/\w+;base64,([^)]+)", content)
            if not base64_match:
                print("❌ 未找到图片数据")
                return False
                
            image_data = base64.b64decode(base64_match.group(1))
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(image_data)
                
            print(f"✅ 图片已保存")
            return True
            
        except Exception as e:
            print(f"❌ 生成异常: {str(e)}")
            return False

    def parse_markdown(self, content_path):
        """解析 Markdown，提取标题和知识点"""
        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 提取标题 (H1)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Indoor Plants"
        
        # 提取 H3 标题作为知识点 (### 1. 绿萝)
        sections = []
        matches = re.finditer(r'^###\s+(\d+\.|)(.+)$', content, re.MULTILINE)
        for match in matches:
            section_name = match.group(2).strip()
            # 过滤掉非植物的 H3 (如 "推荐尺寸")
            if "推荐" in section_name and "尺寸" in section_name:
                continue
            sections.append(section_name)
            
        return title, sections

    def generate_article_images(self, content_path, format_type="long_article"):
        """为文章生成全套配图"""
        content_path = Path(content_path)
        output_dir = content_path.parent
        
        tasks = []
        
        # 解析内容
        title, sections = self.parse_markdown(content_path)
        print(f"📄 解析文章: {title}")
        print(f"📋 提取知识点: {len(sections)} 个")

        # 通用 Prompt 后缀 (强制约束)
        common_negative = "NO TEXT. NO WORDS. NO LETTERS. NO PINYIN. NO PEOPLE. NO STUDIO LIGHTING."
        common_style = "Modern minimalist interior, stylish contemporary home, 2024 design trends. Soft natural window light, bright and airy, warm golden hour glow. Realistic lifestyle photography, soft focus, film-like quality."
        
        if format_type == "long_article":
            # 1. 封面图 (2.35:1)
            cover_prompt = f"A 2.35:1 wide banner photograph in dreamy realistic style. Subject: Indoor living room full of lush green plants, cozy atmosphere. {common_style} {common_negative}"
            tasks.append({
                "name": "cover.png",
                "prompt": cover_prompt,
                "desc": "封面图"
            })
            
            # 2. 正文配图 (16:9)
            for i, section in enumerate(sections):
                # 提取植物名称 (去除 "1. " 等前缀)
                plant_name = re.sub(r'^\d+\.\s*', '', section).split(' ')[0]
                
                prompt = f"A 16:9 wide photograph in dreamy realistic style. Subject: {plant_name} (indoor plant) in a stylish living room setting. Close-up or medium shot showing healthy leaves. {common_style} {common_negative}"
                
                filename = f"{i+1:02d}_{plant_name}.png"
                # 清理文件名中的特殊字符
                filename = re.sub(r'[^\w\.-]', '_', filename)
                
                tasks.append({
                    "name": filename,
                    "prompt": prompt,
                    "desc": section
                })
                
        elif format_type == "picture_article":
            # 图文模式 (3:4)
            cover_prompt = f"A 3:4 portrait photograph in dreamy realistic style. Subject: Indoor plants collage or beautiful living room corner. {common_style} {common_negative}"
            tasks.append({
                "name": "cover.png",
                "prompt": cover_prompt,
                "desc": "封面图"
            })
            
            for i, section in enumerate(sections):
                plant_name = re.sub(r'^\d+\.\s*', '', section).split(' ')[0]
                prompt = f"A 3:4 portrait photograph in dreamy realistic style. Subject: {plant_name} (indoor plant). {common_style} {common_negative}"
                
                filename = f"{i+1:02d}_{plant_name}.png"
                filename = re.sub(r'[^\w\.-]', '_', filename)
                
                tasks.append({
                    "name": filename,
                    "prompt": prompt,
                    "desc": section
                })
        
        # 执行生成
        print(f"🚀 开始生成配图，共 {len(tasks)} 张...")
        for task in tasks:
            output_path = output_dir / task["name"]
            if output_path.exists():
                print(f"⏩ 跳过已存在: {task['name']}")
                continue
                
            print(f"📸 生成 [{task['desc']}]...")
            self.generate_image(task["prompt"], str(output_path))
            
        print("\n✅ 所有配图生成完成！")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="文章Markdown文件路径")
    parser.add_argument("--format", default="long_article", help="格式：long_article 或 picture_article")
    args = parser.parse_args()
    
    generator = WeChatImageGenerator()
    generator.generate_article_images(args.path, args.format)

if __name__ == "__main__":
    main()
