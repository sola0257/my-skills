# 配图生成反面案例库（Anti-Patterns）

> **用途**：记录坚决不要生成的错误效果，作为负面参考
> **更新日期**：2026-01-31

---

## ⚠️ 使用说明

本文档记录的是**反面案例**，即**坚决不要生成**的错误效果。

每个案例包含：
- 错误图片的描述
- 具体问题分析
- 正确的 prompt 应该如何写

---

## 案例1：封面图 - 英文标注问题

### 错误示例描述

**文件**：`年宵花与家居风格搭配_封面.png`

**错误 Prompt**：
```
A 3:4 split-screen comparison image for Xiaohongshu cover.
Left side: "Wrong Match" - A beautiful white orchid placed on a cluttered, messy table.
Right side: "Perfect Match" - The SAME white orchid placed on a clean, minimalist coffee table.
Main Title Overlay in the center/top: "选对位置 高级翻倍".
```

### 问题分析

1. **英文标注问题**：
   - ❌ 图片中出现了 "Wrong Match" 和 "Perfect Match" 英文标注
   - ❌ 违反了 `NO ENGLISH TEXT` 约束

2. **主题理解错误**：
   - ❌ 文章主题是"年宵花与家居风格搭配"，不是"位置选择"
   - ❌ 左侧应该展示"风格不搭配"，而不是"位置不对"
   - ❌ 对比点应该是"风格杂乱 vs 风格协调"，而不是"杂乱 vs 整洁"

3. **场景设计问题**：
   - ❌ 左侧场景过于杂乱，但问题不是"位置"，而是"风格不搭"

### 正确的 Prompt 应该这样写

```
A 3:4 split-screen comparison photograph for Xiaohongshu cover.
Left side: White orchid in a modern minimalist room but surrounded by conflicting decor styles (traditional Chinese vase, industrial metal shelf, bohemian textiles), creating visual chaos and style mismatch.
Right side: The SAME white orchid in a cohesive modern minimalist room with unified style (clean lines, neutral tones, consistent materials), creating harmony and high-end feel.
Center overlay: Chinese text "选对风格 高级翻倍" in bold clear handwritten font.
Lighting: Soft natural light, realistic home environment.
Color palette: Muted Morandi colors, desaturated tones.
Style: Realistic lifestyle photography, high contrast comparison.
NO ENGLISH TEXT. NO PEOPLE. NO STUDIO LIGHTING.
```

**关键改进**：
- ✅ 完全移除英文标注
- ✅ 对比点改为"风格不搭 vs 风格协调"
- ✅ 左侧场景改为"风格冲突"而非"杂乱"

---

## 案例2：手绘图 - 大量英文标注

### 错误示例描述

**文件**：`年宵花与家居风格搭配_04.png`（避坑指南）

**错误 Prompt**：
```
A 3:4 infographic in hand-drawn sketchnote style.
Topic: "Pitfall Guide".
Left side: Too many different colorful flowers crowded together. Label: "❌ 贪多杂乱".
Right side: One or two flowers with breathing space. Label: "✅ 适当留白".
```

### 问题分析

1. **大量英文标注**：
   - ❌ 图片中出现："Pitfall Guide", "Too many varieties!", "No room!", "Messy!", "Balance", "Air flow growth", "Less is More", "Focus on Quality"
   - ❌ 英文占比远超中文

2. **标题英文化**：
   - ❌ "Pitfall Guide" 应该是中文"避坑指南"

### 正确的 Prompt 应该这样写

```
A 3:4 infographic in hand-drawn sketchnote style.
Topic: 避坑指南
Title at top: "避坑指南" in clear bold handwritten Chinese font.
Structure: Split comparison, left side vs right side.
Left side: 多种颜色的花挤在一起，品种繁多，空间拥挤。Label: "❌ 贪多杂乱" in clear handwriting. Additional notes: "品种太多" "没有空间" "视觉混乱".
Right side: 一两盆花，留有呼吸空间，整洁有序。Label: "✅ 适当留白" in clear handwriting. Additional notes: "平衡感" "空气流通" "健康生长".
Visual elements: Simple icons, arrows, comparison layout.
Background: Clean white or lined notebook paper.
Color palette: Functional colors for categorization, yellow highlighter accents.
Style: Educational sketchnote aesthetic.
Chinese text must use clear, legible handwritten style font similar to marker or brush pen writing.
NO ENGLISH TEXT.
```

**关键改进**：
- ✅ 所有标注改为中文
- ✅ 标题改为中文"避坑指南"
- ✅ 补充说明也用中文

---

## 案例3：真实感图片 - AI感太重 + 逻辑错误

### 错误示例描述

**文件**：`06_盆底新根.png`、`07_表土新根.png`

**问题场景**：展示植物的新根生长

### 问题分析

1. **AI感太重**：
   - ❌ 根系看起来很假，不真实
   - ❌ 缺少真实的土壤质感和植物细节

2. **逻辑错误**：
   - ❌ 植物都没了，只看到根
   - ❌ 无法理解"植物生长出来的新根"的概念
   - ❌ 应该能看到植物本体和新根的关系

3. **构图问题**：
   - ❌ 焦点错误：应该同时展示植物和新根，而不是只展示根

### 正确的 Prompt 应该这样写

