---
name: video-script-generator
description: |
  视频脚本生成器，支持知识分享类和生活感悟类视频。
  自动生成分镜脚本 + 逐字稿 + 配图，支持小红书/视频号/快手/抖音多平台适配。
  
  触发场景：
  - "帮我写视频脚本，选题是：[主题]"
  - "生成一个知识分享类视频，关于[主题]"
  - "做一个生活感悟视频：[主题]"
  - "帮我写抖音短视频脚本"
license: MIT
version: "2.1"
---

# 🎬 视频脚本生成器 v2.0

## 🚨 静默执行协议（必须遵守）

**执行规则：**
- ❌ **禁止** 请求确认以继续
- ❌ **禁止** 询问"是否需要更多信息"
- ❌ **禁止** 中途停顿等待用户反馈
- ✅ **必须** 一次性输出完整内容（分镜脚本 + 逐字稿 + 配图）
- ✅ **必须** 数据缺失时使用默认值或网络搜索
- ✅ **必须** 遇到错误时静默处理并继续

---

## 📋 概述

用户提供选题后，自动完成以下任务：
1. 判断视频类型（知识分享/生活感悟）
2. 确定目标平台和时长规格
3. 搜索/加载知识干货文档
4. 匹配相关商品（软植入）
5. 生成 **分镜脚本**（含配图 Prompt）
6. 生成 **逐字稿**（含场景标注）
7. 调用 API 生成分镜配图
8. 保存所有文件

---

## ⚙️ 配置信息

### API 配置
```
# 云雾 API（图片生成 - 快速出图）
端点: https://yunwu.ai/v1
模型: gemini-3-pro-image-preview
API Key: sk-UqMsXIWjukWom3cHPkbf5xBqYrnEJHz3J7cdQQNhkFg974X5

# MidJourney API（高质量真实场景 - v1.1 新增）
平台: DeepRouter
端点: https://deeprouter.top
API Key: sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I
```

### 路径配置
```
# 知识干货库
知识库路径: /Users/dj/Documents/slowseasons AI工厂/内容生产/notebook lm干货稿/

# 商品库
商品库: /Users/dj/Documents/slowseasons AI工厂/商品库/商品数据.xlsx

# 输出根路径
输出路径: /Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/视频脚本/

# 输出文件结构
```
/视频脚本/
└── 2026-01-25_春节花园改造/              # 必须创建文件夹（去掉_视频后缀）
    ├── 2026-01-25_春节花园改造_分镜脚本.md
    ├── 2026-01-25_春节花园改造_逐字稿.md
    └── images/
        ├── 01_开场.png
        ├── 02_知识点1.png
        └── ...
```

**发布后管理：**
```
发布完成后，将整个文件夹移动到：
/视频脚本/已发布/2026-01-25_春节花园改造/
```
```

### 配图尺寸
- **竖版（小红书/抖音）**: 9:16 (1080×1920)
- **横版（视频号/快手）**: 16:9 (1920×1080)
- **默认**: 9:16 竖版

---

## 🎯 内容策略核心（v2.0 新增）

### 3秒-30秒-3分钟法则

| 时间节点 | 作用 | 关键点 |
|----------|------|--------|
| **前3秒** | 抓住注意力 | 决定用户是否停留 |
| **前30秒** | 建立信任 | 决定用户是否继续看 |
| **3分钟** | 完成转化 | 决定用户是否购买/关注 |

### 开头公式（视频版）

| 类型 | 口播模板 | 视频示例 |
|------|----------|----------|
| **痛点共鸣型** | "你是不是也有这个困扰？[痛点]别担心，今天教你..." | "诶，你的绿萝是不是也这样黄叶了？" |
| **好奇悬念型** | "你知道吗？[反常识]其实真相是..." | "你知道吗？90%的人养绿萝都犯这个错..." |
| **故事代入型** | "我之前也是这样...[经历]直到我发现了..." | "我第一次养绿萝，也是各种黄叶烂根..." |

### 吸引点设计技巧

