# 小红书配图生成指南 v4.0

> 本文档是小红书配图生成的**唯一规范**，定义工具选择、风格模板和 Prompt 结构。
> **核心原则**：同一选题6张图风格统一，不同选题风格可切换。

---

## 🌸 小红书审美调性（v4.0 核心更新）

> ⚠️ **这是所有配图生成的前置约束，必须优先于其他规则执行！**

### 小红书用户偏好的视觉风格

小红书用户追求的是**高级感、生活化、真实感**，而非商品展示图。

| 风格类型 | 特点 | 适用场景 |
|---------|------|---------|
| **ins 风** | 低饱和度、柔和光线、留白多 | 生活场景、居家布置 |
| **日系风** | 温暖色调、自然光、胶片质感 | 日常记录、治愈系 |
| **侘寂风** | 极简、素雅、自然材质 | 高端感、品质生活 |
| **奶油风** | 奶白色调、柔和、温馨 | 家居、温馨场景 |

### 🎨 颜色控制规则（必须严格遵守）

#### ✅ 正确的颜色表达

| 原始颜色 | 小红书调性替换词 | 说明 |
|---------|----------------|------|
| 红色 | `dusty coral`, `muted rose`, `terracotta red`, `desaturated crimson` | 避免正红色 |
| 粉色 | `blush pink`, `dusty pink`, `muted salmon` | 避免荧光粉 |
| 橙色 | `burnt sienna`, `muted peach`, `soft terracotta` | 避免鲜橙色 |
| 黄色 | `cream yellow`, `muted gold`, `soft honey` | 避免亮黄色 |
| 绿色 | `sage green`, `eucalyptus`, `muted olive` | 避免荧光绿 |

#### ❌ 禁止的颜色表达

```
禁止词汇（会导致高饱和度/假感）：
- bright red, vivid red, pure red
- hot pink, neon pink, fuchsia
- bright orange, vivid yellow
- neon green, lime green
- any "bright", "vivid", "neon", "pure" color descriptors
```

### 📸 真实感强制约束

**每个 Prompt 必须包含以下约束词之一：**

```
# 真实感约束（选择1-2个添加到每个 Prompt）
- "authentic home environment"
- "lived-in atmosphere"
- "natural imperfections"
- "realistic indoor lighting"
- "lifestyle photography feel"
- "not a studio shot"
```

**每个 Prompt 必须包含以下颜色约束：**

```
# 颜色约束（必须添加）
- "desaturated color palette"
- "muted tones throughout"
- "low saturation, high-end aesthetic"
- "Morandi color scheme"
```

### 🚫 反例 Prompt（必须避免）

#### ❌ 错误示例 1：商品展示风

```
❌ 错误 Prompt:
A beautiful red amaryllis flower in a white pot, 
bright studio lighting, product photography, 
clean white background, vibrant red petals.

问题：
- "bright studio lighting" → 商品图质感
- "product photography" → 不是生活图
- "vibrant red" → 颜色过饱和
- "clean white background" → 缺少生活场景
```

#### ✅ 正确示例 1：生活化

```
✅ 正确 Prompt:
A dusty coral amaryllis in a cream ceramic pot,
placed on a wooden windowsill in a cozy living room,
soft natural morning light, lived-in atmosphere,
muted Morandi color palette, low saturation,
realistic lifestyle photography, film-like quality.
NO TEXT. NO WORDS. NO PEOPLE.
```

#### ❌ 错误示例 2：过于艳丽的年宵花

```
❌ 错误 Prompt:
Bright red Chinese New Year flowers including 
vivid pink cyclamen and orange kalanchoe,
colorful festive arrangement, 
red lanterns, pure gold decorations.

问题：
- "bright red", "vivid pink" → 饱和度过高
- "colorful" → 会生成杂乱的高饱和图
- "pure gold" → 太假
```

#### ✅ 正确示例 2：高级感年宵花

```
✅ 正确 Prompt:
Elegant Chinese New Year floral arrangement,
dusty coral amaryllis and muted rose cyclamen,
soft terracotta kalanchoe blooms,
placed in blue-and-white porcelain vases,
natural window light, cream and wood tones room,
subtle red paper decorations in background,
desaturated festive atmosphere, understated luxury,
Morandi color palette, lifestyle photography.
NO TEXT. NO WORDS. NO PEOPLE.
```

