#!/usr/bin/env python3
"""
上传所有参考照片到 ImgBB 并保存 URL
"""
import requests
import base64
import json
from pathlib import Path

# ImgBB API 配置
API_KEY = "392e09c3d61043f9de6371365696ee56"
UPLOAD_URL = "https://api.imgbb.com/1/upload"

# 参考照片路径
skill_dir = Path("/Users/dj/.claude/skills/xiaohongshu-content-generator")
ref_dir = skill_dir / "knowledge/character_references"

# 需要上传的照片
photos = {
    "primary_ref": ref_dir / "primary_ref.jpg",
    "secondary_ref": ref_dir / "secondary_ref.HEIF",
    "backup_01": ref_dir / "backup_01.HEIC",
    "backup_02": ref_dir / "backup_02.heic"
}

# 先转换 HEIC/HEIF 为 JPG
import subprocess

for name, path in photos.items():
    if path.suffix.lower() in ['.heic', '.heif']:
        jpg_path = path.with_suffix('.jpg')
        if not jpg_path.exists():
            print(f"🔄 转换 {path.name} 为 JPG...")
            subprocess.run(['sips', '-s', 'format', 'jpeg', str(path), '--out', str(jpg_path)],
                         capture_output=True)
        photos[name] = jpg_path

# 上传所有照片
uploaded_urls = {}

for name, path in photos.items():
    print(f"\n📤 上传 {name}...")

    try:
        with open(path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        payload = {
            "key": API_KEY,
            "image": image_data,
            "name": name
        }

        response = requests.post(UPLOAD_URL, data=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                url = result["data"]["url"]
                uploaded_urls[name] = url
                print(f"✅ {name}: {url}")
            else:
                print(f"❌ {name} 上传失败")
        else:
            print(f"❌ {name} 请求失败")

    except Exception as e:
        print(f"❌ {name} 异常: {e}")

# 保存 URL 配置
config_file = ref_dir / "imgbb_urls.json"
with open(config_file, "w") as f:
    json.dump(uploaded_urls, f, indent=2, ensure_ascii=False)

print(f"\n✅ 所有 URL 已保存到: {config_file}")
print(f"\n📋 上传结果:")
for name, url in uploaded_urls.items():
    print(f"  {name}: {url}")
