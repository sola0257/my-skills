# 插画风格 Prompt 模板库 v1.0

> **本文档包含**：10种插画风格的完整 Prompt 模板（5大风格 × 2种美感）+ 彩铅步骤图模板

---

## 📋 使用说明

### Prompt 结构

每个 Prompt 遵循以下结构：
```
[基础描述] + [风格定义] + [文化美感] + [技术参数] + [约束条件]
```

### 变量替换

模板中的变量需要替换为实际内容：
- `{subject}` - 植物名称（如"多肉植物桃蛋"）
- `{details}` - 细节描述（从图片分析或用户输入提取）
- `{composition}` - 构图描述
- `{mood}` - 情绪关键词
- `{user_preferences}` - 用户特殊要求

---

## 🌊 1. 清新水彩（Watercolor）

### 1.1 清新水彩（东方美感）

**风格代码**：`watercolor_oriental`

**视觉特点**：
- 留白多、意境感强
- 色彩淡雅、晕染自然
- 笔触轻盈、水分充足
- 类似中国工笔画的细腻

**Prompt 模板**：
```
A 3:4 watercolor illustration in Oriental style.
Subject: {subject}
Composition: Generous white space, asymmetric balance, breathing room around subject.
Technique: Delicate wet-on-wet washes, soft color bleeding, transparent layers.
Details: {details}, fine brush details on petals/leaves, natural water marks.
Color palette: Muted jade green, soft plum, pale peach, dusty rose, cream white.
Cultural elements: Inspired by Chinese gongbi painting, elegant restraint, poetic atmosphere.
Mood: {mood}, serene, contemplative, understated elegance.
Paper texture: Cold-press watercolor paper, visible grain.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

**关键词说明**：
- 东方特色：`jade green`, `plum blossom pink`, `ink wash influence`, `poetic restraint`
- 技法：`wet-on-wet`, `transparent layers`, `soft bleeding edges`
- 留白：`generous white space`, `breathing room`, `asymmetric balance`

---

### 1.2 清新水彩（西方美感）

**风格代码**：`watercolor_western`

**视觉特点**：
- 色彩饱满（但仍保持水彩透明感）
- 构图更满、细节更丰富
- 笔触明显、层次分明
- 类似植物插画风格

**Prompt 模板**：
```
A 3:4 watercolor illustration in Western botanical style.
Subject: {subject}
Composition: Full composition, detailed botanical accuracy, centered subject with surrounding elements.
Technique: Layered washes, visible brushstrokes, wet-on-dry details, controlled color mixing.
Details: {details}, botanical precision, leaf veins, petal textures, stem details.
Color palette: Rich but muted - forest green, burgundy, golden ochre, deep coral, cream.
Cultural elements: Inspired by Victorian botanical illustrations, scientific accuracy meets artistic beauty.
Mood: {mood}, vibrant yet elegant, detailed, educational aesthetic.
Paper texture: Hot-press watercolor paper, smooth finish.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

**关键词说明**：
- 西方特色：`botanical accuracy`, `Victorian illustration`, `scientific precision`
- 技法：`layered washes`, `wet-on-dry`, `controlled mixing`
- 构图：`full composition`, `centered subject`, `detailed rendering`

---

## 🖋️ 2. 水墨国画（Chinese Ink Painting）

### 2.1 水墨国画（东方美感）

**风格代码**：`ink_oriental`

**视觉特点**：
- 水墨为主，淡彩点缀
- 写意风格，笔墨韵味
- 大量留白，意境深远
- 书法题款（可选）

**Prompt 模板**：
```
A 3:4 Chinese ink painting (Guo Hua) illustration.
Subject: {subject}
Style: Xieyi (freehand brushwork), expressive ink strokes, spontaneous and fluid.
Technique: Ink wash gradations from dark to light, minimal color accents (light mineral pigments).
Brushwork: Confident calligraphic strokes, varying pressure, dry brush textures.
Details: {details}, capturing essence rather than exact form.
Composition: Asymmetric, generous negative space, following traditional Chinese composition rules.
Color palette: Black ink dominant, subtle touches of vermillion, indigo, or ochre.
Cultural elements: Traditional Chinese painting aesthetics, poetic restraint, "yi jing" (artistic conception).
Paper: Xuan paper texture, visible ink absorption and bleeding.
Optional: Small red seal stamp in corner (traditional artist's seal).
NO ENGLISH TEXT. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

**关键词说明**：
- 国画特色：`xieyi brushwork`, `ink wash`, `calligraphic strokes`, `yi jing`
- 技法：`varying ink density`, `dry brush`, `spontaneous strokes`
- 留白：`generous negative space`, `asymmetric composition`

---

### 2.2 水墨国画（西方美感）

**风格代码**：`ink_western`

**视觉特点**：
- 融合现代审美
- 色彩更丰富
- 保留国画笔触
- 适合年轻受众

**Prompt 模板**：
```
A 3:4 contemporary Chinese-style illustration.
Subject: {subject}
Style: Modern interpretation of traditional Chinese painting, fusion aesthetic.
Technique: Ink brush strokes combined with watercolor washes, contemporary color palette.
Brushwork: Expressive Chinese brush techniques with modern composition.
Details: {details}, balance between traditional and contemporary.
Composition: Clean, modern layout with traditional brushwork elements.
Color palette: Muted modern colors - sage green, dusty pink, soft grey, cream, with ink black accents.
Cultural elements: Chinese painting influence without being strictly traditional, accessible to modern audience.
Mood: {mood}, elegant, contemporary, culturally rooted yet fresh.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

