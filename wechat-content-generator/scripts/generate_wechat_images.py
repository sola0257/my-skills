#!/usr/bin/env python3
"""
微信公众号配图生成器 (修正版)
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

    def generate_article_images(self, content_path, format_type="long_article"):
        """为文章生成全套配图"""
        content_path = Path(content_path)
        output_dir = content_path.parent
        
        tasks = []
        
        # 风格定义
        style = "Soft, bright, fresh spring colors, botanical art photography, macro details, natural light, high quality, 4k"
        
        if format_type == "picture_article": # 图文模式 (竖版)
            # 封面 (3:4)
            tasks.append({
                "name": "cover.png",
                "prompt": f"{style}. A collage or composition of various spring flowers (Tulips, Hyacinth, Winter Jasmine). Colorful, vibrant, and festive. Text space at the top. Aspect ratio 3:4.",
                "desc": "封面图"
            })
            
            # 正文配图 (3:4) - 对应5种植物
            plants = [
                ("01_winter_jasmine.png", "Winter Jasmine (迎春花) branches with bright yellow flowers, simple vase, window light"),
                ("02_tulips.png", "Elegant bouquet of Tulips (郁金香) in a glass vase, pink and white, soft focus background"),
                ("03_hyacinth.png", "Hyacinth (风信子) bulb growing in a glass water vase, blue or purple flowers, showing roots in water"),
                ("04_silver_willow.png", "Red Silver Willow (银柳) branches in a tall vase, Chinese New Year festive vibe"),
                ("05_narcissus.png", "Chinese Narcissus (水仙) carving art, white flowers with yellow centers, elegant ceramic bowl")
            ]
            
            for filename, plant_desc in plants:
                tasks.append({
                    "name": filename,
                    "prompt": f"{style}. {plant_desc}. Close-up, detailed, artistic composition. Aspect ratio 3:4.",
                    "desc": filename
                })
        
        # 执行生成
        print(f"🚀 开始生成配图，共 {len(tasks)} 张...")
        for task in tasks:
            output_path = output_dir / task["name"]
            if output_path.exists():
                print(f"⏩ 跳过已存在: {task['name']}")
                continue
                
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
