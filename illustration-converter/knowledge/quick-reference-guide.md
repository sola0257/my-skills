# 插画生成快速参考指南

**目的**：快速检查 Prompt 是否符合要求，避免常见错误

---

## 🚨 生成前必查清单

### 1. 风格特征检查
- [ ] 包含 `HAND-DRAWN` 或类似强调手绘的词汇
- [ ] 包含 `VISIBLE STROKES/PENCIL STROKES/BRUSHSTROKES`
- [ ] 包含 `paper texture` 或 `canvas texture`
- [ ] 包含 `This is NOT a photo filter` 或类似说明

### 2. 画面纯粹性检查
- [ ] 包含 `This is the artwork itself filling the entire frame`
- [ ] 包含 `NOT a photograph of a drawing/painting`
- [ ] 包含 `No paper edges, no background behind artwork`

### 3. 植物逻辑检查（如果是植物主题）
- [ ] 包含植物连续性说明（flowers → stems → leaves → pot）
- [ ] 包含 `ONE continuous plant, not separate elements`
- [ ] 包含 `The plant GROWS from the pot`

### 4. 构图差异检查
- [ ] 局部特写：明确说明只有花朵，无花盆
- [ ] 中景视角：明确说明完整生长过程，花盆上半部分
- [ ] 整体全景：明确说明完整植物+完整花盆+底座
- [ ] 意境氛围：明确说明保持植物特征

### 5. 画面饱满度检查
- [ ] 包含花朵密度要求（ABUNDANT, LUSH, FULL）
- [ ] 包含减少留白要求（Minimize empty space）

---

## ⚠️ 禁止使用的词汇

### 风格相关
- ❌ photorealistic（会导致照片转换效果）
- ❌ polished finish（会失去手绘感）
- ❌ smooth blending（会过于光滑）
- ❌ digital art（会有数字感）

### 构图相关
- ❌ balanced composition（太模糊）
- ❌ complete view（不够具体）
- ❌ general（没有明确指导）

---

## ✅ 推荐使用的词汇

### 风格相关
- ✅ HAND-DRAWN
- ✅ VISIBLE PENCIL STROKES / BRUSHSTROKES
- ✅ paper texture / canvas texture
- ✅ natural variations
- ✅ authentic [medium] texture

### 构图相关
- ✅ extreme close-up（局部特写）
- ✅ complete plant growing from pot（中景）
- ✅ 100% of plant AND pot AND surface（整体全景）
- ✅ specific percentages（具体百分比）

### 植物逻辑相关
- ✅ continuous plant
- ✅ grows from pot
- ✅ flowers → stems → leaves → pot
- ✅ ONE unified plant

---

## 📋 各画风必备约束

### 彩铅（Colored Pencil）
```
COLORED PENCIL SPECIFIC:
- VISIBLE PENCIL STROKES
- Paper texture must be evident
- Hand-drawn quality with natural imperfections
- Layered pencil marks creating rich color
- This is NOT a photo - it's hand-drawn colored pencil art
- This is the artwork itself, NOT a photograph of a drawing
- No paper edges, no background behind artwork
```

### 水彩（Watercolor）
```
WATERCOLOR SPECIFIC:
- Transparent washes, soft edges
- Water blooms and natural color bleeding
- Visible brushstrokes and paper texture
- This is watercolor painting, not digital art
- This is the artwork itself, NOT a photograph of a painting
- No paper edges, no background behind artwork
```

### 国画（Ink Painting）
```
INK PAINTING SPECIFIC:
- Ink gradations (墨分五色)
- Expressive brushstrokes and natural ink flow
- This is traditional ink painting, not digital art
- This is the artwork itself, NOT a photograph of a painting
- No paper edges, no background behind artwork
```

### 油画（Oil Painting）
```
OIL PAINTING SPECIFIC:
- Visible brushstrokes
- Impasto texture where appropriate
- Rich color layering
- This is oil painting, not digital art
- This is the artwork itself, NOT a photograph of a painting
- No canvas edges, no background behind artwork
```

