#!/usr/bin/env python3
"""
商品图片批量处理脚本
功能：使用Rembg抠图 + 合成莫兰迪风格背景

使用前需安装依赖：
pip install rembg Pillow

用法：
python image_processor.py --input ./images --output ./processed --background ./backgrounds/bg_morandi_green.png
"""

import os
import sys
import argparse
from pathlib import Path
from io import BytesIO

try:
    from rembg import remove
    from PIL import Image
except ImportError:
    print("请先安装依赖：pip install rembg Pillow")
    sys.exit(1)


def remove_background(input_path: str) -> Image.Image:
    """
    使用Rembg移除图片背景
    
    参数:
        input_path: 输入图片路径
    
    返回:
        透明背景的PIL Image对象
    """
    with open(input_path, 'rb') as f:
        input_data = f.read()
    
    output_data = remove(input_data)
    return Image.open(BytesIO(output_data)).convert("RGBA")


def composite_with_background(
    foreground: Image.Image, 
    background_path: str,
    output_size: tuple = (800, 800),
    position: str = "center"
) -> Image.Image:
    """
    将抠图后的商品与背景合成
    
    参数:
        foreground: 透明背景的商品图
        background_path: 背景图片路径
        output_size: 输出尺寸
        position: 商品位置 (center/bottom)
    
    返回:
        合成后的PIL Image对象
    """
    # 加载背景
    background = Image.open(background_path).convert("RGBA")
    background = background.resize(output_size, Image.Resampling.LANCZOS)
    
    # 调整商品大小（保持宽高比，最大占背景的80%）
    max_size = int(min(output_size) * 0.8)
    fg_ratio = min(max_size / foreground.width, max_size / foreground.height)
    new_size = (int(foreground.width * fg_ratio), int(foreground.height * fg_ratio))
    foreground = foreground.resize(new_size, Image.Resampling.LANCZOS)
    
    # 计算位置
    if position == "center":
        x = (output_size[0] - foreground.width) // 2
        y = (output_size[1] - foreground.height) // 2
    elif position == "bottom":
        x = (output_size[0] - foreground.width) // 2
        y = output_size[1] - foreground.height - 20
    else:
        x, y = 0, 0
    
    # 合成
    result = background.copy()
    result.paste(foreground, (x, y), foreground)
    
    return result.convert("RGB")


def create_solid_background(
    color: tuple = (230, 235, 225),  # 莫兰迪绿灰色
    size: tuple = (800, 800)
) -> Image.Image:
    """
    创建纯色背景
    
    参数:
        color: RGB颜色值
        size: 背景尺寸
    
    返回:
        纯色背景图
    """
    return Image.new("RGB", size, color)


def create_gradient_background(
    color1: tuple = (245, 243, 238),  # 米白色
    color2: tuple = (225, 230, 220),  # 莫兰迪绿
    size: tuple = (800, 800),
    direction: str = "vertical"
) -> Image.Image:
    """
    创建渐变背景
    
    参数:
        color1: 起始颜色
        color2: 结束颜色
        size: 背景尺寸
        direction: 渐变方向 (vertical/horizontal)
    
    返回:
        渐变背景图
    """
    img = Image.new("RGB", size)
    
    for i in range(size[1] if direction == "vertical" else size[0]):
        ratio = i / (size[1] if direction == "vertical" else size[0])
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        
        if direction == "vertical":
            for j in range(size[0]):
                img.putpixel((j, i), (r, g, b))
        else:
            for j in range(size[1]):
                img.putpixel((i, j), (r, g, b))
    
    return img


def process_single_image(
    input_path: str,
    output_path: str,
    background_path: str = None,
    use_gradient: bool = True
) -> bool:
    """
    处理单张图片
    
    参数:
        input_path: 输入图片路径
        output_path: 输出图片路径
        background_path: 背景图片路径（可选）
        use_gradient: 无背景时是否使用渐变
    
    返回:
        是否成功
    """
    try:
        print(f"处理中: {input_path}")
        
        # 1. 抠图
        foreground = remove_background(input_path)
        
        # 2. 准备背景
        if background_path and os.path.exists(background_path):
            result = composite_with_background(foreground, background_path)
        else:
            # 使用默认莫兰迪渐变背景
            if use_gradient:
                background = create_gradient_background()
            else:
                background = create_solid_background()
            
            # 合成
            background = background.convert("RGBA")
            max_size = int(min(800, 800) * 0.8)
            fg_ratio = min(max_size / foreground.width, max_size / foreground.height)
            new_size = (int(foreground.width * fg_ratio), int(foreground.height * fg_ratio))
            foreground = foreground.resize(new_size, Image.Resampling.LANCZOS)
            
            x = (800 - foreground.width) // 2
            y = (800 - foreground.height) // 2
            background.paste(foreground, (x, y), foreground)
            result = background.convert("RGB")
        
        # 3. 保存
        result.save(output_path, "JPEG", quality=95)
        print(f"完成: {output_path}")
        return True
        
    except Exception as e:
        print(f"处理失败 {input_path}: {e}")
        return False


def batch_process(
    input_dir: str,
    output_dir: str,
    background_path: str = None
) -> dict:
    """
    批量处理图片
    
    参数:
        input_dir: 输入目录
        output_dir: 输出目录
        background_path: 背景图片路径
    
    返回:
        处理结果统计
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 支持的图片格式
    extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    
    # 统计
    stats = {"success": 0, "failed": 0, "skipped": 0}
    
    for file in input_path.iterdir():
        if file.suffix.lower() not in extensions:
            stats["skipped"] += 1
            continue
        
        output_file = output_path / f"{file.stem}_processed.jpg"
        
        if process_single_image(str(file), str(output_file), background_path):
            stats["success"] += 1
        else:
            stats["failed"] += 1
    
    return stats


def main():
    parser = argparse.ArgumentParser(description="商品图片批量处理工具")
    parser.add_argument("--input", "-i", required=True, help="输入图片目录")
    parser.add_argument("--output", "-o", required=True, help="输出目录")
    parser.add_argument("--background", "-b", default=None, help="背景图片路径（可选）")
    parser.add_argument("--single", "-s", action="store_true", help="单张图片模式")
    
    args = parser.parse_args()
    
    if args.single:
        # 单张处理
        output_file = Path(args.output)
        if output_file.is_dir():
            output_file = output_file / f"{Path(args.input).stem}_processed.jpg"
        
        success = process_single_image(args.input, str(output_file), args.background)
        sys.exit(0 if success else 1)
    else:
        # 批量处理
        stats = batch_process(args.input, args.output, args.background)
        
        print("\n" + "=" * 40)
        print(f"处理完成！")
        print(f"  成功: {stats['success']}")
        print(f"  失败: {stats['failed']}")
        print(f"  跳过: {stats['skipped']}")
        print("=" * 40)


if __name__ == "__main__":
    main()