### 🔄 Prompt 生成检查清单

每个 Prompt 生成后，必须检查：

- [ ] 是否包含饱和度控制词（`muted`, `desaturated`, `dusty`）？
- [ ] 是否避免了禁止词汇（`bright`, `vivid`, `neon`）？
- [ ] 是否包含真实感约束（`lived-in`, `natural light`）？
- [ ] 是否有生活化场景（不是纯白背景/棚拍）？
- [ ] 红色系是否使用替代词（`dusty coral`, `terracotta`）？

---

## 🚨 工具选择决策树（必须首先判断）

### 核心规则

```
┌─────────────────────────────────────────────────────┐
│                  选题是否需要人物？                    │
└─────────────────────────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          ▼                              ▼
    ❌ 不需要人物                    ✅ 需要人物
          │                              │
          ▼                              ▼
   ┌─────────────┐               ┌─────────────┐
   │  Gemini API │               │ Midjourney  │
   │  (云雾端点)  │               │   API       │
   └─────────────┘               └─────────────┘
```

### 人物判断规则

| 选题类型 | 是否需要人物 | 使用工具 | 判断依据 |
|---------|-------------|---------|---------|
| **产品展示类** | ❌ 不需要 | Gemini | 纯产品/植物特写 |
| **养护教程类** | ❌ 不需要 | Gemini | 重点是植物本身 |
| **科普知识类** | ❌ 不需要 | Gemini | 信息图、图解 |
| **场景布置类** | ✅ 需要 | Midjourney | 人与植物的互动 |
| **生活方式类** | ✅ 需要 | Midjourney | 需要生活氛围感 |
| **使用场景类** | ✅ 需要 | Midjourney | 展示真实使用场景 |

### 关键词判断逻辑

```python
def need_person(topic_title):
    """判断选题是否需要人物"""
    # 需要人物的关键词
    person_keywords = [
        "生活", "日常", "氛围", "治愈", "陪伴",
        "我的", "分享", "vlog", "记录", "打造"
    ]
    
    # 不需要人物的关键词（优先判断）
    no_person_keywords = [
        "推荐", "必买", "种类", "品种", "养护",
        "教程", "方法", "技巧", "避坑", "选购"
    ]
    
    # 优先判断不需要人物
    if any(kw in topic_title for kw in no_person_keywords):
        return False
    
    # 再判断需要人物
    if any(kw in topic_title for kw in person_keywords):
        return True
    
    # 默认不需要人物
    return False

def select_tool(topic_title):
    """根据选题选择生成工具"""
    if need_person(topic_title):
        return "Midjourney"
    else:
        return "Gemini"
```

### 示例判断

| 选题 | 是否需要人物 | 工具 |
|------|-------------|------|
| 「春季必买！这8种开花植物颜值爆表」 | ❌ | Gemini |
| 「绿植养护避坑指南」 | ❌ | Gemini |
| 「我的阳台花园改造记」 | ✅ | Midjourney |
| 「和植物一起的治愈生活」 | ✅ | Midjourney |

---

## 🎨 第一部分：Gemini API 风格模板（无人物场景）

### 风格选择规则

| 选题类型 | 风格 | 说明 |
|---------|------|------|
| **场景类**（居家、装饰、旅行） | dreamy-photo | 真实感、实拍感、自然光、柔焦 |
| **教程类**（方法、步骤、技巧） | cozy-sketch | 手绘涂鸦感、可配中文标注 |
| **科普类**（知识、原理、对比） | infographic-sketch | 信息图风格、手绘+图解 |
| **情感类**（心情、感悟、治愈） | soft-botanical | 柔和水彩、植物插画、氛围感 |
| **产品类**（推荐、测评、好物） | minimal-collage | 极简拼贴、突出主体 |

### ⚠️ 关键规则
1. **同一选题的6张配图必须使用相同风格**
2. **不同选题之间切换风格**，确保主页视觉多样性
3. **风格轮换记录**：记住上一次使用的风格，下次自动切换

---

### 🌅 dreamy-photo（梦幻实拍风）

**适用**：场景类、生活类、居家装饰（无人物版本）