1. **使用对比**：分镜展示 ❌错误做法 vs ✅正确做法
2. **使用数字**：“记住这3点”、“5种植物”
3. **场景化描述**："想象一下，你下班回家，看到客厅的绿萝绿油油的..."
4. **金句收尾**：每个知识点用一句话总结

---

## 🎯 两种视频类型

### 类型一：知识分享类 📚

| 维度 | 规格 |
|------|------|
| **定位** | 干货输出、深度知识 |
| **时长** | 2-5分钟（中长视频） |
| **分镜数** | 10-20个 |
| **结构** | 钩子→问题引出→知识点1→知识点2→知识点3→总结→CTA |
| **特点** | 信息密度大、一环扣一环、让人想听到最后 |
| **适用选题** | 新手必知误区、养护全攻略、原理讲解、对比测评 |

**识别关键词：**
- 教程、技巧、方法、步骤、原理
- 误区、避坑、必知、全攻略
- 对比、测评、选购指南

---

### 类型二：生活感悟类 🌿

| 维度 | 规格 |
|------|------|
| **定位** | 情感共鸣、人生哲学 |
| **时长** | 30秒-2分钟（短中视频） |
| **分镜数** | 5-12个 |
| **结构** | 场景切入→故事/细节→情感升华→共鸣收尾 |
| **特点** | 植物×人生哲学、治愈、反人类观点、情绪价值 |
| **适用选题** | 养花与人生、生活小感悟、治愈时刻、反常识观点 |

**识别关键词：**
- 感悟、人生、生活、治愈
- 反思、发现、原来、突然
- 慢下来、等待、陪伴

---

## 🎨 四平台适配

| 平台 | 图标 | 时长偏好 | 节奏 | 话术风格 | 特有元素 |
|------|------|----------|------|----------|----------|
| 小红书 | 🔴 | 1-3分钟 | 紧凑、信息密集 | 姐妹感、亲切口语 | 金句截图、字幕密集 |
| 视频号 | 🟣 | 1-5分钟 | 中等、品质感 | 娓娓道来、有调性 | 私域引导、公众号联动 |
| 快手 | 🟡 | 30秒-3分钟 | 直接、接地气 | 真实朴素、体验感 | 实用性强、老铁感 |
| 抖音 | 🔵 | 15秒-1分钟 | 快节奏、强钩子 | 活泼潮流、网感 | 热点结合、开头炸裂 |

### 平台适配规则

**默认行为：**
- 未指定平台 → 生成通用版本（可多平台发布）
- 通用版取中间值：节奏适中、话术亲切但不过度口语化

**指定平台后：**
- 开头钩子按平台风格调整
- 节奏快慢按平台偏好调整
- 话术风格按平台调性适配
- 时长建议按平台规范

---

## 🔄 执行流程

### Step 1: 解析输入

**输入解析规则：**

| 输入类型 | 示例 | 处理方式 |
|----------|------|----------|
| 明确选题 | "新手养绿萝的5个误区" | 直接使用 |
| 模糊主题 | "关于浇水" | 细化为具体选题 |
| 带类型指定 | "知识分享视频：多肉配土" | 使用指定类型 |
| 带平台指定 | "抖音短视频：3秒学会浇水" | 按平台适配 |
| 纯主题词 | "绿萝" | 智能判断类型并生成选题 |

**类型判断逻辑：**
```
IF 包含 [教程/技巧/方法/误区/攻略/原理/对比] THEN
    类型 = 知识分享类
ELSE IF 包含 [感悟/人生/治愈/发现/慢/等待/陪伴] THEN
    类型 = 生活感悟类
ELSE
    默认 = 知识分享类（更通用）
```

**时长确定：**
```
知识分享类：
  - 单一知识点 → 短视频（1-2分钟）→ 8-12分镜
  - 系统知识 → 中长视频（3-5分钟）→ 15-20分镜

生活感悟类：
  - 默认 → 短视频（30秒-1分钟）→ 5-8分镜
  - 完整故事 → 中视频（1-2分钟）→ 8-12分镜
```

---