### 彩绘（Gouache）
```
GOUACHE SPECIFIC:
- Opaque flat colors
- Clean edges and matte finish
- This is gouache painting, not digital art
- This is the artwork itself, NOT a photograph of a painting
- No paper edges, no background behind artwork
```

---

## 🎯 构图标准模板

### 局部特写（Extreme Close-up）
```
EXTREME CLOSE-UP DETAIL - MACRO VIEW:
- Show ONLY 2-3 individual flowers at extreme close range
- Fill the ENTIRE frame with flower details
- NO pot visible, NO stems below, NO leaves at bottom
- This is a MACRO botanical study
- Think: "looking through a magnifying glass"
```

### 中景视角（Mid-range View）
```
MID-RANGE VIEW - SHOW THE PLANT GROWING FROM POT:
- Show the COMPLETE plant growing naturally from the pot
- You must see: flowers at top → stems in middle → leaves → pot (upper half)
- This is ONE continuous plant, not separate elements
- The plant EMERGES from the pot and grows upward naturally
- Show ABUNDANT flowers - densely packed, LUSH and FULL
- Minimize empty space - create a full rich composition
- Pot bottom and base are cropped out
```

### 整体全景（Full Scene）
```
FULL SCENE - COMPLETE BOTANICAL DOCUMENTATION:
- Show 100% of plant from top to bottom
- Show 100% of pot from rim to base
- Include the surface the pot sits on
- This is the "specimen documentation" view
- CRITICAL DIFFERENCE from Mid-range: Mid-range crops pot bottom, Full Scene shows complete pot + base
```

### 意境氛围（Atmospheric Mood）
```
ATMOSPHERIC MOOD - ARTISTIC INTERPRETATION:
- BOTANICAL ACCURACY (MOST IMPORTANT): Plant MUST maintain exact characteristics from reference photo
- Flower shape, color, structure must match reference
- Do NOT change plant species or alter appearance
- Artistic interpretation is in ENVIRONMENT, not in changing plant
- This is NOT foreground+background composition
- Entire scene drawn/painted together as ONE unified artwork
```

---

## 🔍 生成后检查清单

### 第一眼检查
1. 看起来是手绘的吗？（不是照片转换）
2. 植物是从盆里生长的吗？（不是分离的）
3. 画面饱满吗？（不是稀疏空洞）
4. 这是一幅画吗？（不是拍摄画作）

### 细节检查
1. 能看到笔触吗？
2. 能看到纸张/画布质感吗？
3. 花朵、茎叶、花盆连接了吗？
4. 花朵密度够吗？

### 构图检查
1. 局部特写够近吗？（只有花朵）
2. 中景显示完整生长过程了吗？
3. 整体全景包含完整花盆和底座了吗？
4. 不同视角有明显区别吗？

---

## 🚑 常见问题快速修复

### 问题：看起来像照片滤镜
**修复**：添加 `HAND-DRAWN`, `VISIBLE STROKES`, `This is NOT a photo filter`

### 问题：有画纸边缘和背景
**修复**：添加 `This is the artwork itself, NOT a photograph of a drawing, No paper edges`

### 问题：花朵和花盆分离
**修复**：添加 `Show COMPLETE plant growing from pot, flowers → stems → leaves → pot, ONE continuous plant`

### 问题：构图差异不明显
**修复**：使用具体的百分比和裁切说明，明确不同视角的区别

### 问题：花朵稀少留白多
**修复**：添加 `ABUNDANT flowers, LUSH and FULL, Minimize empty space`

---

## 📚 参考文档

- 完整优化记录：`complete-optimization-record.md`
- 反面案例库：`anti-patterns-cases.md`
- 用户审美偏好：`user-aesthetic-preferences.md`
- 跨画风问题分析：`cross-style-issue-analysis.md`

---

**创建时间**：2026-02-02
**适用范围**：所有插画风格生成
