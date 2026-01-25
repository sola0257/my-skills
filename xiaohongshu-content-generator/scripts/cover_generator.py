import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

class CoverGenerator:
    def __init__(self):
        # 字体路径配置 (优先使用苹方，回退到华文黑体)
        self.font_path_bold = "/System/Library/Fonts/STHeiti Medium.ttc"
        self.font_path_light = "/System/Library/Fonts/STHeiti Light.ttc"
        
        # 品牌色配置 (慢养四季 - 绿色系/大地色系)
        self.brand_colors = {
            "primary": "#2E5C38",  # 深绿
            "secondary": "#E8F5E9", # 浅绿背景
            "accent": "#C05621",    # 强调色(橙红)
            "text_dark": "#1A202C", # 深灰
            "text_light": "#FFFFFF" # 白
        }

    def _load_font(self, size, is_bold=True):
        """加载字体"""
        path = self.font_path_bold if is_bold else self.font_path_light
        try:
            return ImageFont.truetype(path, size)
        except:
            # 回退到默认
            return ImageFont.load_default()

    def _wrap_text(self, text, font, max_width, draw):
        """自动换行"""
        lines = []
        words = list(text) # 中文按字分割
        current_line = []
        
        for word in words:
            current_line.append(word)
            width = draw.textlength("".join(current_line), font=font)
            if width > max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append("".join(current_line))
                    current_line = [word]
                else:
                    lines.append("".join(current_line))
                    current_line = []
        
        if current_line:
            lines.append("".join(current_line))
        return lines

    def _add_text_with_shadow(self, draw, xy, text, font, text_color, shadow_color="#000000", shadow_offset=(2, 2)):
        """添加带阴影的文字"""
        x, y = xy
        # 绘制阴影
        draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow_color)
        # 绘制主体
        draw.text((x, y), text, font=font, fill=text_color)

    def generate(self, base_image_path, title, subtitle, output_path, layout_type="auto"):
        """
        生成封面主函数
        :param base_image_path: 底图路径
        :param title: 主标题
        :param subtitle: 副标题
        :param output_path: 输出路径
        :param layout_type: 排版类型 (auto, split, magazine, center, minimalist)
        """
        # 加载底图
        try:
            img = Image.open(base_image_path).convert("RGBA")
        except Exception as e:
            print(f"Error loading image: {e}")
            return False

        # 统一尺寸 (小红书 3:4 -> 1080x1440)
        target_size = (1080, 1440)
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # 创建绘制层
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # 自动选择排版
        if layout_type == "auto":
            layout_type = random.choice(["split", "magazine", "center", "minimalist"])
        
        print(f"Applying layout: {layout_type}")

        if layout_type == "split":
            self._layout_split(img, overlay, draw, title, subtitle)
        elif layout_type == "magazine":
            self._layout_magazine(img, overlay, draw, title, subtitle)
        elif layout_type == "center":
            self._layout_center(img, overlay, draw, title, subtitle)
        else:
            self._layout_minimalist(img, overlay, draw, title, subtitle)

        # 合成最终图片
        final_img = Image.alpha_composite(img, overlay)
        final_img = final_img.convert("RGB")
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        final_img.save(output_path, quality=95)
        return True

    # --- 排版逻辑实现 ---

    def _layout_split(self, img, overlay, draw, title, subtitle):
        """左右对分排版 (适合对比/干货)"""
        w, h = img.size
        
        # 创建半透明遮罩 (左侧或底部)
        # 这里做底部遮罩，更稳妥
        mask_h = int(h * 0.35)
        draw.rectangle([(0, h - mask_h), (w, h)], fill=(255, 255, 255, 240))
        
        # 绘制主标题
        title_font_size = 100
        title_font = self._load_font(title_font_size, is_bold=True)
        # 简单的自动缩放
        while draw.textlength(title, font=title_font) > w * 0.85:
            title_font_size -= 5
            title_font = self._load_font(title_font_size, is_bold=True)
            
        draw.text((w*0.08, h - mask_h + 50), title, font=title_font, fill=self.brand_colors["text_dark"])
        
        # 绘制副标题
        sub_font = self._load_font(50, is_bold=False)
        lines = self._wrap_text(subtitle, sub_font, w * 0.85, draw)
        
        y_offset = h - mask_h + 50 + title_font_size + 30
        for line in lines:
            draw.text((w*0.08, y_offset), line, font=sub_font, fill="#555555")
            y_offset += 60

    def _layout_magazine(self, img, overlay, draw, title, subtitle):
        """杂志风排版 (大标题在顶部)"""
        w, h = img.size
        
        # 顶部渐变遮罩
        # 暂用纯色半透明代替渐变
        draw.rectangle([(0, 0), (w, int(h * 0.25))], fill=(0, 0, 0, 100))
        
        # 竖排文字逻辑 (模拟) - 这里先用横排大字
        title_font_size = 120
        title_font = self._load_font(title_font_size, is_bold=True)
        
        # 文字居中
        text_w = draw.textlength(title, font=title_font)
        x_pos = (w - text_w) / 2
        
        self._add_text_with_shadow(draw, (x_pos, 100), title, title_font, 
                                 self.brand_colors["text_light"], shadow_color="#000000")
        
        # 副标题在底部
        sub_font = self._load_font(60, is_bold=True)
        sub_w = draw.textlength(subtitle, font=sub_font)
        draw.rectangle([(w/2 - sub_w/2 - 20, h - 200), (w/2 + sub_w/2 + 20, h - 120)], fill=self.brand_colors["accent"])
        draw.text(((w - sub_w) / 2, h - 190), subtitle, font=sub_font, fill="white")

    def _layout_center(self, img, overlay, draw, title, subtitle):
        """中心聚焦 (几何窗口)"""
        w, h = img.size
        
        # 中心矩形框
        box_w, box_h = int(w * 0.8), int(h * 0.3)
        box_x, box_y = (w - box_w) // 2, (h - box_h) // 2
        
        draw.rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], 
                      fill=(255, 255, 255, 230), outline=self.brand_colors["primary"], width=5)
        
        # 标题
        title_font = self._load_font(90, is_bold=True)
        lines = self._wrap_text(title, title_font, box_w * 0.9, draw)
        
        # 计算总高度以垂直居中
        total_text_h = len(lines) * 100 + 80 # 80是副标题估算
        current_y = box_y + (box_h - total_text_h) / 2
        
        for line in lines:
            lw = draw.textlength(line, font=title_font)
            draw.text((box_x + (box_w - lw)/2, current_y), line, font=title_font, fill=self.brand_colors["text_dark"])
            current_y += 100
            
        # 副标题
        current_y += 20
        sub_font = self._load_font(45, is_bold=False)
        lw = draw.textlength(subtitle, font=sub_font)
        draw.text((box_x + (box_w - lw)/2, current_y), subtitle, font=sub_font, fill=self.brand_colors["primary"])

    def _layout_minimalist(self, img, overlay, draw, title, subtitle):
        """极简留白 (文字小而精)"""
        w, h = img.size
        
        # 简单的装饰线条
        draw.line([(50, 50), (w-50, 50)], fill="white", width=3)
        draw.line([(50, 50), (50, h-50)], fill="white", width=3)
        draw.line([(w-50, 50), (w-50, h-50)], fill="white", width=3)
        draw.line([(50, h-50), (w-50, h-50)], fill="white", width=3)
        
        # 标题放在图片上方 1/3 处
        title_font = self._load_font(110, is_bold=True)
        self._add_text_with_shadow(draw, (80, 200), title, title_font, "white")
        
        # 副标题
        sub_font = self._load_font(50, is_bold=False)
        draw.rectangle([(80, 330), (80 + 10 + draw.textlength(subtitle, sub_font), 390)], fill="black")
        draw.text((85, 335), subtitle, font=sub_font, fill="white")

if __name__ == "__main__":
    # 测试代码
    generator = CoverGenerator()
    test_img = "/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/小红书/test_cover_base.png"
    # 创建一个测试底图
    if not os.path.exists(test_img):
        img = Image.new('RGB', (1024, 1024), color = 'gray')
        os.makedirs(os.path.dirname(test_img), exist_ok=True)
        img.save(test_img)
        
    generator.generate(test_img, "救命！琴叶榕掉叶子", "3个动作教你起死回生", 
                      "/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/小红书/test_cover_output.png", 
                      layout_type="auto")