### Step 2: 知识加载

**搜索优先级：**

1. **本地干货库**：`/notebook lm干货稿/`
   - 匹配规则：文件名或内容包含选题关键词
   - 如匹配到 → 提取相关知识点

2. **网络搜索**（无匹配时）：
   - 使用 `search_web` 搜索可靠知识
   - 搜索关键词：`[选题] 专业知识 养护方法`
   - 将搜索结果整理后保存至干货库

**知识提取要点：**
- 核心知识点（3-5个）
- 常见误区（1-3个）
- 实操步骤（按需）
- 背后原理（可选）

---

### Step 3: 商品库匹配

**调用 product-catalog 匹配商品：**

```python
import pandas as pd

PRODUCT_EXCEL = "/Users/dj/Documents/slowseasons AI工厂/商品库/商品数据.xlsx"

def match_products(keywords, max_results=2):
    df = pd.read_excel(PRODUCT_EXCEL)
    df = df[df['商品状态'] == '销售中']
    
    scored = []
    for _, row in df.iterrows():
        score = 0
        text = f"{row['商品名称']} {row['商品分组']} {row['商品卖点']}"
        for kw in keywords:
            if kw in text:
                score += 1
                if kw in str(row['商品名称']):
                    score += 2
        if score > 0:
            scored.append((score, row))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scored[:max_results]]
```

**植入策略：**

| 视频类型 | 商品数量 | 植入方式 |
|----------|----------|----------|
| 知识分享类 | 1-2个 | 在相关知识点处自然提及 |
| 生活感悟类 | 0-1个 | 片尾轻描淡写或不植入 |

**软植入话术模板：**
- "我自己用的是这款[商品名]，效果还不错"
- "很多姐妹问我用什么，其实[商品名]就够用了"
- "顺便说一下，评论区有链接"

---

### Step 4: 生成分镜脚本

**分镜脚本结构：**

每个分镜包含以下字段：

| 字段 | 说明 |
|------|------|
| 分镜序号 | 01, 02, 03... |
| 时长 | 该分镜预计秒数 |
| 画面内容 | 画面描述（用于生成配图/指导拍摄） |
| 镜头提示 | 镜头语言（近景/远景/特写/转场） |
| 配图Prompt | 用于 AI 生成配图的英文 Prompt |
| 口播要点 | 该分镜对应的口播核心内容 |

**知识分享类分镜模板：**

| 分镜 | 时长 | 内容类型 |
|------|------|----------|
| 01 | 3-5秒 | 钩子开场（痛点/反问/惊讶） |
| 02 | 5-8秒 | 问题引出/背景铺垫 |
| 03-05 | 各15-30秒 | 知识点1（核心干货） |
| 06-08 | 各15-30秒 | 知识点2（深入/对比） |
| 09-11 | 各15-30秒 | 知识点3（实操/避坑） |
| 12 | 5-10秒 | 总结金句 |
| 13 | 5-8秒 | CTA引导（关注/评论） |

**生活感悟类分镜模板：**

| 分镜 | 时长 | 内容类型 |
|------|------|----------|
| 01 | 3-5秒 | 场景切入（氛围画面） |
| 02-03 | 各5-10秒 | 故事/细节展开 |
| 04-05 | 各5-10秒 | 情感铺垫 |
| 06 | 5-10秒 | 哲理升华（金句） |
| 07 | 3-5秒 | 共鸣收尾 |

---

### Step 5: 生成逐字稿

**⚠️ 重要：逐字稿 ≠ 分镜要点提取**

**逐字稿的正确定义：**
- 逐字稿是**完整的口播内容**，每一个字都要写出来
- 是在分镜要点基础上**扩展和丰富**的完整表达
- 包含自然的过渡、连接、解释和情感表达
- **不包含**场景标注（如 `[看镜头]`、`[画外音]` 等，这些属于分镜脚本）

**错误示例（只是要点提取）：**
```
第一个道理：不是所有付出都要立刻看到回报
```

