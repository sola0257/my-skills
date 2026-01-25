# 微信公众号配图生成指南 v1.2

> ⚠️ **重要**：本文档是微信公众号配图的**唯一规范**。
>
> **公众号有两种内容格式，配图规范不同！**

---

## 📋 两种内容格式对照表

| 格式 | 触发词 | 封面图比例 | 正文配图比例 | 配图数量 |
|-----|-------|-----------|------------|---------|
| **长文** (article) | "公众号长文"、"订阅号长文" | 2.35:1 (900×383px) | 16:9 (900×506px) | 1封面 + 3正文 |
| **图文** (card) | "公众号图文"、"订阅号图文" | 3:4 (1080×1440px) | 3:4 (1080×1440px) | 1封面 + 5正文 |

> [!IMPORTANT]
> **默认格式**：未指定时默认生成**长文**（横版）
>
> **图文格式**：使用小红书的 [image-prompt-guide.md](file:///Users/dj/Desktop/%E5%B0%8F%E9%9D%99%E7%9A%84skills/xiaohongshu-content-generator/knowledge/image-prompt-guide.md) 的 3:4 模板

---

## 🚨 比例强制约束（长文格式）

### ❌ 禁止使用

```
❌ A 3:4 photograph...（这是小红书比例！）
❌ --ar 3:4（这是小红书 Midjourney 参数！）
❌ 任何竖版图片
```

### ✅ 必须使用

| 图片类型 | Prompt 开头 | 尺寸 |
|---------|------------|------|
| 封面图 | `A 2.35:1 wide banner...` | 900×383px |
| 正文配图 | `A 16:9 wide...` | 900×506px |

---

## 📐 生成前检查清单

**每次生成公众号配图前，必须确认：**

- [ ] Prompt 中包含 `2.35:1 wide banner`（封面）或 `16:9 wide`（正文）
- [ ] **没有** 使用 `3:4` 或 `--ar 3:4`
- [ ] 封面图使用 `wide banner` 关键词
- [ ] 正文配图使用 `wide` 关键词

---

## 🔤 中文文字清晰度要求（必须遵守）

> [!CRITICAL]
> **所有包含中文文字的图片必须确保文字清晰可读！**

### 强制要求

**每个包含中文文字的 prompt 必须添加以下语句：**

```
CRITICAL REQUIREMENTS:
- Use ONLY Chinese characters for ALL text - must be CLEAR and LEGIBLE
- NO English letters or words anywhere
- Text must NOT be distorted or blurry
- All Chinese text must be readable and well-formed
```

### 适用场景

- ✅ cozy-sketch 风格（教程类）- 包含中文标注
- ✅ infographic-sketch 风格（科普类）- 包含中文标签和说明
- ✅ 任何需要文字标注的图片

### 不适用场景

- ❌ dreamy-photo 风格 - 明确要求 NO TEXT
- ❌ soft-botanical 风格 - 明确要求 NO TEXT
- ❌ minimal-collage 风格 - 明确要求 NO TEXT

---

## 🖼️ 封面图模板（2.35:1 横版）

### dreamy-photo 风格（场景类）

```
A 2.35:1 wide banner photograph in dreamy realistic style.
Scene: [具体场景描述], authentic home environment, lived-in atmosphere.
Lighting: Soft natural window light, warm golden hour glow, gentle shadows.
Details: [场景细节元素]
Mood: [情绪关键词], cozy, inviting.
Composition: Wide horizontal layout, balanced composition, subject centered or rule-of-thirds.
Color palette: Muted Morandi colors, desaturated tones, cream and sage.
Color control: Use dusty coral instead of red, muted rose instead of pink, soft terracotta for warm accents.
Style: Realistic lifestyle photography, soft focus, film-like quality, NOT product photography.
NO TEXT. NO WORDS. NO LETTERS. NO PEOPLE. NO STUDIO LIGHTING.
```

### cozy-sketch 风格（教程类）

```
A 2.35:1 wide banner illustration in hand-drawn sketch style.
Subject: [主题内容]
Details: Pencil line drawings with soft watercolor washes, notebook paper texture.
Elements: [具体元素]
Composition: Wide horizontal layout, elements spread across the banner.
Annotations: Include simple Chinese text labels for key points.
Color palette: Muted beige, dusty rose, sage green watercolor accents.
Style: Cozy sketchbook aesthetic, natural imperfect lines.

CRITICAL REQUIREMENTS:
- Use ONLY Chinese characters for ALL text - must be CLEAR and LEGIBLE
- NO English letters or words anywhere
- Text must NOT be distorted or blurry
```

### infographic-sketch 风格（科普类）

```
A 2.35:1 wide banner infographic in hand-drawn sketchnote style.
Topic: [知识主题]
Structure: [信息结构描述]
Composition: Wide horizontal layout, information flows left to right.
Visual elements: Icons, simple diagrams, arrows, bullet points.
Text: Include Chinese labels and brief explanations.
Background: Lined notebook paper or clean white.
Color palette: Functional colors for categorization, yellow highlighter accents, red pen circles.
Style: Educational sketchnote aesthetic.

CRITICAL REQUIREMENTS:
- Use ONLY Chinese characters for ALL text - must be CLEAR and LEGIBLE
- NO English letters or words anywhere
- Text must NOT be distorted or blurry
```

### soft-botanical 风格（情感类）

```
A 2.35:1 wide banner illustration in soft botanical watercolor style.
Subject: [情感主题相关意象]
Elements: Delicate plants, flowers, leaves, petals.
Composition: Wide horizontal layout, generous white space, floating elements, dreamy arrangement.
Mood: [情绪关键词]
Color palette: Sage green, blush pink, cream white, muted earth tones.
Style: Soft watercolor with gentle brushstrokes, ethereal and calming.
NO TEXT. NO WORDS. NO LETTERS.
```

### minimal-collage 风格（产品类）

```
A 2.35:1 wide banner illustration in minimal collage style.
Subject: [产品/物品]
Composition: Wide horizontal layout, clean geometric shapes, subject positioned for visual balance.
Elements: Abstract shapes, simple shadows, product highlight.
Background: Pure white or soft neutral.
Color palette: Muted grey-green, soft taupe, clean white accents.
Style: Modern minimalist, editorial clean aesthetic.
NO TEXT. NO WORDS. NO LETTERS.
```

---

## 📄 正文配图模板（16:9 横版）

### dreamy-photo 风格（场景类）

```
A 16:9 wide photograph in dreamy realistic style.
Scene: [具体场景描述], authentic home environment, lived-in atmosphere.
Lighting: Soft natural window light, warm golden hour glow, gentle shadows.
Details: [场景细节元素]
Mood: [情绪关键词], cozy, inviting.
Composition: Wide horizontal layout, subject clearly visible, natural framing.
Color palette: Muted Morandi colors, desaturated tones, cream and sage.
Color control: Use dusty coral instead of red, muted rose instead of pink, soft terracotta for warm accents.
Style: Realistic lifestyle photography, soft focus, film-like quality, NOT product photography.
NO TEXT. NO WORDS. NO LETTERS. NO PEOPLE. NO STUDIO LIGHTING.
```

### cozy-sketch 风格（教程类）

```
A 16:9 wide illustration in hand-drawn sketch style.
Subject: [主题内容]
Details: Pencil line drawings with soft watercolor washes, notebook paper texture.
Elements: [具体元素]
Composition: Wide horizontal layout, clear visual hierarchy.
Annotations: Include simple Chinese text labels for key points.
Color palette: Muted beige, dusty rose, sage green watercolor accents.
Style: Cozy sketchbook aesthetic, natural imperfect lines.

CRITICAL REQUIREMENTS:
- Use ONLY Chinese characters for ALL text - must be CLEAR and LEGIBLE
- NO English letters or words anywhere
- Text must NOT be distorted or blurry
```

### infographic-sketch 风格（科普类）

```
A 16:9 wide infographic in hand-drawn sketchnote style.
Topic: [知识主题]
Structure: [信息结构描述]
Composition: Wide horizontal layout, information organized clearly.
Visual elements: Icons, simple diagrams, arrows, bullet points.
Text: Include Chinese labels and brief explanations.
Background: Lined notebook paper or clean white.
Color palette: Functional colors for categorization, yellow highlighter accents, red pen circles.
Style: Educational sketchnote aesthetic.

CRITICAL REQUIREMENTS:
- Use ONLY Chinese characters for ALL text - must be CLEAR and LEGIBLE
- NO English letters or words anywhere
- Text must NOT be distorted or blurry
```

### soft-botanical 风格（情感类）

```
A 16:9 wide illustration in soft botanical watercolor style.
Subject: [情感主题相关意象]
Elements: Delicate plants, flowers, leaves, petals.
Composition: Wide horizontal layout, generous white space, floating elements, dreamy arrangement.
Mood: [情绪关键词]
Color palette: Sage green, blush pink, cream white, muted earth tones.
Style: Soft watercolor with gentle brushstrokes, ethereal and calming.
NO TEXT. NO WORDS. NO LETTERS.
```

### minimal-collage 风格（产品类）

```
A 16:9 wide illustration in minimal collage style.
Subject: [产品/物品]
Composition: Wide horizontal layout, clean geometric shapes, centered subject, generous negative space.
Elements: Abstract shapes, simple shadows, product highlight.
Background: Pure white or soft neutral.
Color palette: Muted grey-green, soft taupe, clean white accents.
Style: Modern minimalist, editorial clean aesthetic.
NO TEXT. NO WORDS. NO LETTERS.
```

---

## 🎨 风格选择规则

> [!IMPORTANT]
> **订阅号长文干货类内容，优先使用 dreamy-photo 真实感风格！**
> 
> 真实的操作场景照片比手绘图更有说服力，读者更容易代入和学习。

| 选题类型 | 风格 | 说明 |
|---------|------|------|
| **干货教程类**（扦插、换盆、浇水步骤） | **dreamy-photo** | ⭐推荐！真实操作场景，有说服力 |
| 场景类（居家、装饰） | dreamy-photo | 真实感、自然光、柔焦 |
| 养护知识类（养护技巧、避坑指南） | dreamy-photo | 真实植物状态，更直观 |
| 轻科普类（简单原理解释） | cozy-sketch | 手绘涂鸦感、可配中文标注 |
| 重科普类（复杂知识图谱） | infographic-sketch | 信息图+手绘、清晰层级 |
| 情感类（心情、治愈） | soft-botanical | 柔和水彩、氛围感 |
| 产品类（推荐、测评） | minimal-collage | 极简拼贴、突出主体 |

### 风格选择原则

1. **干货实操类 → dreamy-photo**：扦插、换盆、修剪、浇水等实操教程，使用真实场景照片
2. **抽象概念类 → cozy-sketch / infographic-sketch**：需要图解说明的抽象知识
3. **情感治愈类 → soft-botanical**：氛围感、情绪表达为主的内容

---

## ⚙️ 技术参数

| 参数 | 值 |
|------|------|
| **API 端点** | https://yunwu.ai/v1 |
| **模型** | gemini-3-pro-image-preview |
| **封面图比例** | 2.35:1（在 prompt 中强调） |
| **正文配图比例** | 16:9（在 prompt 中强调） |

---

## 🆚 与小红书配图的区别

| 维度 | 小红书 | 微信公众号 |
|------|--------|-----------|
| 比例 | 3:4 竖版 | 2.35:1 / 16:9 横版 |
| 配图指南 | `image-prompt-guide.md` | **本文档** |
| 封面尺寸 | 1080×1440px | 900×383px |
| 正文配图尺寸 | 1080×1440px | 900×506px |

---

*v1.0 创建：2026-01-16 - 公众号专用横版配图规范*
*v1.1 更新：2026-01-16 - 添加图文格式说明*
*v1.2 更新：2026-01-17 - 添加中文文字清晰度强制要求*
