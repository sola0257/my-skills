#!/usr/bin/env python3
"""
环境为主的生成测试
- 植物和居家环境是主角
- 人物是场景的一部分，可以模糊
- 极低的 CW 权重或不使用 --cref
"""
import sys
sys.path.append('/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书')

from deeprouter_mj_api import DeepRouterMJ

api = DeepRouterMJ("sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I")

# 方案1：极低 CW 权重（20）- 人物模糊融入环境
prompt_low_cw = """
cozy living room filled with lush green plants, pothos hanging from shelves,
monstera and ferns in ceramic pots, wooden furniture, soft natural window light,
a woman in the background tending to plants, peaceful atmosphere,
plants are the main subject, lifestyle photography, dreamy style,
muted Morandi colors, film-like quality
"""

# 方案2：完全不用 --cref - 通用人物
prompt_no_cref = """
bright plant-filled living room corner, abundant green plants on wooden shelves,
pothos, monstera, orchids in ceramic pots, soft sunlight through sheer curtains,
a person in cream clothing among the plants, peaceful home atmosphere,
focus on the plants and interior, lifestyle photography, dreamy realistic style,
muted colors, low saturation, film grain
"""

print("🎨 测试环境为主的生成方案")
print("=" * 60)

# 测试方案1：极低 CW 权重
print("\n📋 方案1：使用极低 CW 权重（20）")
character_url = "https://i.ibb.co/WNTZrtcQ/primary-ref.jpg"

# 手动构建 prompt
full_prompt_1 = f"{prompt_low_cw} --cref {character_url} --cw 20 --v 6.1 --ar 3:4"

payload_1 = {"prompt": full_prompt_1}
response_1 = api.headers
url = f"{api.base_url}/mj/submit/imagine"

import requests
response = requests.post(url, headers=api.headers, json=payload_1, timeout=60)
result = response.json()

if result.get("code") == 1:
    task_id_1 = result.get("result")
    print(f"✅ 方案1 任务提交成功，ID: {task_id_1}")

    image_url_1 = api.wait_for_result(task_id_1, max_wait=300)
    if image_url_1:
        output_1 = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/test_environment_focus_cw20.png"
        api.download_image(image_url_1, output_1)
        print(f"✅ 方案1 完成: {output_1}")

# 测试方案2：不使用 --cref
print("\n📋 方案2：不使用人物参考（纯环境）")
task_id_2 = api.submit_imagine(prompt_no_cref)

if task_id_2:
    image_url_2 = api.wait_for_result(task_id_2, max_wait=300)
    if image_url_2:
        output_2 = "/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/test_environment_focus_no_cref.png"
        api.download_image(image_url_2, output_2)
        print(f"✅ 方案2 完成: {output_2}")

print("\n" + "=" * 60)
print("✅ 两个方案都已生成，请对比效果")