**正确示例（完整逐字稿）：**
```
第一个道理，就是不是所有的付出，都要立刻看到回报。

你看，你每天给它浇水，每天看着它，可能一个月过去了，它还是那样，一动不动的。你都开始怀疑了，是不是自己哪里做错了，是不是水浇多了，还是光照不够。

但其实呢，它不是不长，它只是在积蓄力量。

然后某一天，你突然发现，诶，它冒出新芽了！那一刻你就明白了，原来它一直在努力，只是需要时间。
```

**逐字稿特点：**

1. **完整性**：每一个要说的字都写出来，不是大纲或要点
2. **口语化**：像跟朋友聊天，保留语气词（呢、啊、诶）
3. **自然流畅**：有过渡、有连接、有情感递进
4. **可直接朗读**：拿起来就能照着说，不需要再加工

**口语化技巧：**
- 短句为主，每句≤20字
- 保留语气词：诶、嘛、呢、啊
- 有情绪起伏：惊讶→平静→强调
- 适当反问/设问
- 自然停顿和重复

**逐字稿模板示例：**
```
[看镜头] 诶，你是不是也觉得绿萝特别好养？

[转头，看向植物] 但其实很多人都踩了这几个坑...

[展示画面] 你看这盆，叶子发黄就是因为...

[画外音] 正确的做法应该是...

[看镜头] 记住这三个字就够了：干透浇透

[停顿1秒] 

[看镜头，微笑] 好啦，我是小静，下期见~
```

---

### Step 6: 生成分镜配图

**调用云雾 API 生成图片：**

```python
import requests
import base64
import os
import re

def generate_image_yunwu(prompt: str, output_path: str):
    """使用云雾 API 生成图片"""
    url = "https://yunwu.ai/v1/chat/completions"
    
    headers = {
        "Authorization": "Bearer sk-UqMsXIWjukWom3cHPkbf5xBqYrnEJHz3J7cdQQNhkFg974X5",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gemini-3-pro-image-preview",
        "messages": [
            {"role": "user", "content": f"Generate an image: {prompt}"}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        match = re.search(r"data:image/\w+;base64,([^)]+)", content)
        if not match:
            print(f"❌ 未能在响应中找到图片数据")
            return False
            
        image_data = match.group(1)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_data))
        
        print(f"✅ 图片已保存: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 图片生成失败: {e}")
        return False
```

**配图 Prompt 规范：**

```
A [比例] photograph/illustration in [风格] style.
Scene: [场景描述]
Subject: [主体]
Lighting: [光线]
Mood: [情绪]
Color palette: Muted Morandi colors, low saturation.
Style: [风格补充]
NO TEXT. NO WORDS. NO LETTERS.
```

**视频配图风格选择：**

| 视频类型 | 推荐风格 | 推荐 API | 说明 |
|----------|----------|----------|------|
| 知识分享类 | dreamy-photo / cozy-sketch | 云雾 API | 真实感教程感 |
| 生活感悟类 | soft-botanical | 云雾 API | 柔和治愈氛围 |
| 植物家居场景 | realistic-lifestyle | **MidJourney** | 更逼真的人物植物互动 |

---

### Step 6.5: 生成4个平台封面（v2.1 新增）📱

> **重要**：每个视频脚本需要生成4个不同平台的封面，适配各平台风格

**平台封面配置：**

| 平台 | 尺寸 | 风格特点 | 文件命名 |
|------|------|----------|----------|
| 视频号 | 16:9 (1920×1080) | 品质感、调性、私域导流 | `cover_视频号.png` |
| 抖音 | 9:16 (1080×1920) | 爆款、娱乐、短平快 | `cover_抖音.png` |
| 快手 | 9:16 (1080×1920) | 实用、接地气、真实感 | `cover_快手.png` |
| 小红书 | 3:4 (1080×1440) | 种草、教程、生活方式 | `cover_小红书.png` |

**Prompt 差异化策略：**

