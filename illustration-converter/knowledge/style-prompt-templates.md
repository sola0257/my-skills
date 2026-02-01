# 插画风格 Prompt 模板库 v2.0

> **本文档包含**：10种插画风格的完整 Prompt 模板（5大风格 × 2种美感）+ 彩铅步骤图模板 + 4张系列图结构

---

## 📋 使用说明

### 4张系列图结构（标准模式）

**所有风格都遵循统一的4张系列图结构**：

1. **局部特写（Close-up Detail）**
   - 聚焦植物最美的局部（叶片、花朵、纹理）
   - 展现细节之美
   - 构图：紧凑，填满画面

2. **中景视角（Mid-range View）**
   - 展现植物的整体形态
   - 保留部分环境（花盆、周边）
   - 构图：平衡，主体突出

3. **整体全景（Full Scene）**
   - 完整展现植物+花盆+基础环境
   - 真实还原照片内容
   - 构图：完整，忠实原图

4. **意境氛围（Atmospheric Mood）** ⭐
   - 将植物置于想象的美丽环境中
   - 创造诗意氛围，营造意境
   - **关键**：统一融合的场景，不是前景+背景拼贴

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

### 意境氛围图的特殊要求 ⚠️

**必须遵循的核心原则**（基于反面案例总结）：

1. **参考图选择**：使用原始照片，不是已生成的水彩图
2. **统一融合**：植物、花盆、环境一起绘制，不是分层
3. **自然规律**：植物必须从花盆中自然生长
4. **和谐环境**：环境元素与植物协调
5. **饱满构图**：不是极简留白，而是有序的饱满构图

**关键 Prompt 约束**：
```
IMPORTANT: This is NOT a foreground+background composition.
The entire scene - plant, pot, and environment - should be painted
together as ONE unified painting with harmonious integration.
```

---

## 🌊 1. 清新水彩（Watercolor）

### 1.1 清新水彩（东方美感）

**风格代码**：`watercolor_oriental`

**视觉特点**：
- 留白多、意境感强
- 色彩淡雅、晕染自然
- 笔触轻盈、水分充足
- 类似中国工笔画的细腻

**关键词说明**：
- 东方特色：`jade green`, `plum blossom pink`, `ink wash influence`, `poetic restraint`
- 技法：`wet-on-wet`, `transparent layers`, `soft bleeding edges`
- 留白：`generous white space`, `breathing room`, `asymmetric balance`

---

#### 图1：局部特写（Close-up Detail）

```
A 3:4 watercolor illustration in Oriental style - CLOSE-UP DETAIL.
Subject: {subject} - focusing on the most beautiful detail (leaf texture, petal, rosette cluster)
Composition: Tight crop, filling the frame, intimate view of plant details.
Technique: Delicate wet-on-wet washes, soft color bleeding, transparent layers.
Details: {details}, fine brush details showing texture, natural water marks, subtle color variations.
Color palette: Muted jade green, soft plum, pale peach, dusty rose, cream white.
Cultural elements: Inspired by Chinese gongbi painting, elegant restraint, poetic atmosphere.
Mood: {mood}, serene, contemplative, understated elegance.
Paper texture: Cold-press watercolor paper, visible grain.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

#### 图2：中景视角（Mid-range View）

```
A 3:4 watercolor illustration in Oriental style - MID-RANGE VIEW.
Subject: {subject} - showing the overall plant form with some surrounding context
Composition: Balanced composition, plant as main subject with partial pot visible, some breathing room.
Technique: Delicate wet-on-wet washes, soft color bleeding, transparent layers.
Details: {details}, capturing the plant's growth pattern and form, fine brush details.
Color palette: Muted jade green, soft plum, pale peach, dusty rose, cream white.
Cultural elements: Inspired by Chinese gongbi painting, elegant restraint, poetic atmosphere.
Mood: {mood}, serene, contemplative, understated elegance.
Paper texture: Cold-press watercolor paper, visible grain.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

#### 图3：整体全景（Full Scene）

