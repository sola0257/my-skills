# 案例 002：小红书多肉养护封面（3:4 竖版，带文字）

> **返回索引**：[案例库索引](./README.md)

## 📋 基本信息

- **来源平台**：小红书
- **适用平台**：小红书（优先）、其他竖版平台需调整比例
- **验证状态**：✅ 已验证（2026-01-30）
- **文章主题**：多肉养护避坑指南
- **图片类型**：封面图（dreamy-photo 风格 + 文字叠加）
- **迭代次数**：3次
- **最终文件**：cover_养了2年多肉才明白：新手最容易犯的3个错误_v2.png

### ✅ 最终确认的 Prompt

```
A 3:4 photograph in dreamy realistic style for Xiaohongshu cover.

Scene: Simple windowsill with 2-3 succulent plants in ceramic pots, clean and minimalist composition, authentic home environment, lived-in atmosphere. The background is a plain cream or light grey wall, very simple and uncluttered. The succulents are arranged naturally but not crowded on a wooden surface.

Lighting: Soft natural morning light from window, warm golden hour glow, gentle shadows.

Details: 2-3 succulent varieties in muted ceramic pots (sage green, cream, dusty rose colors), wooden windowsill, clean simple background, generous negative space in upper portion.

Mood: Peaceful, clean, minimalist, cozy, inviting.

Color palette: Muted Morandi colors, desaturated tones, cream and sage green, dusty rose accents.

Color control: Use dusty coral instead of red, muted rose instead of pink, soft terracotta for warm accents.

Style: Realistic lifestyle photography, soft focus, film-like quality, NOT product photography, editorial clean aesthetic.

Composition: Leave generous empty space in the top 1/3 of the image. The plants should be in the middle and lower portion.

TEXT OVERLAY REQUIREMENTS (CRITICAL):
Add Chinese text at the top center of the image:
Line 1: "养了2年多肉才明白："
Line 2: "新手最容易犯的3个错误"

Text style (MUST FOLLOW EXACTLY):
- Font: Bold, thick, chunky Chinese font (similar to impact or heavy bold style)
- Color: Pure white (#FFFFFF) with a black stroke/outline
- Stroke: 4-6 pixel black outline around white text for maximum contrast and clarity
- Size: Large and prominent (占据顶部约1/4空间)
- Position: Top center, horizontally centered
- Spacing: Moderate line spacing between the two lines
- Effect: The text should look SHARP, CLEAR, and BOLD - like professional graphic design text overlay, NOT handwritten style

The text should be highly visible and readable, with strong contrast against any background. The black outline should make the white text pop out clearly.

Image size: 1080x1440 pixels (3:4 vertical format for Xiaohongshu).

NO ENGLISH TEXT. NO PEOPLE. NO STUDIO LIGHTING.
```

### 🔒 固定部分（不要修改）

#### 1. 封面文字设计规范（高点赞率特征）

```
TEXT OVERLAY REQUIREMENTS (CRITICAL):
- Font: Bold, thick, chunky Chinese font
- Color: Pure white (#FFFFFF) with 4-6px black stroke
- Size: Large and prominent (占据顶部约1/4空间)
- Position: Top center, horizontally centered
- Effect: SHARP, CLEAR, and BOLD
```

**关键要素**：
- ✅ 白色粗体字 + 黑边（最重要）
- ✅ 字号大（占顶部1/4-1/3）
- ✅ 顶部居中
- ✅ 清晰锐利（不是手写风格）

**为什么这些重要**：
- 白色+黑边在任何背景下都清晰可见
- 大字号确保缩略图也能看清
- 顶部居中符合小红书高互动内容的视觉习惯

#### 2. 背景简洁原则

```
Scene: Simple windowsill with 2-3 succulent plants, clean and minimalist composition, plain cream or light grey wall, very simple and uncluttered.
Composition: Leave generous empty space in the top 1/3 of the image.
```

**关键词**：
- ✅ `Simple` - 简洁
- ✅ `2-3` - 不要太多物品
- ✅ `plain cream or light grey wall` - 纯色浅色背景
- ✅ `very simple and uncluttered` - 非常简洁不杂乱
- ✅ `generous empty space in the top 1/3` - 顶部留白给文字

**避免**：
- ❌ 背景过于复杂（多个物品、杂乱）
- ❌ 主体太多（5+个物品）
- ❌ 没有留白空间

#### 3. 三层结构布局

```
顶部（1/3）：文字层 + 留白
中部：呼吸空间
底部（2/3）：主体物品
```

**关键原则**：
- ✅ 上下分区明确
- ✅ 文字不遮挡主体
- ✅ 有足够呼吸空间

### 🔄 可调整部分（根据具体内容修改）

#### 1. 主体物品

```
Details: 2-3 succulent varieties in muted ceramic pots (sage green, cream, dusty rose colors)
```

**可替换**：
- 物品类型：succulents → 其他植物、物品
- 数量：2-3（保持简洁）
- 颜色：根据主题调整（但保持莫兰迪色系）

#### 2. 文字内容

```
Line 1: "养了2年多肉才明白："
Line 2: "新手最容易犯的3个错误"
```

**可替换**：
- 根据具体标题修改
- 建议分两行（更易读）
- 保持口语化、情绪化

**保持**：
- 白色粗体+黑边的样式
- 顶部居中的位置
- 大字号

### 📊 高点赞率封面设计检查清单

生成小红书封面后，检查：

- [ ] 文字是否清晰（白色粗体+黑边）
- [ ] 文字是否够大（缩略图也能看清）
- [ ] 背景是否简洁（不杂乱）
- [ ] 主体是否突出（2-3个物品）
- [ ] 上下分区是否明确
- [ ] 色调是否温馨（莫兰迪色系）
- [ ] 光线是否自然（不是棚拍）
- [ ] 是否有生活感（真实场景）

### 🎯 实施建议

**统一方案：使用 Gemini API 生成带文字的封面**

**方式1：一步生成（推荐）**

优势：
- 一次性完成，效率高
- 文字和背景自然融合
- 文字清晰、粗壮、有力
- 黑边效果好

实施：
- 在 prompt 中同时指定场景和文字要求
- 使用 `gemini-3-pro-image-preview` 模型
- 参考本案例的完整 prompt

**方式2：两步生成（可选）**

优势：
- 可以先确认底图效果
- 文字可以单独调整

实施：
- 第一步：Gemini 生成封面底图（prompt 中不包含文字要求）
- 第二步：Gemini 在底图基础上添加文字（prompt 中指定文字叠加）

**不推荐：PIL 后期添加文字**

原因：
- 文字可能不够清晰
- 黑边效果不如 Gemini
- 需要调试参数
- 效果不如 AI 生成

---

**相关案例**：
- [案例 001：微信公众号君子兰封面](./case-001-wechat-cover.md)
- [案例 003：小红书真实场景图（手写文字）](./case-003-xhs-scene.md)

**返回**：[案例库索引](./README.md)