```python
def generate_platform_covers(base_prompt: str, topic_title: str):
    """
    为4个平台生成差异化封面
    
    参数:
        base_prompt: 基础场景描述
        topic_title: 选题标题
    """
    covers = {}
    
    # 视频号：品质感、调性
    covers['视频号'] = {
        'prompt': f\"{base_prompt}, elegant composition, premium quality, "
                  f"sophisticated lighting, refined aesthetic, "
                  f"professional lifestyle photography --ar 16:9 --v 6.1\",
        'size': '16:9',
        'filename': 'cover_视频号.png'
    }
    
    # 抖音：爆款、娱乐
    covers['抖音'] = {
        'prompt': f\"{base_prompt}, vibrant colors, dynamic composition, "
                  f"eye-catching visual, trendy aesthetic, "
                  f"energetic mood --ar 9:16 --v 6.1\",
        'size': '9:16',
        'filename': 'cover_抖音.png'
    }
    
    # 快手：实用、接地气
    covers['快手'] = {
        'prompt': f\"{base_prompt}, authentic feel, relatable scene, "
                  f"practical demonstration, down-to-earth aesthetic, "
                  f"warm natural lighting --ar 9:16 --v 6.1\",
        'size': '9:16',
        'filename': 'cover_快手.png'
    }
    
    # 小红书：种草、教程
    covers['小红书'] = {
        'prompt': f\"{base_prompt}, lifestyle aesthetic, tutorial vibe, "
                  f"clean composition, aspirational yet achievable, "
                  f"soft natural lighting --ar 3:4 --v 6.1\",
        'size': '3:4',
        'filename': 'cover_小红书.png'
    }
    
    return covers
```

**生成流程：**
1. 基于选题生成基础场景描述
2. 为每个平台添加差异化关键词
3. 调用 MidJourney API 生成4张封面
4. 保存到 `images/` 文件夹，按平台命名

---

### Step 6.6: 生成分镜配图

**⚠️ 推荐用于：植物家居类、生活场景类、需要人物出镜的配图**

#### MidJourney API 配置

```python
# DeepRouter Midjourney API
API_BASE_URL = "https://deeprouter.top"
API_KEY = "sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I"
```

#### 集成代码

```python
import sys
sys.path.append('/Users/dj/Desktop/小静的skills/xiaohongshu-content-generator/scripts')
from deeprouter_mj_api import DeepRouterMJ

# 初始化 API
api = DeepRouterMJ("sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I")

# 生成图片
task_id = api.submit_imagine(prompt)
image_url = api.wait_for_result(task_id, max_wait=300)
api.download_image(image_url, output_path)
```

#### 视频配图 Prompt 模板

**适用场景：植物养护、生活感悟类视频的分镜配图**

```
bright modern living room corner with natural plant collection,
white phalaenopsis orchids in ceramic pots on wooden shelf,
large monstera deliciosa and boston ferns on floor near window,
trailing pothos in woven basket hanging from shelf,
plants arranged at accessible heights with varied textures,
an Asian woman with long black hair, wearing cream linen dress,
standing with back to camera, gently touching plant leaves,
soft golden hour sunlight through sheer white curtains,
warm peachy tones, clean minimalist interior,
lifestyle photography, natural authentic feel, slightly dreamy,
professional but lived-in atmosphere --v 6.1 --ar 9:16
```

#### 场景统一性方案（同一视频多张配图）

**使用 --seed 参数保持场景一致：**

```python
# 第一张图生成后，手动指定 seed
base_prompt = "living room with plants, Asian woman..."
seed = 12345  # 固定 seed 值

# 所有配图使用相同 seed
prompt_01 = f"{base_prompt}, wide shot --seed {seed} --v 6.1 --ar 9:16"
prompt_02 = f"{base_prompt}, close-up of hands touching leaves --seed {seed} --v 6.1 --ar 9:16"
prompt_03 = f"{base_prompt}, different angle --seed {seed} --v 6.1 --ar 9:16"
```

#### API 选择策略（与小红书 Skill 统一）