```
A 3:4 watercolor illustration in Oriental style - FULL SCENE.
Subject: {subject} - complete plant with pot and immediate surroundings
Composition: Complete view, generous white space, asymmetric balance, breathing room around subject.
Technique: Delicate wet-on-wet washes, soft color bleeding, transparent layers.
Details: {details}, fine brush details on petals/leaves, natural water marks, showing the complete plant-pot unit.
Color palette: Muted jade green, soft plum, pale peach, dusty rose, cream white.
Cultural elements: Inspired by Chinese gongbi painting, elegant restraint, poetic atmosphere.
Mood: {mood}, serene, contemplative, understated elegance.
Paper texture: Cold-press watercolor paper, visible grain.
NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

#### 图4：意境氛围（Atmospheric Mood）⭐

```
A 3:4 watercolor illustration in Oriental style - ATMOSPHERIC MOOD.
Subject: {subject} - placed within an imagined beautiful garden setting

IMPORTANT: This is NOT a foreground+background composition.
The entire scene - plant, pot, and environment - should be painted
together as ONE unified watercolor painting with harmonious integration.

Composition: The plant-pot unit is thoughtfully placed within a gentle garden atmosphere.
The environment and plant are painted together, creating a cohesive whole.
Soft transitions between elements, no harsh separation.
Full composition with organized breathing room, NOT minimalist with excessive white space.

Environment (integrated, not layered):
- Soft garden atmosphere with muted, harmonious colors
- Complementary elements: garden stones, soft moss, gentle foliage in background
- Garden elements painted with the same watercolor technique as the plant
- Everything flows together - plant, pot, ground, atmosphere - as one painting
- Colors: muted earth tones, soft greens, gentle grays, cream

Natural Logic (CRITICAL):
- Plant MUST grow naturally from the pot
- Plant and pot remain connected, no separation
- Maintain botanical accuracy and natural growth patterns

Technique: Unified watercolor approach throughout - wet-on-wet washes for all elements,
soft edges everywhere, colors bleeding naturally between plant and environment.

Details: {details}, maintaining specific plant characteristics while creating poetic atmosphere.

Color palette: Muted jade green, soft plum, pale peach, dusty rose, cream white,
gentle earth tones for environment.

Cultural elements: Inspired by Chinese garden paintings, poetic atmosphere,
harmonious integration of plant and environment.

Mood: {mood}, serene, contemplative, poetic, unified beauty.

Paper texture: Cold-press watercolor paper, visible grain throughout.