**特点**：
- 真实感、实拍质感
- 柔焦、暖色调、自然光
- 莫兰迪色系、低饱和度
- 有温度的生活场景

**Prompt 模板**：
```
A 3:4 photograph in dreamy realistic style.
Scene: [具体场景描述], authentic home environment, lived-in atmosphere.
Lighting: Soft natural window light, warm golden hour glow, gentle shadows.
Details: [场景细节元素]
Mood: [情绪关键词], cozy, inviting.
Color palette: Muted Morandi colors, desaturated tones, cream and sage.
Color control: Use dusty coral instead of red, muted rose instead of pink, soft terracotta for warm accents.
Style: Realistic lifestyle photography, soft focus, film-like quality, NOT product photography.
NO TEXT. NO WORDS. NO LETTERS. NO PEOPLE. NO STUDIO LIGHTING.
```

---

### ✏️ cozy-sketch（手绘涂鸦风）

**适用**：教程类、步骤类、技巧类

**特点**：
- 手绘铅笔线条 + 淡水彩
- 可包含中文标注和说明
- 生活化、有温度
- 笔记本纸张质感

**Prompt 模板**：
```
A 3:4 illustration in hand-drawn sketch style.
Subject: [主题内容]
Details: Pencil line drawings with soft watercolor washes, notebook paper texture.
Elements: [具体元素]
Annotations: Include simple Chinese text labels for key points.
Color palette: Muted beige, dusty rose, sage green watercolor accents.
Style: Cozy sketchbook aesthetic, natural imperfect lines.
```

---

### 📊 infographic-sketch（信息图手绘风）

**适用**：科普类、知识类、对比类

**特点**：
- 信息可视化结构
- 手绘涂鸦感 + 图标
- 中文文字说明
- 清晰的信息层级

**Prompt 模板**：
```
A 3:4 infographic in hand-drawn sketchnote style.
Topic: [知识主题]
Structure: [信息结构描述]
Visual elements: Icons, simple diagrams, arrows, bullet points.
Text: Include Chinese labels and brief explanations.
Background: Lined notebook paper or clean white.
Color palette: Functional colors for categorization, yellow highlighter accents, red pen circles.
Style: Educational sketchnote aesthetic.
```

---

### 🌿 soft-botanical（柔和水彩植物风）

**适用**：情感类、心情类、治愈类

**特点**：
- 柔和水彩画风
- 绿植、花卉元素
- 大量留白
- 氛围感强

**Prompt 模板**：
```
A 3:4 illustration in soft botanical watercolor style.
Subject: [情感主题相关意象]
Elements: Delicate plants, flowers, leaves, petals.
Composition: Generous white space, floating elements, dreamy arrangement.
Mood: [情绪关键词]
Color palette: Sage green, blush pink, cream white, muted earth tones.
Style: Soft watercolor with gentle brushstrokes, ethereal and calming.
NO TEXT. NO WORDS. NO LETTERS.
```

---

### 🎨 minimal-collage（极简拼贴风）

**适用**：产品类、推荐类、测评类

**特点**：
- 几何形状 + 产品/物品
- 干净背景、突出主体
- 极简构图
- 现代感

**Prompt 模板**：
```
A 3:4 illustration in minimal collage style.
Subject: [产品/物品]
Composition: Clean geometric shapes, centered subject, generous negative space.
Elements: Abstract shapes, simple shadows, product highlight.
Background: Pure white or soft neutral.
Color palette: Muted grey-green, soft taupe, clean white accents.
Style: Modern minimalist, editorial clean aesthetic.
NO TEXT. NO WORDS. NO LETTERS.
```

---

## 👩 第二部分：Midjourney 人物场景模板

> ⚠️ 仅在选题需要人物时使用 Midjourney

### 风格基础（所有人物场景共享）

```
STYLE_BASE = """
soft golden hour light, warm peachy tones,
clean minimalist aesthetic, natural authentic feel,
simple wooden plant stands and metal shelving units,
woven baskets and ceramic pots on tiered plant racks,
realistic home furniture and storage solutions,
lifestyle photography, slightly dreamy,
professional but lived-in atmosphere
--v 6.1 --ar 3:4
"""
```

### 人物设定规范