---

## ✏️ 3. 细腻彩铅（Colored Pencil）

### 3.1 细腻彩铅（东方美感）

**风格代码**：`pencil_oriental`

**视觉特点**：
- 细腻柔和的笔触
- 淡雅色调
- 留白处理
- 纸张质感明显

**Prompt 模板**：
```
A 3:4 colored pencil illustration in Oriental delicate style.
Subject: {subject}
Technique: Fine layered strokes, gentle blending, soft transitions.
Texture: Visible pencil marks, paper grain showing through, delicate hatching.
Details: {details}, meticulous attention to subtle color shifts.
Composition: Generous white space, subject positioned with breathing room.
Color palette: Soft pastels - pale jade, blush pink, cream, light ochre, gentle grey-green.
Style: Delicate and refined, Japanese colored pencil aesthetic influence.
Mood: {mood}, gentle, contemplative, understated beauty.
Paper: Cream or white drawing paper texture visible.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

---

### 3.2 细腻彩铅（西方美感）

**风格代码**：`pencil_western`

**视觉特点**：
- 写实风格
- 色彩饱满
- 细节丰富
- 光影明确

**Prompt 模板**：
```
A 3:4 colored pencil illustration in Western realistic style.
Subject: {subject}
Technique: Layered burnishing, rich color saturation, smooth blending.
Texture: Polished finish, minimal paper grain, photorealistic rendering.
Details: {details}, botanical accuracy, precise shading, clear light source.
Composition: Full detailed rendering, centered subject, complete background.
Color palette: Rich naturalistic colors - deep greens, vibrant florals, warm earth tones.
Style: Hyperrealistic colored pencil art, botanical illustration tradition.
Mood: {mood}, precise, vibrant, scientifically accurate yet artistic.
Lighting: Clear directional light, defined shadows and highlights.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

---

## 📝 3.3 细腻彩铅（步骤图）⭐

**风格代码**：`pencil_steps`

**特殊说明**：
- 必须使用 Gemini 模型（中文标注）
- 生成4-6个步骤
- 每个步骤独立生成
- 保持一致的视角和构图

### Step 1 - 线稿（Line Drawing）

```
A 3:4 colored pencil illustration - STEP 1: Initial line drawing.
Subject: {subject}
Stage: Light pencil outline, basic shapes and contours only.
Details: Simple line work, no shading, clean sketch.
Style: Preparatory drawing stage, educational demonstration.
Text overlay: Add Chinese text "步骤1：线稿" in upper left corner, clear handwritten style, soft cream color.
Paper: White drawing paper, clean and minimal.
Image size: 1080x1440 pixels (3:4 vertical format).
```

### Step 2 - 基础色（Base Colors）

```
A 3:4 colored pencil illustration - STEP 2: Base color layer.
Subject: {subject}
Stage: First layer of light color, establishing color zones.
Details: Gentle even strokes, light pressure, building foundation.
Style: Educational demonstration, showing color blocking stage.
Text overlay: Add Chinese text "步骤2：铺底色" in upper left corner, clear handwritten style, soft cream color.
Colors: Light washes of base colors, no deep shadows yet.
Image size: 1080x1440 pixels (3:4 vertical format).
```

### Step 3 - 深化色彩（Deepening Colors）

```
A 3:4 colored pencil illustration - STEP 3: Color deepening.
Subject: {subject}
Stage: Adding layers, building color intensity, initial shading.
Details: Multiple layers visible, color transitions beginning.
Style: Educational demonstration, mid-process stage.
Text overlay: Add Chinese text "步骤3：深化色彩" in upper left corner, clear handwritten style, soft cream color.
Colors: Richer tones, shadows starting to form.
Image size: 1080x1440 pixels (3:4 vertical format).
```

### Step 4 - 细节刻画（Detail Work）

