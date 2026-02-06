#!/usr/bin/env python3
"""
精准配图生成器 (Accurate Image Generator)
严格遵循 wechat-image-prompt-guide.md 规范
针对文章：《北京花友请留步！暖气房换盆的"生死时速"》
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

class AccurateImageGenerator:
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
        """定义精准配图任务"""
        
        # 风格定义 (参考 wechat-image-prompt-guide.md)
        
        # 1. Dreamy-Photo (场景/植物)
        style_photo = "A 16:9 wide photograph in dreamy realistic style. Modern minimalist interior, stylish contemporary home, 2024 design trends. Soft natural window light, bright and airy. Realistic lifestyle photography, soft focus, film-like quality. NO TEXT. NO WORDS."
        
        # 2. Infographic-Sketch (知识/原理)
        style_info = "A 16:9 wide infographic in hand-drawn sketchnote style. Clean white background or lined notebook paper texture. Clear visual hierarchy. Functional colors (sage green, soft red). Educational aesthetic. CRITICAL: Use ONLY Chinese characters for text if needed, or NO text. "
        
        # 3. Cozy-Sketch (教程/步骤)
        style_sketch = "A 16:9 wide illustration in hand-drawn sketch style. Pencil line drawings with soft watercolor washes. Cozy sketchbook aesthetic. Clear steps."

        # 4. Banner (封面)
        style_banner = "A 2.35:1 wide banner photograph in dreamy realistic style. Modern interior."

        tasks = [
            # 封面：场景类 -> Dreamy Photo
            {
                "name": "cover.png",
                "prompt": f"{style_banner} Subject: A warm Beijing winter living room scene. Sunlight streaming through sheer curtains, illuminating a healthy Monstera (龟背竹) and Pothos (绿萝) by the window. Cozy, vibrant green against a winter backdrop. NO TEXT.",
                "desc": "封面：北京暖气房绿植场景"
            },
            
            # 插图1：判断标准 (知识类) -> Infographic Sketch
            {
                "name": "01__.png", # 对应文案中的占位符
                "prompt": f"{style_info} Subject: Comparison chart. Left side: A blooming Phalaenopsis Orchid (蝴蝶兰) with a Red 'X' mark (Don't repot). Right side: A potted Monstera with roots growing out of the bottom with a Green Checkmark (Repot OK). Hand-drawn style.",
                "desc": "判断：能换vs不能换 (知识图解)"
            },
            
            # 插图2：VPD原理 (原理类) -> Infographic Sketch
            {
                "name": "02__.png",
                "prompt": f"{style_info} Subject: Diagram illustrating 'Physiological Drought'. A plant leaf losing water (blue droplets evaporating) faster than roots can absorb it. Background shows a radiator (heater) emitting heat waves. Visualizing dry air. Educational diagram.",
                "desc": "原理：VPD水分流失 (知识图解)"
            },
            
            # 插图3：套袋操作 (操作类) -> Dreamy Photo (实操更有说服力)
            {
                "name": "03___.png",
                "prompt": f"{style_photo} Subject: Close-up of a potted plant covered with a clear transparent plastic bag (humidity dome) to retain moisture. The bag has tiny holes for ventilation. Placed on a wooden table near a window with soft light. Realistic instruction.",
                "desc": "操作：套袋保湿 (实拍风格)"
            },
            
            # 植物展示：植物类 -> Dreamy Photo (必须准确)
            {
                "name": "04_场景A_春节买的年宵花_杜鹃_栀子_红掌_.png",
                "prompt": f"{style_photo} Subject: A beautiful potted Azalea (杜鹃花) or Gardenia (栀子花) in a modern ceramic pot. Showing healthy green leaves and some flowers. Indoor setting.",
                "desc": "植物：年宵花 (杜鹃/栀子)"
            },
            
            {
                "name": "05_场景B_僵苗一冬天的观叶植物_龟背竹_绿萝_.png",
                "prompt": f"{style_photo} Subject: A lush green Pothos (绿萝) trailing down from a shelf, and a Monstera (龟背竹) in the background. Healthy, vibrant green leaves. Modern living room context.",
                "desc": "植物：观叶植物 (绿萝/龟背竹)"
            }
        ]
        
        print(f"🚀 开始生成精准配图，共 {len(tasks)} 张...")
        for task in tasks:
            output_path = os.path.join(output_dir, task["name"])
            # 先删除旧图，确保重新生成
            if os.path.exists(output_path):
                os.remove(output_path)
                
            self.generate_image(task["prompt"], output_path)
            
        print("\n✅ 所有配图生成完成！")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="图片输出目录")
    args = parser.parse_args()
    
    generator = AccurateImageGenerator()
    generator.generate_tasks(args.output_dir)

if __name__ == "__main__":
    main()