NO TEXT. NO WORDS. NO PEOPLE.
Image size: 1080x1440 pixels (3:4 vertical format).
```

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
- 写实风格、色彩饱满
- 细节丰富、光影明确
- **核心特征**：可见的彩铅笔触、纸张纹理、层层叠加的色彩
- **手绘感**：不是照片转换，而是真实的手绘彩铅画

**关键词说明**：
- 彩铅特征：`visible pencil strokes`, `layered colored pencil marks`, `paper tooth texture`, `hand-drawn quality`
- 技法：`burnishing technique`, `layering colors`, `cross-hatching`, `gradual color build-up`
- 质感：`matte finish`, `slight paper grain`, `authentic colored pencil texture`

---

#### 图1：局部特写（Close-up Detail）

```
A 3:4 colored pencil illustration in Western realistic style - CLOSE-UP DETAIL.
Subject: {subject} - extreme close-up of the most intricate detail (single petal, leaf vein pattern, flower center).
Composition: Macro view, filling the entire frame, showing botanical details at intimate scale.
Technique: HAND-DRAWN colored pencil with VISIBLE PENCIL STROKES. Layered burnishing technique, rich color saturation achieved through multiple layers, smooth blending with slight texture.
Texture: IMPORTANT - This must look like REAL COLORED PENCIL ART, not a photo filter. Show paper tooth texture, visible pencil marks, hand-drawn quality with slight imperfections that prove it's hand-drawn.
Details: {details}, botanical accuracy with artistic interpretation, precise shading showing form and volume, clear light source creating defined shadows and highlights.
Color palette: Rich naturalistic colors - deep forest greens, vibrant flower tones, warm earth browns, subtle color transitions through layering.
Style: Hyperrealistic botanical colored pencil illustration in the tradition of scientific botanical art, but with artistic soul. Think Ann Swan or Janie Gildow's colored pencil work.
Mood: {mood}, precise yet warm, scientifically accurate yet emotionally engaging.
Lighting: Clear directional natural light, defined cast shadows, subtle reflected light in shadow areas.
Paper: White or cream drawing paper with visible texture.
NO TEXT. NO WORDS. NO PEOPLE. NO PHOTO EFFECTS.
Image size: 1080x1440 pixels (3:4 vertical format).
```

#### 图2：中景视角（Mid-range View）

```
A 3:4 colored pencil illustration in Western realistic style - MID-RANGE VIEW.
Subject: {subject} - showing the plant's overall form and character, including stem/leaves and partial pot.
Composition: Balanced composition with plant as focal point, some environmental context (pot edge, surface), comfortable breathing room around subject.
Technique: HAND-DRAWN colored pencil with VISIBLE PENCIL STROKES. Layered color application, burnishing for smooth areas, cross-hatching for texture, gradual color build-up showing the artist's process.
Texture: CRITICAL - Must show AUTHENTIC COLORED PENCIL TEXTURE. Visible pencil marks, paper grain showing through lighter areas, hand-drawn quality with natural variations in pressure and stroke direction.
Details: {details}, complete botanical structure visible, careful attention to how leaves attach to stems, natural growth patterns, realistic color variations within the plant.
Color palette: Full range of naturalistic plant colors - various greens from yellow-green to blue-green, flower colors with subtle tonal shifts, neutral pot tones, soft background hints.
Style: Professional botanical colored pencil art - realistic but not photographic, showing the hand of the artist. Reference artists like Ann Swan, Janie Gildow, or Cathy Sheeter.
Mood: {mood}, approachable yet detailed, inviting closer inspection.
Lighting: Natural window light quality, soft shadows, gentle highlights on glossy leaves.
Paper: Quality drawing paper with subtle texture visible.
NO TEXT. NO WORDS. NO PEOPLE. NO PHOTO FILTERS.
Image size: 1080x1440 pixels (3:4 vertical format).
```

#### 图3：整体全景（Full Scene）

```
A 3:4 colored pencil illustration in Western realistic style - FULL SCENE.
Subject: {subject} - complete plant in pot with immediate surroundings, faithful to reference photo composition.
Composition: Full view showing entire plant-pot unit, including base/surface, complete environmental context as seen in reference photo.
Technique: HAND-DRAWN colored pencil throughout. Consistent pencil stroke quality across entire image, varying detail levels (more detail on plant, softer treatment of background), unified colored pencil aesthetic.
Texture: ESSENTIAL - Every element must show COLORED PENCIL TEXTURE. Visible pencil strokes on plant, pot, and background. Paper texture visible. Hand-drawn quality obvious - this is NOT a photo with a filter applied.
Details: {details}, complete botanical accuracy, pot material and texture rendered in colored pencil, surface/background suggested with looser strokes, spatial relationships clear.
Color palette: Harmonious full-scene palette - plant colors dominant, pot in complementary or neutral tones, background soft and supportive (cream, pale gray, or subtle environmental colors).
Style: Complete botanical colored pencil illustration showing the full subject in context. Think of gallery-quality botanical art that tells the complete story of the plant.
Mood: {mood}, complete and satisfying, showing the plant's full presence and character.
Lighting: Consistent natural lighting across the scene, shadows anchoring the pot to the surface, atmospheric perspective if background has depth.
Paper: Consistent paper texture throughout.
NO TEXT. NO WORDS. NO PEOPLE. PURE COLORED PENCIL ART.
Image size: 1080x1440 pixels (3:4 vertical format).
```

#### 图4：意境氛围（Atmospheric Mood）

```
A 3:4 colored pencil illustration in Western realistic style - ATMOSPHERIC MOOD SCENE.
Subject: {subject} - plant in pot placed within an imagined beautiful environment (garden corner, sunlit windowsill, botanical setting).
Composition: Plant-pot unit integrated into a poetic setting, environmental elements supporting the mood, unified scene (NOT foreground plant pasted on background).
Technique: ENTIRELY HAND-DRAWN IN COLORED PENCIL. The plant, pot, and environment are all rendered with the same colored pencil technique, creating a cohesive artistic vision. Varying levels of detail create depth - sharper focus on plant, softer atmospheric treatment of environment.
Texture: CRITICAL - EVERYTHING must show COLORED PENCIL TEXTURE. The plant, pot, table, background elements - all rendered with visible pencil strokes. This creates artistic unity. NO photo elements, NO digital effects, PURE colored pencil art throughout.
Details: {details}, plant rendered with botanical care, environment suggested with artistic freedom (soft foliage, dappled light, garden elements), natural integration where plant grows from pot which sits in environment.
Color palette: Harmonious atmospheric palette - plant colors enhanced by complementary environmental tones, warm or cool color temperature supporting mood, subtle color echoes between plant and environment.
Style: Artistic botanical colored pencil illustration with environmental storytelling. Think of colored pencil artists who create complete scenes, not just isolated specimens. The entire image should feel like one unified colored pencil artwork.
Mood: {mood}, elevated and poetic, inviting the viewer into an idealized moment.
Lighting: Beautiful natural light (golden hour glow, soft morning light, dappled shade), creating atmosphere and emotion, consistent light source affecting all elements.
Environment: Garden setting, windowsill scene, botanical conservatory, or natural habitat - rendered in colored pencil with artistic interpretation.
Paper: Consistent paper texture across the entire illustration.
IMPORTANT: This is NOT a foreground+background composition. The entire scene - plant, pot, and environment - should be drawn together as ONE unified colored pencil artwork with harmonious integration.
NO TEXT. NO WORDS. NO PEOPLE. COMPLETE COLORED PENCIL ILLUSTRATION.
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