```
A 3:4 colored pencil illustration - STEP 4: Detail refinement.
Subject: {subject}
Stage: Adding fine details, textures, veins, subtle color variations.
Details: Precise work on specific areas, texture building.
Style: Educational demonstration, detail stage.
Text overlay: Add Chinese text "步骤4：细节刻画" in upper left corner, clear handwritten style, soft cream color.
Focus: Leaf veins, petal textures, stem details.
Image size: 1080x1440 pixels (3:4 vertical format).
```

### Step 5 - 完成（Final Touches）

```
A 3:4 colored pencil illustration - STEP 5: Final artwork.
Subject: {subject}
Stage: Completed illustration with all details, highlights, and finishing touches.
Details: {details}, polished and refined.
Style: Educational demonstration, final result.
Text overlay: Add Chinese text "步骤5：完成" in upper left corner, clear handwritten style, soft cream color.
Finish: Complete with highlights, deepest shadows, final adjustments.
Image size: 1080x1440 pixels (3:4 vertical format).
```

---

**（续下一部分：油画和彩绘风格）**

## 🎨 4. 质感油画（Oil Painting）

### 4.1 质感油画（东方美感）

**风格代码**：`oil_oriental`

**视觉特点**：
- 融合东方审美
- 色彩柔和
- 笔触含蓄
- 意境感

**Prompt 模板**：
```
A 3:4 oil painting illustration with Oriental aesthetic.
Subject: {subject}
Technique: Soft impasto, gentle brushstrokes, subtle texture.
Style: Oil painting with Eastern sensibility, restrained palette.
Details: {details}, poetic interpretation rather than literal rendering.
Composition: Asymmetric, generous negative space, contemplative mood.
Color palette: Muted oil colors - sage green, dusty rose, cream, soft ochre, grey-blue.
Brushwork: Visible but gentle strokes, layered glazes, soft edges.
Mood: {mood}, serene, contemplative, fusion of East and West.
Canvas texture: Linen canvas, subtle weave visible.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

---

### 4.2 质感油画（西方美感）

**风格代码**：`oil_western`

**视觉特点**：
- 古典油画技法
- 色彩浓郁
- 笔触明显
- 光影强烈

**Prompt 模板**：
```
A 3:4 oil painting illustration in classical Western style.
Subject: {subject}
Technique: Rich impasto, bold brushstrokes, thick paint application.
Style: Classical oil painting tradition, Dutch Golden Age botanical influence.
Details: {details}, dramatic lighting, rich textures.
Composition: Full composition, chiaroscuro lighting, depth and dimension.
Color palette: Rich oil colors - deep emerald, burgundy, golden yellow, warm browns, cream highlights.
Brushwork: Visible confident strokes, layered paint, textural variety.
Lighting: Dramatic side lighting, strong shadows, luminous highlights.
Mood: {mood}, dramatic, luxurious, timeless classical beauty.
Canvas texture: Canvas weave visible, traditional oil painting surface.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

---

## 🖌️ 5. 装饰彩绘（Gouache）

### 5.1 装饰彩绘（东方美感）

**风格代码**：`gouache_oriental`

**视觉特点**：
- 平涂为主
- 装饰性强
- 图案化处理
- 民间艺术感

**Prompt 模板**：
```
A 3:4 gouache illustration with Oriental decorative style.
Subject: {subject}
Technique: Flat color application, opaque coverage, clean edges.
Style: Decorative folk art influence, pattern-like quality.
Details: {details}, stylized rather than realistic, ornamental approach.
Composition: Balanced, decorative arrangement, pattern sensibility.
Color palette: Harmonious flat colors - jade green, coral red, cream, soft gold, ink black accents.
Brushwork: Smooth opaque layers, minimal visible brushstrokes, graphic quality.
Mood: {mood}, cheerful, decorative, folk art charm.
Cultural elements: Inspired by Chinese folk painting, Japanese mingei aesthetic.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

---

### 5.2 装饰彩绘（西方美感）

**风格代码**：`gouache_western`

**视觉特点**：
- 现代插画风格
- 色块明确
- 设计感强
- 商业插画质感

**Prompt 模板**：
```
A 3:4 gouache illustration in modern Western style.
Subject: {subject}
Technique: Opaque flat colors, clean shapes, graphic approach.
Style: Contemporary illustration, editorial quality, design-forward.
Details: {details}, simplified forms, bold color choices.
Composition: Modern layout, strong graphic impact, intentional negative space.
Color palette: Bold yet sophisticated - teal, coral, mustard, cream, charcoal.
Brushwork: Smooth matte finish, clean edges, poster-like quality.
Mood: {mood}, modern, confident, design-conscious.
Aesthetic: Mid-century modern illustration influence, Scandinavian design sensibility.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