- ✅ 亚洲女性特征（长黑发、亚洲面孔）
- ✅ 背影或侧脸（面部可模糊）
- ✅ 米色/奶白色服装
- ✅ 自然动作（浇水、触摸植物）
- ⚠️ **不使用 --cref 参数**（环境为主，人物为辅）

---

### 场景痛点类模板

**封面图**：
```
realistic home scene showing [痛点场景],
[具体问题描述], cluttered/messy/problematic situation,
Asian woman in background looking concerned,
plants/items showing the problem clearly,
{STYLE_BASE}
```

**正文配图**：
```
[解决方案场景], organized and improved,
[具体改善细节], clear before-after contrast,
Asian woman demonstrating solution,
focus on the improvement,
{STYLE_BASE}
```

---

### 季节时令类模板

**封面图**：
```
[季节] atmosphere home scene,
[seasonal plants/flowers] in full bloom,
[季节特色元素],
Asian woman enjoying seasonal plants,
{STYLE_BASE}
```

**正文配图**：
```
close-up of [seasonal plant], beautiful [season] colors,
[seasonal care details], natural seasonal light,
Asian woman gently tending plants,
focus on seasonal beauty,
{STYLE_BASE}
```

---

### 生活方式类模板

**封面图**：
```
bright modern living room corner with natural plant collection,
[具体植物描述],
an Asian woman with long black hair in loose bun, wearing cream linen dress,
standing with back to camera, gently touching plant petals,
{STYLE_BASE}
```

**正文配图**：
```
[生活场景细节],
Asian woman in natural pose interacting with plants,
[动作描述: watering, arranging, admiring],
lifestyle photography, authentic feel,
{STYLE_BASE}
```

---

### 场景统一性方案（同一笔记多张图）

**方法：使用 --seed 参数保持场景一致**

```python
# 第一张图生成后，获取 seed
first_task_id = api.submit_imagine(prompt_1)
first_image_url = api.wait_for_result(first_task_id)

# 手动指定 seed 确保一致性
seed = 12345  # 固定 seed 值

# 后续图片使用相同 seed + 不同角度
prompt_2 = f"{base_prompt}, different angle --seed {seed} --v 6.1 --ar 3:4"
prompt_3 = f"{base_prompt}, close-up view --seed {seed} --v 6.1 --ar 3:4"
```

---

## 🎨 第三部分：色彩系统（所有风格通用）

### 莫兰迪色系（核心）
- **主色调**：低饱和度、雾感、柔和
- **辅助色**：奶油白、雾霾蓝、豆沙粉、鼠尾草绿、燕麦色
- **点缀色**：暖阳色、淡金色、珊瑚橘（少量提亮）

### 统一性约束
- ✅ **所有图片必须**：低饱和度、柔和光线
- ❌ **避免**：高对比度、荧光色、锐利线条

---

## ⚙️ 第四部分：技术参数

### Gemini API（云雾）

| 参数 | 值 |
|------|------|
| **端点** | https://yunwu.ai/v1 |
| **模型** | gemini-3-pro-image-preview |
| **比例** | 3:4（在 prompt 中强调） |
| **分辨率** | 1080 × 1440 px |
| **用途** | 无人物场景（产品、植物、教程图） |

### Midjourney API（DeepRouter）

| 参数 | 值 |
|------|------|
| **端点** | https://deeprouter.top |
| **版本** | --v 6.1 |
| **比例** | --ar 3:4 |
| **用途** | 人物场景（生活方式、互动场景） |
| **注意** | 必须 auto_upscale，避免返回 grid 图 |

---

## 🔄 第五部分：风格轮换策略

### 确保主页视觉多样性

为避免主页千篇一律，按以下规则轮换：

```
选题1 → dreamy-photo
选题2 → cozy-sketch
选题3 → soft-botanical
选题4 → minimal-collage
选题5 → dreamy-photo (循环)
...
```

### 智能选择优先级
1. **首先**：根据选题类型匹配最佳风格
2. **其次**：如果与上一篇风格相同，自动切换到同类型的备选风格
3. **目标**：连续3篇不重复同一风格

---

*v3.0 更新：2026-01-14 - 整合工具选择决策树，统一 Gemini 和 Midjourney 模板*