## 📝 4张系列图应用指南

### 适用范围

**所有风格都应遵循4张系列图结构**：
- 清新水彩（东方/西方）
- 水墨国画（东方/西方）
- 细腻彩铅（东方/西方）
- 质感油画（东方/西方）
- 装饰彩绘（东方/西方）

### 应用方法

对于未在本文档中详细列出4张模板的风格，按照以下方法生成：

1. **图1：局部特写**
   - 基础模板 + `CLOSE-UP DETAIL`
   - 构图：`Tight crop, filling the frame, intimate view`

2. **图2：中景视角**
   - 基础模板 + `MID-RANGE VIEW`
   - 构图：`Balanced composition, plant as main subject with partial pot visible`

3. **图3：整体全景**
   - 基础模板 + `FULL SCENE`
   - 构图：`Complete view, showing the complete plant-pot unit`

4. **图4：意境氛围**
   - 基础模板 + 意境氛围特殊约束（见下方）
   - **必须添加**：统一融合约束

### 意境氛围图的通用约束（所有风格）

**必须在所有风格的第4张图中添加以下约束**：

```
IMPORTANT: This is NOT a foreground+background composition.
The entire scene - plant, pot, and environment - should be painted/drawn
together as ONE unified artwork with harmonious integration.

Composition: The plant-pot unit is thoughtfully placed within a gentle
[garden/natural] atmosphere. The environment and plant are [painted/drawn]
together, creating a cohesive whole. Soft transitions between elements,
no harsh separation. Full composition with organized breathing room,
NOT minimalist with excessive white space.

Environment (integrated, not layered):
- Soft [garden/natural] atmosphere with muted, harmonious colors
- Complementary elements appropriate to the style
- Environment elements [painted/drawn] with the same technique as the plant
- Everything flows together - plant, pot, ground, atmosphere - as one artwork

Natural Logic (CRITICAL):
- Plant MUST grow naturally from the pot
- Plant and pot remain connected, no separation
- Maintain botanical accuracy and natural growth patterns
```

### 关键检查清单

生成意境氛围图前，必须确认：

- [ ] 使用原始照片作为参考（不是已生成的插画）
- [ ] Prompt 中包含"NOT foreground+background"约束
- [ ] Prompt 中包含"unified artwork"描述
- [ ] Prompt 中包含"Natural Logic"约束
- [ ] 环境元素与植物风格协调
- [ ] 构图饱满但有序，不是极简留白

---

**最后更新**：2026-02-01
**版本**：v2.0
**重要更新**：添加4张系列图结构，整合意境氛围图的核心原则