**盆底新根**：
```
A 3:4 photograph in dreamy realistic style.
Scene: A hand gently lifting a potted plant to show the bottom of the pot, where healthy white new roots are visible emerging from the drainage holes. The plant itself (leaves and stems) is clearly visible in the upper part of the image, showing it's a thriving plant with new root growth.
Lighting: Soft natural window light, warm golden hour glow.
Details: Ceramic pot with drainage holes, healthy white roots emerging, visible soil, the plant's leaves in frame, authentic home environment.
Mood: Educational, hopeful, showing healthy growth.
Color palette: Muted Morandi colors, desaturated tones, cream and sage.
Style: Realistic lifestyle photography, educational feel, NOT overly stylized AI art.
Text overlay: Add Chinese text "盆底新根" in a natural handwritten style, positioned in the lower right corner, using a soft cream color.
Image size: 1080x1440 pixels (3:4 vertical format).
NO ENGLISH TEXT. NO PEOPLE FACES. NO STUDIO LIGHTING.
IMPORTANT: The plant must be visible in the image, not just the roots. Show the relationship between the plant and its new roots.
```

**表土新根**：
```
A 3:4 photograph in dreamy realistic style.
Scene: Top-down view of a potted plant, with a small wooden tool gently moving aside the top layer of soil to reveal healthy white new roots just below the surface. The plant's stems and leaves are clearly visible, showing it's actively growing.
Lighting: Soft natural window light, warm golden hour glow.
Details: Ceramic pot, dark soil, white new roots visible in the soil, wooden tool, plant stems and leaves in frame, authentic home environment.
Mood: Educational, discovery, showing healthy growth.
Color palette: Muted Morandi colors, desaturated tones, cream and sage.
Style: Realistic lifestyle photography, educational feel, NOT overly stylized AI art.
Text overlay: Add Chinese text "表土新根" in a natural handwritten style, positioned in the upper right corner, using a soft cream color.
Image size: 1080x1440 pixels (3:4 vertical format).
NO ENGLISH TEXT. NO PEOPLE FACES. NO STUDIO LIGHTING.
IMPORTANT: The plant must be visible in the image, not just the roots and soil. Show the relationship between the plant and its new roots.
```

**关键改进**：
- ✅ 强调"植物本体必须可见"
- ✅ 强调"展示植物和新根的关系"
- ✅ 添加 `NOT overly stylized AI art` 约束，减少AI感
- ✅ 详细描述场景，确保逻辑合理

---

## 案例4：真实感图片 - 内容与主题无关 + 家居风格破旧

### 错误示例描述

**文件**：`08_光照管理.png`

**主题**：光照管理

### 问题分析

1. **内容与主题无关**：
   - ❌ 图片看不出与"光照管理"的关系
   - ❌ 应该展示植物与光照的关系（如窗边的植物、光线照射等）

2. **家居风格破旧**：
   - ❌ 地板上有很重的脚印（不合理，现代家居不会有这种痕迹）
   - ❌ 整体风格太破旧，不符合现代家居审美
   - ❌ 缺少现代感和高级感

3. **细节不合理**：
   - ❌ 木地板上的脚印太重，不符合真实生活场景

### 正确的 Prompt 应该这样写

```
A 3:4 photograph in dreamy realistic style.
Scene: A lush green plant placed near a bright window in a modern living room, with soft natural sunlight streaming through sheer curtains, creating beautiful light patterns on the plant's leaves. The room has clean, modern furniture and well-maintained wooden floor.
Lighting: Soft natural window light, warm golden hour glow, gentle shadows, visible light rays.
Details: Modern window with sheer curtains, healthy plant with vibrant leaves, clean wooden floor (no footprints or damage), modern minimalist furniture, authentic but well-maintained home environment.
Mood: Bright, healthy, showing ideal light conditions for plants.
Color palette: Muted Morandi colors, desaturated tones, cream and sage.
Style: Realistic lifestyle photography, modern home aesthetic, NOT old or worn-out interior.
Text overlay: Add Chinese text "循序渐进" in a natural handwritten style, positioned in the upper right corner, using a soft cream color.
Image size: 1080x1440 pixels (3:4 vertical format).
NO ENGLISH TEXT. NO PEOPLE. NO STUDIO LIGHTING.
IMPORTANT: The image must clearly show the relationship between the plant and natural light. The home interior must look modern, clean, and well-maintained, NOT old or damaged.
```

**关键改进**：
- ✅ 明确展示"植物与光照的关系"
- ✅ 强调"现代、整洁、维护良好的家居环境"
- ✅ 添加 `NOT old or worn-out interior` 约束
- ✅ 强调"无脚印、无损坏"

---

## 🎯 反面案例总结

### 核心问题类型

1. **英文标注问题**
   - 封面图、手绘图中出现英文
   - 违反 `NO ENGLISH TEXT` 约束

2. **主题理解错误**
   - 对比点选择错误
   - 内容与主题无关

3. **AI感太重**
   - 图片看起来很假
   - 缺少真实感和细节

4. **逻辑错误**
   - 植物消失，只看到局部
   - 无法理解要表达的概念

5. **家居风格问题**
   - 太破旧，不符合现代审美
   - 细节不合理（如地板脚印）

### 强制约束（必须遵守）

1. **NO ENGLISH TEXT**（绝对禁止）
2. **现代家居风格**（clean, modern, well-maintained）
3. **逻辑合理性**（主体必须可见，关系必须清晰）
4. **真实感优先**（NOT overly stylized AI art）
5. **主题相关性**（内容必须与主题直接相关）

---

**最后更新**：2026-01-31
