#!/usr/bin/env python3
"""
优化后的人物生成测试
- 降低 --cw 权重（100 → 60）
- 明确指定服装和姿态
- 强调植物为主体
"""
import sys
sys.path.append('/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书')

from deeprouter_mj_api import DeepRouterMJ
import requests
import json

class OptimizedMJ(DeepRouterMJ):
    def submit_imagine_optimized(self, prompt: str, character_ref_url: str, cw_weight: int = 60) -> str:
        """优化的提交方法，可调节 --cw 权重"""
        url = f"{self.base_url}/mj/submit/imagine"

        # 构建 prompt，降低 cw 权重
        full_prompt = f"{prompt} --cref {character_ref_url} --cw {cw_weight} --v 6.1 --ar 3:4"

        payload = {"prompt": full_prompt}

        try:
            print(f"🎨 提交优化任务...")
            print(f"📝 CW权重: {cw_weight}")
            print(f"📝 Prompt: {full_prompt[:150]}...")

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

# 初始化
api = OptimizedMJ("sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I")

# 优化后的 prompt - 强调植物为主，人物为辅
prompt = """
bright living room filled with lush green plants, pothos and monstera on wooden shelves,
a woman in elegant cream linen dress standing naturally among the plants,
she is gently touching a leaf, soft window light, peaceful atmosphere,
plants are the main focus, woman is part of the scene,
natural facial features, relaxed expression,
lifestyle photography, dreamy style, muted colors
"""

character_url = "https://i.ibb.co/WNTZrtcQ/primary-ref.jpg"

print("🎨 测试优化后的生成（降低 CW 权重 + 明确 prompt）")
print("=" * 60)

# 使用较低的 cw 权重（60 instead of 100）
task_id = api.submit_imagine_optimized(prompt, character_url, cw_weight=60)
if not task_id:
    sys.exit(1)

image_url = api.wait_for_result(task_id, max_wait=300)
if not image_url:
    sys.exit(1)

output_path = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/test_optimized_cw60.png"
api.download_image(image_url, output_path)
print(f"\n✅ 完成: {output_path}")