**判断逻辑（参考 image-prompt-guide.md v3.0）：**
```python
def need_person(topic_title):
    """判断选题是否需要人物"""
    # 需要人物的关键词
    person_keywords = ["生活", "日常", "氛围", "治愈", "陪伴", "我的", "分享"]
    # 不需要人物的关键词（优先判断）
    no_person_keywords = ["推荐", "必买", "养护", "教程", "方法", "技巧", "避坑"]
    
    if any(kw in topic_title for kw in no_person_keywords):
        return False
    if any(kw in topic_title for kw in person_keywords):
        return True
    return False  # 默认不需要人物
```

| 配图类型 | 推荐 API | 原因 |
|----------|----------|------|
| 手绘/插画风 | 云雾 API（Gemini） | 更快、风格稳定 |
| **真实场景/人物** | **MidJourney** | 更逼真、质感好 |
| 信息图/图解 | 云雾 API | 支持中文标注 |
| 纯植物/产品特写 | 云雾 API | 单张完整图 |

**⚠️ 人物图片生成策略（v2.1 重要更新）：**

**禁止使用正脸镜头：**
- ❌ 不要生成人物正面看镜头的图片
- ❌ 不要生成清晰的面部特写
- ❌ AI 生成的正脸人物太完美、不真实、一致性差

**推荐使用的角度：**
- ✅ **背影**：人物背对镜头，看向窗外/植物
- ✅ **侧脸/侧身**：人物侧面，不看镜头
- ✅ **手部特写**：只拍手和植物的互动
- ✅ **远景**：人物在场景中，面部不清晰
- ✅ **局部**：肩膀、手臂、衣角等局部

**Prompt 示例（避免正脸）：**
```
# 背影
back view of Asian woman with long black hair,
standing by window looking at plants outside,
wearing cream linen dress, natural home setting

# 侧脸（不看镜头）
side profile of Asian woman,
looking down at plant in her hands,
soft natural light, contemplative mood

# 手部特写
close-up of hands gently touching green plant leaves,
delicate fingers, natural caring gesture,
no face visible

# 远景
wide shot of living room,
small figure of woman near window with plants,
face not clearly visible, atmospheric shot
```

**原因：**
1. 避免 AI 生成人脸的"太完美"问题
2. 提升真实感和生活感
3. 解决多张图人物一致性问题
4. 更符合纪实摄影风格

---

### Step 7: 保存输出

**文件夹结构：**

```
/视频脚本/
└── 2026-01-14_[选题名]_[平台]/
    ├── 2026-01-14_[选题名]_分镜脚本.md
    ├── 2026-01-14_[选题名]_逐字稿.md
    ├── images/
    │   ├── 01_开场.png
    │   ├── 02_知识点A.png
    │   ├── 03_知识点B.png
    │   └── ...
    └── README.md  # 项目概览（可选）
```

**文件命名规则：**
- 日期格式：YYYY-MM-DD
- 选题名：简短（≤10字）
- 平台：小红书/视频号/快手/抖音/通用

---

## 📄 输出模板

### 分镜脚本模板

```markdown
# 🎬 分镜脚本

> 📅 生成时间：[YYYY-MM-DD HH:mm]
> 📹 视频类型：知识分享类 / 生活感悟类
> ⏱️ 预计时长：[X分X秒]
> 🎯 目标平台：[平台名称]
> 🏷️ 选题：[选题名称]

---

## 分镜列表

| 序号 | 时长 | 画面内容 | 镜头 | 口播要点 |
|------|------|----------|------|----------|
| 01 | 5秒 | [画面描述] | 中景/看镜头 | [要点] |
| 02 | 8秒 | [画面描述] | 特写 | [要点] |
| ... | ... | ... | ... | ... |

---

## 分镜详情

### 分镜 01：开场钩子
- **时长**：5秒
- **画面**：[详细画面描述]
- **镜头**：中景，人物居中，看镜头
- **配图提示**：[展示画面时的配图 Prompt]

### 分镜 02：...
...

---

## 配图 Prompt 汇总

| 分镜 | Prompt |
|------|--------|
| 01 | A 9:16 photograph in dreamy-photo style... |
| 02 | A 9:16 photograph in dreamy-photo style... |
| ... | ... |

---

## 商品植入点

| 分镜 | 商品 | 植入方式 |
|------|------|----------|
| 05 | [商品名] | 自然提及 |
| 10 | - | 评论区引导 |
```

