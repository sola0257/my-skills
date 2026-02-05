
import os
import sys
from generate_wechat_images import WeChatImageGenerator

def regenerate_modern_images():
    generator = WeChatImageGenerator()
    output_dir = "/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/订阅号/2026-02-04_立春仪式感/"
    
    # 共同风格：现代、明亮、简约、高级
    base_style = "Modern minimalist interior, stylish contemporary home, 2024 design trends, bright and airy, soft natural light, high quality, 4k, photorealistic"
    
    tasks = [
        {
            "name": "cover.png",
            "prompt": f"{base_style}. A beautiful horizontal banner for 'Li Chun'. Close-up of fresh green buds in a modern glass vase on a white table. Clean background, negative space on the right. Elegant and fresh. Aspect ratio 2.35:1."
        },
        {
            "name": "02_chasing_light.png",
            "prompt": f"{base_style}. Modern living room corner with floor-to-ceiling windows. Stylish indoor plants (Fiddle Leaf Fig, Monstera) in modern ceramic or cement pots basking in the sun. White sheer curtains, light wood floor. No clutter, no vintage furniture. Aspect ratio 16:9."
        },
        {
            "name": "03_spring_tea.png",
            "prompt": f"{base_style}. A modern coffee table scene. A clear glass cup of tea, a plate with spring pancakes (modern plating), and a vase of tulips. Background is a blurry modern sofa or bright living room. Lifestyle aesthetic. Aspect ratio 16:9."
        }
    ]
    
    for task in tasks:
        output_path = os.path.join(output_dir, task["name"])
        if os.path.exists(output_path):
            os.remove(output_path)
        print(f"🔄 Regenerating {task['name']}...")
        generator.generate_image(task["prompt"], output_path)

if __name__ == "__main__":
    regenerate_modern_images()
