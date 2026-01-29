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
MAX_BASE64_SIZE = 2 * 1024 * 1024  # 2MB


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


def image_to_base64_data_uri(image_path):
    """
    将图片转换为 Base64 Data URI

    Args:
        image_path: 图片文件路径

    Returns:
        Base64 Data URI 字符串，失败返回 None
    """
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # 获取文件大小
        file_size = len(image_data)

        # 如果文件过大，返回 None（将使用图床）
        if file_size > MAX_BASE64_SIZE:
            print(f"⚠️  图片过大 ({file_size / 1024 / 1024:.2f}MB)，将使用图床: {os.path.basename(image_path)}")
            return None

        # 转换为 Base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        mime_type = get_image_mime_type(image_path)
        data_uri = f"data:{mime_type};base64,{image_base64}"

        print(f"✅ Base64 嵌入成功 ({file_size / 1024:.1f}KB): {os.path.basename(image_path)}")
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


def process_markdown_images(markdown_content, image_folder):
    """
    处理Markdown中的图片

    策略（v3.0 优化）：
    1. 封面图：必须使用图床（API 数据库字段有长度限制）
    2. 正文图片：优先 Base64 嵌入（≤2MB），过大则用图床

    Args:
        markdown_content: Markdown内容
        image_folder: 图片文件夹路径

    Returns:
        处理后的Markdown内容，封面图URL
    """
    cover_image_url = None
    processed_content = markdown_content

    # 查找所有图片引用
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(image_pattern, processed_content)

    for i, (alt_text, image_file) in enumerate(matches):
        image_path = os.path.join(image_folder, image_file)

        if os.path.exists(image_path):
            # 第一张图是封面，必须使用图床（API 限制）
            if i == 0:
                print(f"📸 封面图使用图床: {os.path.basename(image_path)}")
                image_uri = upload_image_to_imgbb(image_path)
                if image_uri:
                    cover_image_url = image_uri
            else:
                # 正文图片：尝试 Base64，失败则用图床
                image_uri = image_to_base64_data_uri(image_path)
                if not image_uri:
                    print(f"📤 使用图床备用方案: {os.path.basename(image_path)}")
                    image_uri = upload_image_to_imgbb(image_path)

            if image_uri:
                # 替换图片链接
                processed_content = processed_content.replace(
                    f'![{alt_text}]({image_file})',
                    f'![{alt_text}]({image_uri})'
                )
        else:
            print(f"⚠️  图片文件不存在: {image_path}")

    return processed_content, cover_image_url


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

    # 处理图片
    print("🖼️  处理图片...")
    print("📋 策略: 封面用图床 + 正文用Base64（≤2MB）\n")
    processed_content, cover_image = process_markdown_images(markdown_content, image_folder)

    # 提取摘要
    print("\n📝 提取摘要...")
    summary = extract_summary(markdown_content)
    print(f"   摘要: {summary}")

    # 推送到草稿箱
    print(f"\n📤 推送到{account_type}草稿箱...")
    result = push_to_wechat_draft(title, processed_content, summary, cover_image, account_type)

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
    if len(sys.argv) < 2:
        print("用法: python wechat_publish.py <markdown_file> [account_type]")
        print("account_type: subscription (默认) 或 service")
        sys.exit(1)

    markdown_file = sys.argv[1]
    account_type = sys.argv[2] if len(sys.argv) > 2 else 'subscription'

    success = main(markdown_file, account_type)
    sys.exit(0 if success else 1)
