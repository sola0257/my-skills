#!/usr/bin/env python3
"""
混合模式配图生成器 (Mixed Mode Image Generator)
专为北京暖气房换盆指南设计
风格：实拍背景 + 手绘涂鸦 (Real photography + Hand-drawn doodles)
"""
import os
import sys
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

class MixedModeImageGenerator:
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

    def generate_tasks(self, output_dir):
        """定义本期文章的配图任务"""
        
        # 混合模式通用 Prompt 后缀
        style_suffix = "Mixed media style: High-quality realistic indoor photography background overlayed with cute white hand-drawn doodles, arrows, and simple text annotations. The doodles should look like they are drawn with a white marker on the photo. Bright, clean, modern aesthetic. NO CHINESE TEXT CHARACTERS (unless specified as doodle style). NO REAL TEXT."
        
        tasks = [
            {
                "name": "cover.png",
                "prompt": f"A 2.35:1 wide banner. Background: A cozy Beijing living room with a window view of winter trees, inside is warm with radiators and lush green Monstera plants. Overlay doodles: A big hand-drawn 'VS' symbol between a shivering outdoor tree and a happy indoor plant. Hand-drawn '?' marks around a plant pot. {style_suffix}",
                "desc": "封面：北京暖气房内外对比"
            },
            {
                "name": "01_判断.png",
                "prompt": f"A 16:9 wide image. Split screen comparison. Left side: A blooming Phalaenopsis orchid (Butterfly Orchid) in a pot. Right side: A Monstera with roots coming out of the bottom pot. Overlay doodles: A big Red Cross 'X' drawn over the Orchid (Don't repot!), and a Green Checkmark 'V' drawn over the Monstera (Repot OK!). {style_suffix}",
                "desc": "判断：能换vs不能换"
            },
            {
                "name": "02_原理.png",
                "prompt": f"A 16:9 wide image. Close up of a plant leaf that looks dry and crispy at the edges. Background shows a radiator heater. Overlay doodles: Cute little blue water drop characters with wings flying AWAY from the leaf, evaporating into the air. Doodles representing 'Heat' waves coming from the radiator. Visualizing VPD (Vapor Pressure Deficit). {style_suffix}",
                "desc": "原理：VPD水分流失"
            },
            {
                "name": "03_操作.png",
                "prompt": f"A 16:9 wide image. A potted plant covered with a clear transparent plastic bag (humidity dome). The bag has some condensation inside. Overlay doodles: Arrows pointing to holes poked in the bag for ventilation. A doodle of a water spray bottle next to it. Text doodle 'ICU' (humorous style) near the plant. {style_suffix}",
                "desc": "操作：套袋保湿大法"
            }
        ]
        
        print(f"🚀 开始生成混合模式配图，共 {len(tasks)} 张...")
        for task in tasks:
            output_path = os.path.join(output_dir, task["name"])
            self.generate_image(task["prompt"], output_path)
            
        print("\n✅ 所有配图生成完成！")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="图片输出目录")
    args = parser.parse_args()
    
    generator = MixedModeImageGenerator()
    generator.generate_tasks(args.output_dir)

if __name__ == "__main__":
    main()