---

## 📝 使用示例

### 示例1：清新水彩（东方）- 多肉植物

**输入变量**：
- subject: "一株粉色的桃蛋多肉植物"
- details: "圆润饱满的叶片，表面有白霜，粉色渐变"
- mood: "治愈、温柔"

**生成的 Prompt**：
```
A 3:4 watercolor illustration in Oriental style.
Subject: 一株粉色的桃蛋多肉植物
Composition: Generous white space, asymmetric balance, breathing room around subject.
Technique: Delicate wet-on-wet washes, soft color bleeding, transparent layers.
Details: 圆润饱满的叶片，表面有白霜，粉色渐变, fine brush details on petals/leaves, natural water marks.
Color palette: Muted jade green, soft plum, pale peach, dusty rose, cream white.
Cultural elements: Inspired by Chinese gongbi painting, elegant restraint, poetic atmosphere.
Mood: 治愈、温柔, serene, contemplative, understated elegance.
Paper texture: Cold-press watercolor paper, visible grain.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

---

### 示例2：细腻彩铅（步骤图）- 蝴蝶兰

**步骤1 Prompt**：
```
A 3:4 colored pencil illustration - STEP 1: Initial line drawing.
Subject: 一株白色蝴蝶兰
Stage: Light pencil outline, basic shapes and contours only.
Details: Simple line work, no shading, clean sketch.
Style: Preparatory drawing stage, educational demonstration.
Text overlay: Add Chinese text "步骤1：线稿" in upper left corner, clear handwritten style, soft cream color.
Paper: White drawing paper, clean and minimal.
Image size: 1080x1440 pixels (3:4 vertical format).
```

**步骤5 Prompt**：
```
A 3:4 colored pencil illustration - STEP 5: Final artwork.
Subject: 一株白色蝴蝶兰
Stage: Completed illustration with all details, highlights, and finishing touches.
Details: 白色花瓣带淡黄色中心，细腻的纹理，优雅的花型, polished and refined.
Style: Educational demonstration, final result.
Text overlay: Add Chinese text "步骤5：完成" in upper left corner, clear handwritten style, soft cream color.
Finish: Complete with highlights, deepest shadows, final adjustments.
Image size: 1080x1440 pixels (3:4 vertical format).
```

---

## 🔧 Prompt 优化技巧

### 1. 颜色控制

**避免高饱和度**：
- ❌ `bright red`, `vivid pink`, `neon green`
- ✅ `dusty coral`, `muted rose`, `sage green`

### 2. 真实感约束

**每个 Prompt 必须包含**：
- 真实感约束：`authentic`, `lived-in atmosphere`, `natural imperfections`
- 颜色约束：`desaturated`, `muted tones`, `low saturation`

### 3. 文字处理

**需要中文文字时**：
- 使用 Gemini 模型
- 添加：`Text overlay: Add Chinese text "XXX" in clear handwritten style`
- 指定位置：`upper left corner`, `lower center` 等

### 4. 风格一致性

**保持视觉一致性**：
- 同一风格使用相同的关键词
- 同一风格使用相同的模型
- 同一风格使用相同的色彩描述

---

## 📋 快速参考表

| 风格代码 | 用户友好名称 | 关键特征 | 适用场景 |
|---------|-------------|---------|---------|
| `watercolor_oriental` | 清新水彩（东方） | 留白、淡雅、晕染 | 治愈系、日常记录 |
| `watercolor_western` | 清新水彩（西方） | 细节、饱满、植物插画 | 科普、教育 |
| `ink_oriental` | 水墨国画（东方） | 水墨、写意、诗意 | 传统节日、禅意 |
| `ink_western` | 水墨国画（西方） | 现代水墨、融合 | 文艺、现代 |
| `pencil_oriental` | 细腻彩铅（东方） | 柔和、淡雅、留白 | 温柔、细腻 |
| `pencil_western` | 细腻彩铅（西方） | 写实、光影、细节 | 教程、写实 |
| `pencil_steps` | 细腻彩铅（步骤图） | 分步骤、中文标注 | 教程、步骤展示 |
| `oil_oriental` | 质感油画（东方） | 含蓄、意境、柔和 | 高级感、艺术 |
| `oil_western` | 质感油画（西方） | 浓郁、戏剧、古典 | 艺术氛围、情感 |
| `gouache_oriental` | 装饰彩绘（东方） | 平涂、装饰、民间 | 活泼、图案化 |
| `gouache_western` | 装饰彩绘（西方） | 现代、设计、商业 | 现代、设计感 |

---

**最后更新**：2026-01-31
