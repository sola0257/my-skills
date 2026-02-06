#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号内容推送脚本 v3.0
功能：将Markdown文档转换为HTML并推送到公众号草稿箱

v3.0 更新 (2026-01-30):
- 图片处理策略优化：
  * 封面图：使用图床（API 数据库字段限制）
  * 正文图片：优先 Base64 嵌入（≤2MB），过大则用图床
- 优势：减少外部依赖，提高推送可靠性
"""

import os
import sys
import json
import requests
import re
import base64
from datetime import datetime
from pathlib import Path

# API配置
API_BASE = "https://wx.limyai.com/api/openapi"
SUBSCRIPTION_API_KEY = "xhs_1beb09d01e1f7600af37b438a845a07c"
SERVICE_API_KEY = "xhs_1a04cc8001bc87b37cc032bdde2517b0"

# 公众号AppID
SUBSCRIPTION_APPID = "wxfb77628a184ae198"  # 静待花开 慢养四季（订阅号）
SERVICE_APPID = "wx86ea292c58e761ad"  # 慢养四季（服务号）

# ImgBB图床配置（备用方案）
IMGBB_API_KEY = "392e09c3d61043f9de6371365696ee56"
IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"

# 图片大小阈值（2MB）
MAX_BASE64_SIZE = 0  # Force ImgBB for better editor compatibility


def get_image_mime_type(image_path):
    """
    根据文件扩展名获取MIME类型

    Args:
        image_path: 图片文件路径

    Returns:
        MIME类型字符串
    """
    ext = os.path.splitext(image_path)[1].lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    return mime_types.get(ext, 'image/jpeg')


from PIL import Image
import io

def compress_image_to_jpeg_bytes(image_path, quality=80):
    """
    读取图片并压缩为JPEG格式的bytes
    """
    try:
        with Image.open(image_path) as img:
            # 转换为RGB（兼容PNG透明通道，防止变黑）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            output_buffer = io.BytesIO()
            img.save(output_buffer, format='JPEG', quality=quality)
            return output_buffer.getvalue()
    except Exception as e:
        print(f"❌ 图片压缩失败: {e}")
        return None

def image_to_base64_data_uri(image_path):
    """
    将图片转换为 Base64 Data URI (带自动压缩)
    """
    try:
        # 尝试压缩图片
        image_data = compress_image_to_jpeg_bytes(image_path)
        mime_type = 'image/jpeg' # 压缩后统一为 JPEG
        
        if image_data is None:
            # 如果压缩失败，回退到原始读取
            with open(image_path, 'rb') as f:
                image_data = f.read()
            mime_type = get_image_mime_type(image_path)

        # 获取文件大小
        file_size = len(image_data)

        # 如果文件过大，返回 None（将使用图床）
        if file_size > MAX_BASE64_SIZE:
            print(f"⚠️  图片过大 ({file_size / 1024 / 1024:.2f}MB)，将使用图床: {os.path.basename(image_path)}")
            return None

        # 转换为 Base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        data_uri = f"data:{mime_type};base64,{image_base64}"

        print(f"✅ Base64 生成成功 (压缩后 {file_size / 1024:.1f}KB): {os.path.basename(image_path)}")
        return data_uri

    except Exception as e:
        print(f"❌ Base64 转换失败: {e}")
        return None


def upload_image_to_imgbb(image_path):
    """
    上传图片到ImgBB图床（备用方案）

    Args:
        image_path: 图片文件路径

    Returns:
        图片URL，失败返回None
    """
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()

        image_base64 = base64.b64encode(image_data).decode('utf-8')

        response = requests.post(
            IMGBB_UPLOAD_URL,
            data={
                'key': IMGBB_API_KEY,
                'image': image_base64
            },
            timeout=30
        )

        result = response.json()
        if result.get('success'):
            url = result['data']['url']
            print(f"✅ 图床上传成功: {os.path.basename(image_path)}")
            return url
        else:
            print(f"❌ 图床上传失败: {result.get('error', {}).get('message', '未知错误')}")
            return None

    except Exception as e:
        print(f"❌ 图床上传异常: {e}")
        return None


def markdown_to_html_with_base64(markdown_content, image_folder):
    """
    将Markdown转换为HTML，并将图片嵌入为Base64（用户指定模式）
    
    Args:
        markdown_content: Markdown内容
        image_folder: 图片文件夹路径
        
    Returns:
        HTML内容, 封面图Base64
    """
    html_content = markdown_content
    cover_image_data = None
    
    # 1. 转换标题 (带微信风格样式)
    html_content = re.sub(r'^# (.*?)$', r'<h1 style="font-size: 22px; font-weight: bold; color: #333; margin-bottom: 20px;">\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.*?)$', r'<h2 style="font-size: 18px; font-weight: bold; border-bottom: 2px solid #07c160; padding-bottom: 10px; margin-top: 30px; margin-bottom: 15px; color: #07c160;">\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.*?)$', r'<h3 style="font-size: 16px; font-weight: bold; border-left: 4px solid #07c160; padding-left: 10px; margin-top: 20px; margin-bottom: 10px; color: #333;">\1</h3>', html_content, flags=re.MULTILINE)
    
    # 2. 转换加粗
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    
    # 3. 处理图片 - 转换为Base64并嵌入
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(image_pattern, html_content)
    
    for i, (alt_text, image_file) in enumerate(matches):
        image_path = os.path.join(image_folder, image_file)
        
        if os.path.exists(image_path):
            print(f"🔄 处理图片: {os.path.basename(image_path)}")
            
            # 策略：封面图必须上传图床（为了 coverImage 字段），正文图使用 Base64（为了编辑器稳定）
            
            # 1. 如果是第一张图（封面），先上传图床获取 URL 用于 API metadata
            if i == 0:
                print(f"📸 封面图上传图床(用于封面字段): {os.path.basename(image_path)}")
                cover_url = upload_image_to_imgbb(image_path)
                if cover_url:
                    cover_image_data = cover_url
            
            # 2. 生成 Base64 用于正文嵌入 (带压缩)
            image_uri = image_to_base64_data_uri(image_path)
            
            if image_uri:
                 img_tag = f'<p style="text-align: center; margin: 10px 0;"><img src="{image_uri}" alt="{alt_text}" style="max-width:100%; height:auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" /></p>'
                 html_content = html_content.replace(f'![{alt_text}]({image_file})', img_tag)
                 print(f"✅ 图片已嵌入HTML (Base64): {os.path.basename(image_path)}")
            else:
                print(f"❌ Base64生成失败，尝试使用图床链接")
                # 如果 Base64 失败（比如太大），尝试用图床链接
                fallback_url = upload_image_to_imgbb(image_path)
                if fallback_url:
                    img_tag = f'<p style="text-align: center; margin: 10px 0;"><img src="{fallback_url}" alt="{alt_text}" style="max-width:100%; height:auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" /></p>'
                    html_content = html_content.replace(f'![{alt_text}]({image_file})', img_tag)
                    print(f"✅ 图片已替换为URL (Fallback): {os.path.basename(image_path)}")

        else:
            print(f"⚠️  图片文件不存在: {image_path}")
            
    # 4. 处理段落 (将剩余的非HTML行包裹在<p>中)
    lines = html_content.split('\n')
    new_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('<'): # 已经是HTML标签
            new_lines.append(line)
        else:
            new_lines.append(f'<p>{line}</p>')
            
    html_content = '\n'.join(new_lines)
    
    return html_content, cover_image_data

def process_markdown_images(markdown_content, image_folder):
    # This function is kept for backward compatibility but main logic will switch
    pass 


def extract_summary(markdown_content):
    """
    从Markdown中提取摘要

    Args:
        markdown_content: Markdown内容

    Returns:
        摘要文本（≤25字）
    """
    # 查找引用块（> 开头的行）
    quote_pattern = r'^>\s*(.+)$'
    match = re.search(quote_pattern, markdown_content, re.MULTILINE)

    if match:
        summary = match.group(1).strip()
        # 限制25字（微信转发卡片显示要求）
        if len(summary) > 25:
            summary = summary[:22] + "..."
        return summary

    # 如果没有引用块，提取第一段
    paragraphs = markdown_content.split('\n\n')
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('#') and not p.startswith('!'):
            # 移除Markdown格式
            p = re.sub(r'\*\*(.+?)\*\*', r'\1', p)
            p = re.sub(r'\*(.+?)\*', r'\1', p)
            if len(p) > 25:
                p = p[:22] + "..."
            return p

    return ""


def push_to_wechat_draft(title, content, summary, cover_image, account_type='subscription'):
    """
    推送内容到微信公众号草稿箱

    Args:
        title: 文章标题
        content: Markdown内容
        summary: 文章摘要
        cover_image: 封面图URL或Data URI
        account_type: 账号类型 ('subscription' 或 'service')

    Returns:
        推送结果字典
    """
    api_key = SUBSCRIPTION_API_KEY if account_type == 'subscription' else SERVICE_API_KEY
    wechat_appid = SUBSCRIPTION_APPID if account_type == 'subscription' else SERVICE_APPID

    try:
        # 构建请求数据
        payload = {
            'wechatAppid': wechat_appid,
            'title': title,
            'content': content,
            'contentFormat': 'markdown',
            'articleType': 'news',
            'author': '小静'
        }

        # 添加可选参数
        if summary:
            payload['summary'] = summary
        if cover_image:
            payload['coverImage'] = cover_image

        print(f"📡 API URL: {API_BASE}/wechat-publish")
        print(f"🔑 API Key: {api_key[:20]}...")
        print(f"📱 AppID: {wechat_appid}")

        # 发送请求
        response = requests.post(
            f"{API_BASE}/wechat-publish",
            headers={
                'X-API-Key': api_key,
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=60
        )

        print(f"📊 HTTP Status: {response.status_code}")

        # 解析响应
        result = response.json()
        print(f"📄 Response: {json.dumps(result, indent=2, ensure_ascii=False)}")

        return result

    except Exception as e:
        return {
            'success': False,
            'error': f'推送异常: {str(e)}'
        }


def main(markdown_file, account_type='subscription'):
    """
    主函数：读取Markdown文件并推送到草稿箱

    Args:
        markdown_file: Markdown文件路径
        account_type: 账号类型
    """
    print(f"\n{'='*50}")
    print(f"📤 开始推送到{account_type}草稿箱")
    print(f"{'='*50}\n")

    # 检查文件是否存在
    if not os.path.exists(markdown_file):
        print(f"❌ 文件不存在: {markdown_file}")
        return False

    # 读取Markdown文件
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # 提取标题
    title_match = re.search(r'^# (.+)$', markdown_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "未命名文章"
    # 移除emoji和多余空格
    title = title.strip()

    # 获取图片文件夹
    image_folder = os.path.dirname(markdown_file)

    # 处理图片 - 切换到 HTML + Base64 (压缩版) 模式
    print("🖼️  处理图片...")
    print("📋 策略: 智能压缩 + Base64嵌入。将图片压缩为JPEG以减小体积，解决编辑器丢图问题。\n")
    
    # 使用新函数转换
    processed_content, cover_image = markdown_to_html_with_base64(markdown_content, image_folder)

    # DEBUG: 保存生成的 HTML 到本地以供检查
    debug_html_path = os.path.join(image_folder, "debug_preview.html")
    with open(debug_html_path, "w", encoding="utf-8") as f:
        # 添加简单的 HTML 骨架以便浏览器预览
        f.write('<!DOCTYPE html><html><head><meta charset="utf-8"><style>img {max-width:100%;}</style></head><body>')
        f.write(processed_content)
        f.write('</body></html>')
    print(f"🐛 [DEBUG] HTML预览已保存: {debug_html_path}")
    print(f"   请检查此文件以确认 Base64 图片是否正确嵌入")

    # 提取摘要
    print("\n📝 提取摘要...")
    summary = extract_summary(markdown_content)
    print(f"   摘要: {summary}")

    # 推送到草稿箱
    print(f"\n📤 推送到{account_type}草稿箱...")
    
    api_key = SUBSCRIPTION_API_KEY if account_type == 'subscription' else SERVICE_API_KEY
    wechat_appid = SUBSCRIPTION_APPID if account_type == 'subscription' else SERVICE_APPID

    try:
        payload = {
            'wechatAppid': wechat_appid,
            'title': title,
            'content': processed_content,
            'contentFormat': 'html',  # 必须使用 HTML 格式才能支持 Base64 img 标签
            'articleType': 'news',
            'author': '小静'
        }

        if summary:
            payload['summary'] = summary
        if cover_image:
            # 封面图直接传 Base64 Data URI
            payload['coverImage'] = cover_image

        print(f"📡 API URL: {API_BASE}/wechat-publish")
        
        response = requests.post(
            f"{API_BASE}/wechat-publish",
            headers={
                'X-API-Key': api_key,
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=180 # Base64 数据量大，增加超时
        )
        
        print(f"📊 HTTP Status: {response.status_code}")
        result = response.json()
        print(f"📄 Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        result = {'success': False, 'error': str(e)}

    # 保存推送结果
    result_file = os.path.join(image_folder, "推送结果.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            'status': 'success' if result.get('success') else 'failed',
            'result': result,
            'push_time': datetime.now().isoformat(),
            'account_type': account_type,
            'title': title,
            'summary': summary
        }, f, ensure_ascii=False, indent=2)

    # 输出结果
    if result.get('success'):
        data = result.get('data', {})
        media_id = data.get('mediaId', '')
        publication_id = data.get('publicationId', '')

        print(f"\n✅ 推送成功！")
        print(f"📋 Media ID: {media_id}")
        print(f"🆔 Publication ID: {publication_id}")
        print(f"🔗 草稿箱链接: https://mp.weixin.qq.com/cgi-bin/appmsg?action=list&type=10")
        print(f"📁 结果已保存: {result_file}\n")
        return True
    else:
        error_msg = result.get('error', '未知错误')
        error_code = result.get('code', '')
        print(f"\n❌ 推送失败: {error_msg}")
        if error_code:
            print(f"🔢 错误码: {error_code}")
        print(f"📁 错误详情已保存: {result_file}\n")
        return False


if __name__ == '__main__':
    # 处理 --help 参数
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        print("=" * 50)
        print("📤 微信公众号推送脚本 v3.0")
        print("=" * 50)
        print("\n用法:")
        print("  python wechat_publish.py <markdown_file> [account_type]")
        print("\n参数:")
        print("  markdown_file   Markdown文件路径（必需）")
        print("  account_type    账号类型（可选，默认: subscription）")
        print("                  - subscription: 订阅号")
        print("                  - service: 服务号")
        print("\n示例:")
        print("  python wechat_publish.py article.md")
        print("  python wechat_publish.py article.md subscription")
        print("  python wechat_publish.py article.md service")
        print("\n功能:")
        print("  - 封面图: 使用图床")
        print("  - 正文图片: Base64嵌入（≤2MB）或图床（>2MB）")
        print("  - 自动提取标题、摘要")
        print("  - 推送到公众号草稿箱")
        print()
        sys.exit(0)
    
    if len(sys.argv) < 2:
        print("用法: python wechat_publish.py <markdown_file> [account_type]")
        print("使用 --help 查看详细帮助")
        sys.exit(1)

    markdown_file = sys.argv[1]
    account_type = sys.argv[2] if len(sys.argv) > 2 else 'subscription'

    success = main(markdown_file, account_type)
    sys.exit(0 if success else 1)