---

### 逐字稿模板

```markdown
# 📝 逐字稿

> 📅 生成时间：[YYYY-MM-DD HH:mm]
> 📹 视频类型：知识分享类 / 生活感悟类
> ⏱️ 预计时长：[X分X秒]
> 🎯 目标平台：[平台名称]
> 🏷️ 选题：[选题名称]

---

## 完整逐字稿（[N]段，对应[N]个分镜）

[第1段完整口播内容，对应分镜01...]

[第2段完整口播内容，对应分镜02...]

[第3段完整口播内容，对应分镜03...]

...

[最后一段完整口播内容，对应最后一个分镜...]

---

## 剪映编辑对照表

| 分镜 | 时长 | 图片文件 | 字数 | 预计语速 |
|------|------|---------|------|---------|
| 01 | X秒 | 01_XXX.png | XX字 | X.X字/秒 |
| 02 | X秒 | 02_XXX.png | XX字 | X.X字/秒 |
| ... | ... | ... | ... | ... |

---

## 语速说明

- **平均语速**：约 XXX 字/分钟（X-X 字/秒）
- **适合场景**：[视频类型]，[节奏描述]
- **停顿**：段落之间自然停顿 0.5-1 秒

---

## 剪映编辑步骤

1. **导入 [N] 张图片**（按顺序 01-[N]）
2. **设置每张图片的时长**（见对照表）
3. **录制音频**：
   - 按照 [N] 段逐字稿录制
   - 控制语速在 X-X 字/秒
   - 段落之间自然停顿
4. **音画对齐**：每段音频对应一张图片
5. **微调时长**：根据实际音频长度调整

---

## 备注

- 这是扩充版逐字稿，按 [N] 个分镜组织
- 每段字数已匹配时长（X-X 字/秒）
- 可以根据实际录音情况微调
```

**⚠️ 逐字稿格式要求（v2.2 重要更新）：**

1. **禁止添加场景标注**：
   - ❌ 不要添加 `[看镜头]`、`[画外音]`、`[展示画面]` 等标注
   - ❌ 不要添加 `【开场】`、`【第一部分】` 等章节标题
   - ✅ 场景标注属于分镜脚本，不属于逐字稿

2. **禁止添加分镜标题**：
   - ❌ 不要添加 `### 分镜 01（8秒）- 窗台绿植晨光`
   - ❌ 不要添加 `---` 分隔线
   - ✅ 直接输出纯文本段落，段落之间用空行分隔

3. **正确格式**：
   - ✅ 每个段落对应一个分镜
   - ✅ 段落之间用一个空行分隔
   - ✅ 方便用户直接复制粘贴到剪映等视频编辑软件
   - ✅ 用户工作流：12张图片 + 12段音频 + 12段文本

**错误示例：**
```markdown
### 分镜 01（8秒）- 窗台绿植晨光

[看镜头] 养花这件事呢，教会了我很多。

---

### 分镜 02（10秒）- 手轻抚叶片

[画外音] 第一个道理，就是...
```

**正确示例：**
```markdown
## 完整逐字稿（12段，对应12个分镜）

养花这件事呢，教会了我很多。第一个道理，就是不是所有的付出，都要立刻看到回报。

你看，你每天给它浇水，每天看着它，可能一个月过去了，它还是那样，一动不动的。

你都开始怀疑了，是不是自己哪里做错了，是不是水浇多了，还是光照不够。但其实呢，它不是不长，它只是在积蓄力量。

...
```

---

## ✅ Good Case（正确示例）

**用户输入：**
```
帮我写一个视频脚本，选题是：新手养绿萝的3个致命误区
```

