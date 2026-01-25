#!/usr/bin/env python3
"""
DeepRouter Midjourney API 完整集成
支持上传照片、生成图片、查询任务状态
"""
import requests
import base64
import time
import json
from pathlib import Path

class DeepRouterMJ:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://deeprouter.top"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def upload_image(self, image_path: str) -> str:
        """上传图片到 Discord，返回图片 URL"""
        url = f"{self.base_url}/mj/submit/upload-discord-images"

        # 读取图片并转换为 base64
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        payload = {
            "base64": f"data:image/png;base64,{image_data}"
        }

        try:
            print(f"📤 上传图片: {Path(image_path).name}")
            response = requests.post(url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            if result.get("code") == 1:
                image_url = result.get("result")
                print(f"✅ 上传成功: {image_url}")
                return image_url
            else:
                print(f"❌ 上传失败: {result}")
                return None

        except Exception as e:
            print(f"❌ 上传异常: {e}")
            return None

    def submit_imagine(self, prompt: str, character_ref_url: str = None) -> str:
        """提交 Imagine 任务，返回任务 ID"""
        url = f"{self.base_url}/mj/submit/imagine"

        # 构建完整 prompt
        full_prompt = prompt

        # 如果使用 character reference，必须指定 v6.1
        if character_ref_url:
            full_prompt += f" --cref {character_ref_url} --cw 100 --v 6.1"

        # 确保有纵向比例
        if "--ar" not in full_prompt:
            full_prompt += " --ar 3:4"

        payload = {
            "prompt": full_prompt
        }

        try:
            print(f"🎨 提交生成任务...")
            print(f"📝 Prompt: {full_prompt[:100]}...")

            response = requests.post(url, headers=self.headers, json=payload, timeout=60)
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
        """查询任务状态"""
        url = f"{self.base_url}/mj/task/{task_id}/fetch"

        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()

            result = response.json()
            return result

        except Exception as e:
            print(f"❌ 查询异常: {e}")
            return None

    def submit_upscale(self, task_id: str, index: int = 1) -> str:
        """提交 Upscale 任务，选择 grid 中的某一张进行放大

        Args:
            task_id: 原始 imagine 任务的 ID
            index: 选择第几张图片 (1-4)

        Returns:
            新的 upscale 任务 ID
        """
        url = f"{self.base_url}/mj/submit/simple-change"

        payload = {
            "content": f"{task_id} U{index}"
        }

        try:
            print(f"🔍 提交 Upscale 任务（选择第 {index} 张）...")
            response = requests.post(url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            if result.get("code") == 1:
                upscale_task_id = result.get("result")
                print(f"✅ Upscale 任务提交成功，ID: {upscale_task_id}")
                return upscale_task_id
            else:
                print(f"❌ Upscale 提交失败: {result}")
                return None

        except Exception as e:
            print(f"❌ Upscale 提交异常: {e}")
            return None

    def wait_for_result(self, task_id: str, max_wait: int = 300, auto_upscale: bool = True) -> str:
        """等待任务完成并返回图片 URL

        Args:
            task_id: 任务 ID
            max_wait: 最大等待时间（秒）
            auto_upscale: 是否自动 upscale（默认 True）

        Returns:
            图片 URL
        """
        print(f"⏳ 等待生成完成（最多等待 {max_wait} 秒）...")
        start_time = time.time()

        while time.time() - start_time < max_wait:
            task_info = self.query_task(task_id)

            if not task_info:
                time.sleep(10)
                continue

            status = task_info.get("status")
            progress = task_info.get("progress", "0%")

            if status == "SUCCESS":
                # 检查是否是 grid 图（4张组合）
                action = task_info.get("action", "")

                if action == "IMAGINE" and auto_upscale:
                    # 这是 grid 图，需要 upscale
                    print(f"✅ Grid 生成完成！")
                    print(f"🔍 自动选择第1张进行 Upscale...")

                    upscale_task_id = self.submit_upscale(task_id, index=1)
                    if upscale_task_id:
                        # 递归等待 upscale 完成
                        return self.wait_for_result(upscale_task_id, max_wait=max_wait, auto_upscale=False)
                    else:
                        # Upscale 失败，返回 grid 图
                        print(f"⚠️ Upscale 失败，返回 Grid 图")
                        return task_info.get("imageUrl")
                else:
                    # 这是最终的单张图
                    image_url = task_info.get("imageUrl")
                    print(f"✅ 生成完成！")
                    return image_url

            elif status == "FAILURE":
                fail_reason = task_info.get("failReason", "未知错误")
                print(f"❌ 生成失败: {fail_reason}")
                return None
            else:
                print(f"⏳ 进度: {progress} - 状态: {status}")
                time.sleep(15)

        print(f"❌ 超时：等待超过 {max_wait} 秒")
        return None

    def download_image(self, image_url: str, save_path: str):
        """下载生成的图片"""
        try:
            print(f"💾 下载图片...")
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()

            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(response.content)

            print(f"✅ 图片已保存: {save_path}")
            return True

        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return False

    def generate_with_character(self, prompt: str, character_image_path: str, output_path: str):
        """完整流程：上传人物照片 → 生成图片 → 下载"""
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
    api = DeepRouterMJ("sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I")

    # 植物场景 prompt
    prompt = """
    A woman in cream linen dress standing in a bright living room corner,
    surrounded by green plants including pothos, monstera, and orchids in ceramic pots,
    gently touching plant leaves, soft natural window light streaming through sheer curtains,
    warm golden hour glow, wooden furniture, cream walls, peaceful and fresh mood,
    lifestyle photography, dreamy realistic style, soft focus, film-like quality,
    muted Morandi colors, low saturation
    """

    # 使用 skill 中的参考照片（JPG 格式）
    character_image = "/Users/dj/.claude/skills/xiaohongshu-content-generator/knowledge/character_references/primary_ref.jpg"

    # 输出路径
    output_path = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/test_deeprouter_character.png"

    # 执行生成
    api.generate_with_character(prompt, character_image, output_path)
