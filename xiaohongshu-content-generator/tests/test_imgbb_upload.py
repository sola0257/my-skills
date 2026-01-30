#!/usr/bin/env python3
"""
ImgBB 图床上传测试
"""
import requests
import base64

# ImgBB API 配置
API_KEY = "392e09c3d61043f9de6371365696ee56"
UPLOAD_URL = "https://api.imgbb.com/1/upload"

# 测试上传照片
image_path = "/Users/dj/.claude/skills/xiaohongshu-content-generator/knowledge/character_references/primary_ref.jpg"

print("📤 测试上传到 ImgBB...")
print(f"📁 文件: {image_path}")

# 读取图片并转换为 base64
with open(image_path, "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# 上传到 imgbb
payload = {
    "key": API_KEY,
    "image": image_data,
    "name": "primary_ref"
}

try:
    response = requests.post(UPLOAD_URL, data=payload, timeout=60)
    print(f"📊 响应状态码: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            image_url = result["data"]["url"]
            display_url = result["data"]["display_url"]

            print(f"\n✅ 上传成功！")
            print(f"📷 图片 URL: {image_url}")
            print(f"🔗 显示 URL: {display_url}")
        else:
            print(f"❌ 上传失败: {result}")
    else:
        print(f"❌ 请求失败: {response.text}")

except Exception as e:
    print(f"❌ 上传异常: {e}")
