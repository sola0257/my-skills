#!/usr/bin/env python3
"""
Midjourney API 集成脚本
用于小红书封面图生成（带人物一致性）
"""
import requests
import base64
import time
import json
from pathlib import Path

class MidjourneyAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://yunwu.ai"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def upload_image(self, image_path: str) -> str:
        """
        上传图片到 Midjourney（用于 --cref）
        返回图片 URL
        """
        # 读取图片并转换为 base64
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        # 调用上传接口
        url = f"{self.base_url}/mj/submit/upload"
        payload = {
            "base64": f"data:image/png;base64,{image_data}"
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            print(f"📊 响应状态码: {response.status_code}")
            print(f"📊 响应内容: {response.text[:500]}")  # 打印前500字符

            response.raise_for_status()
            result = response.json()

            # 返回上传后的图片 URL
            if result.get("code") == 1:
                image_url = result.get("result")
                print(f"✅ 图片上传成功: {image_url}")
                return image_url
            else:
                print(f"❌ 上传失败: {result}")
                return None

        except Exception as e:
            print(f"❌ 上传异常: {e}")
            print(f"📊 响应文本: {response.text if 'response' in locals() else 'No response'}")
            return None

    def submit_imagine(self, prompt: str, character_ref_url: str = None) -> str:
        """
        提交 Midjourney 生成任务
        返回任务 ID
        """
        # 构建完整 prompt
        full_prompt = prompt
        if character_ref_url:
            full_prompt += f" --cref {character_ref_url} --cw 100"

        # 添加纵向比例
        if "--ar" not in full_prompt:
            full_prompt += " --ar 3:4"

        url = f"{self.base_url}/mj/submit/imagine"
        payload = {
            "botType": "MID_JOURNEY",
            "prompt": full_prompt,
            "base64Array": [],
            "notifyHook": "",
            "state": ""
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 1:
                task_id = result.get("result")
                print(f"✅ 任务提交成功，ID: {task_id}")
                return task_id
            else:
                print(f"❌ 提交失败: {result}")
                return None

        except Exception as e:
            print(f"❌ 提交异常: {e}")
            return None

    def query_task(self, task_id: str) -> dict:
        """
        查询任务状态
        返回任务信息
        """
        url = f"{self.base_url}/mj/task/list-by-condition"
        payload = {
            "ids": [task_id]
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()

            if result and len(result) > 0:
                return result[0]
            return None

        except Exception as e:
            print(f"❌ 查询异常: {e}")
            return None

    def wait_for_result(self, task_id: str, max_wait: int = 300) -> str:
        """
        等待任务完成并返回图片 URL
        max_wait: 最大等待时间（秒）
        """
        print(f"⏳ 等待生成完成...")
        start_time = time.time()

        while time.time() - start_time < max_wait:
            task_info = self.query_task(task_id)

            if not task_info:
                time.sleep(5)
                continue

            status = task_info.get("status")
            progress = task_info.get("progress", "0%")

            if status == "SUCCESS":
                image_url = task_info.get("imageUrl")
                print(f"✅ 生成完成！")
                return image_url
            elif status == "FAILURE":
                fail_reason = task_info.get("failReason", "未知错误")
                print(f"❌ 生成失败: {fail_reason}")
                return None
            else:
                print(f"⏳ 进度: {progress}")
                time.sleep(10)

        print(f"❌ 超时：等待超过 {max_wait} 秒")
        return None

    def download_image(self, image_url: str, save_path: str):
        """
        下载生成的图片
        """
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            with open(save_path, "wb") as f:
                f.write(response.content)

            print(f"✅ 图片已保存: {save_path}")
            return True

        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return False

    def generate_with_character(self, prompt: str, character_image_path: str, output_path: str):
        """
        完整流程：上传人物照片 → 生成图片 → 下载
        """
        print("=" * 60)
        print("🎨 开始生成带人物一致性的图片")
        print("=" * 60)

        # Step 1: 上传人物照片
        print("\n📤 Step 1: 上传人物照片...")
        character_url = self.upload_image(character_image_path)
        if not character_url:
            return False

        # Step 2: 提交生成任务
        print("\n🎨 Step 2: 提交生成任务...")
        task_id = self.submit_imagine(prompt, character_url)
        if not task_id:
            return False

        # Step 3: 等待完成
        print("\n⏳ Step 3: 等待生成完成...")
        image_url = self.wait_for_result(task_id)
        if not image_url:
            return False

        # Step 4: 下载图片
        print("\n💾 Step 4: 下载图片...")
        success = self.download_image(image_url, output_path)

        if success:
            print("\n" + "=" * 60)
            print("✅ 全部完成！")
            print("=" * 60)

        return success


# 使用示例
if __name__ == "__main__":
    # 初始化 API
    api = MidjourneyAPI("sk-92m3Pkv3lmHSHrtg3NFHalSOTJr4wUSeeqIfPLft959Fu3AS")

    # 测试：生成带人物的植物场景
    prompt = """
    A woman in cream linen dress standing in a plant-filled living room,
    gently touching orchid petals, soft natural window light,
    warm golden hour glow, surrounded by pothos and monstera in ceramic pots,
    wooden furniture, cream walls, peaceful mood,
    lifestyle photography, dreamy realistic style, film-like quality
    """

    character_image = "/path/to/your/photo.jpg"  # 替换为你的照片路径
    output_path = "/Users/dj/Documents/test_mj_output.png"

    # 执行生成
    api.generate_with_character(prompt, character_image, output_path)
