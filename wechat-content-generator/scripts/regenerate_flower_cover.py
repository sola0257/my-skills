
import os
import sys
from generate_wechat_images import WeChatImageGenerator

def regenerate_cover():
    generator = WeChatImageGenerator()
    
    output_path = "/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/订阅号/2026-02-04_立春赏花图鉴/cover.png"
    
    # New prompt based on user feedback (no empty top, better hierarchy, more aesthetic)
    prompt = "Soft, warm, natural light, healing atmosphere, photorealistic, lifestyle photography, high quality, 4k. A stunning close-up composition of spring flowers (Tulips, Hyacinth, Winter Jasmine). Rich layers, depth of field. No large empty white spaces. Magazine cover quality. A feeling of abundance and spring awakening. Aspect ratio 3:4."
    
    if os.path.exists(output_path):
        os.remove(output_path)
        
    generator.generate_image(prompt, output_path)

if __name__ == "__main__":
    regenerate_cover()