**正确执行：**
1. ✅ 识别类型：知识分享类（包含"误区"关键词）
2. ✅ 确定规格：短中视频（单一知识点）→ 2分钟 → 10-12分镜
3. ✅ 搜索干货库，提取绿萝养护知识
4. ✅ 匹配商品：营养土/喷壶等
5. ✅ 生成分镜脚本（含配图 Prompt）
6. ✅ 生成逐字稿（口语化 + 场景标注）
7. ✅ 调用 API 生成10-12张配图
8. ✅ 保存至 `/视频脚本/2026-01-14_绿萝误区_通用/`

---

## ❌ Anti-Patterns（禁止行为）

**禁止示例1：中途询问**
```
❌ "请问您想要知识分享类还是生活感悟类？"
❌ "视频时长您希望多长？"
```
→ 应根据选题关键词自动判断

**禁止示例2：逐字稿太书面**
```
❌ "绿萝是一种常见的室内观叶植物，其养护需要注意以下几点..."
```
→ 应改为 "诶，绿萝你肯定养过对吧？但这几个坑你可能踩了..."

**禁止示例3：分镜不完整**
```
❌ 只有画面描述，没有镜头提示
❌ 只有口播内容，没有时长
```
→ 每个分镜必须包含完整6个字段

**禁止示例4：配图风格不统一**
```
❌ 分镜01用dreamy-photo，分镜02用cozy-sketch
```
→ 同一视频所有配图风格必须统一

---

## 🛠️ 错误处理

| 场景 | 处理方式 |
|------|----------|
| 选题模糊 | 自动细化为具体选题 |
| 干货库无匹配 | 网络搜索后存入本地 |
| 无法判断类型 | 默认知识分享类 |
| 商品无匹配 | 跳过商品植入 |
| 配图生成失败 | 跳过该图，继续其他图 |
---

## 📁 临时文件管理（v2.0 新增）

**规则：**
- ✅ 所有测试/临时文件必须保存到专属临时文件夹
- ✅ 临时文件夹路径：`[选题文件夹]/.tmp/`
- ✅ 任务完成后自动清理
- ❌ 禁止临时文件散落在工作目录中

**临时文件目录结构：**
```
/视频脚本/2026-01-14_[选题名]_[平台]/
├── 2026-01-14_[选题名]_分镜脚本.md   # 正式输出
├── 2026-01-14_[选题名]_逐字稿.md     # 正式输出
├── images/                                # 分镜配图
└── .tmp/
    ├── test_*.png                         # 测试图片
    ├── draft_*.md                         # 草稿文件
    └── search_cache_*.json               # 搜索缓存
```

---

## 🔗 与其他技能联动

| 技能 | 触发场景 | 关系 |
|------|----------|------|
| `product-catalog` | 商品匹配 | 依赖 |
| `knowledge-extractor` | 知识提取 | 可选 |
| `topic-discovery` | 选题推荐 | 上游 |
| `xiaohongshu-content-generator` | 同选题生成图文 | 并行 |

---

## 📚 知识库引用

- [video-script-templates.md](knowledge/video-script-templates.md) - 脚本结构模板
- [platform-adaptation-guide.md](knowledge/platform-adaptation-guide.md) - 平台适配指南
- [image-prompt-guide.md](file:///Users/dj/Desktop/小静的skills/xiaohongshu-content-generator/knowledge/image-prompt-guide.md) - **配图 Prompt 统一规范 v3.0**（来自小红书 Skill）

---

## 📝 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.2 | 2026-01-17 | **逐字稿格式优化**：移除分镜标题和场景标注，改为纯文本段落格式，方便复制粘贴到剪映 |
| v2.1 | 2026-01-14 | **修复**：MidJourney API 脚本路径修正、添加统一 image-prompt-guide.md 引用 |
| v2.0 | 2026-01-14 | **内容策略整合**：3秒-30秒-3分钟法则、开头公式、吸引点设计技巧、临时文件管理 |
| v1.1 | 2026-01-14 | **MidJourney API 集成**：DeepRouter 平台、场景统一方案 |
| v1.0 | 2026-01-14 | 初始版本：双类型、四平台、分镜+逐字稿 |
