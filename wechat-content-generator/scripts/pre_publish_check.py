#!/usr/bin/env python3
"""
微信公众号推送前检查脚本
"""
import os
import sys
import argparse
import json
from pathlib import Path

def check_file_integrity(content_dir):
    print("🔍 检查文件完整性...")
    content_dir = Path(content_dir)
    md_files = list(content_dir.glob("*.md"))
    if not md_files:
        return False, "❌ 没有找到 Markdown 内容文件"
    
    png_files = list(content_dir.glob("*.png"))
    if not png_files:
        return False, "❌ 没有找到配图文件 (.png)"
        
    print(f"✅ 找到 {len(md_files)} 个文档, {len(png_files)} 张图片")
    return True, "通过"

def check_image_specs(content_dir):
    print("🔍 检查配图规范...")
    # 这里简单检查文件大小，不依赖 PIL 以免环境问题
    content_dir = Path(content_dir)
    images = list(content_dir.glob("*.png"))
    
    for img in images:
        size = img.stat().st_size
        if size > 5 * 1024 * 1024: # 5MB limit
            return False, f"❌ 图片过大: {img.name} ({size/1024/1024:.2f}MB)"
            
    print("✅ 所有图片文件大小检查通过")
    return True, "通过"

def check_content_quality(content_dir):
    print("🔍 检查内容质量...")
    content_dir = Path(content_dir)
    md_file = list(content_dir.glob("*.md"))[0]
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if len(content) < 100:
        return False, "❌ 内容过短"
        
    if "[TODO]" in content or "待补充" in content:
        return False, "❌ 发现未完成的占位符"
        
    print(f"✅ 内容长度 {len(content)} 字符，无明显占位符")
    return True, "通过"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-dir", required=True, help="内容目录路径")
    args = parser.parse_args()
    
    checks = [
        check_file_integrity,
        check_image_specs,
        check_content_quality
    ]
    
    all_pass = True
    for check in checks:
        passed, msg = check(args.content_dir)
        if not passed:
            print(f"{msg}")
            all_pass = False
            
    if all_pass:
        print("\n✨ 所有检查通过，准备推送！")
        sys.exit(0)
    else:
        print("\n❌ 检查失败，请修正后重试。")
        sys.exit(1)

if __name__ == "__main__":
    main()
