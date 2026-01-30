# 微信公众号配图生成成功案例库

> **目的**：记录经过实际验证的成功 prompt，避免重复试错
> **使用方法**：生成类似内容时，参考对应案例的固定部分，只调整可变部分

---

## 📖 使用规则

### 优先级原则
1. **优先参考本平台案例**：微信公众号生成配图时，优先参考标注为"微信公众号"的案例
2. **跨平台参考**：如果本平台没有合适案例，可以参考其他平台的案例，但需要调整比例和尺寸
3. **案例标注**：每个案例都会标注来源平台、适用场景、验证状态

### 案例标注说明
- **来源平台**：案例最初在哪个平台验证成功
- **适用平台**：案例可以应用到哪些平台（需要调整比例）
- **验证状态**：✅ 已验证 | 🔄 待验证 | ⚠️ 需要优化

---

## 案例 1：君子兰冬季养护封面图（2.35:1 横版）

### 📋 基本信息

- **来源平台**：微信公众号（订阅号长文）
- **适用平台**：微信公众号（优先）、其他平台需调整比例
- **验证状态**：✅ 已验证（2026-01-29）
- **文章主题**：君子兰冬季养护
- **图片类型**：封面图（dreamy-photo 风格）
- **迭代次数**：6次
- **最终文件**：cover_final.png

### ✅ 最终确认的 Prompt

```
Generate an image: A 2.35:1 wide banner photograph in dreamy realistic style.
Scene: A healthy Clivia miniata plant on a clean modern windowsill in a bright contemporary living room, authentic home environment with modern aesthetic.
Plant details: Healthy Clivia miniata with natural flower stalks in dusty coral and soft terracotta tones, in a cream ceramic pot, vibrant but not artificial, flowers in natural bloom with organic arrangement, leaves in healthy green with natural growth pattern.
Lighting: Soft natural window light, warm golden hour glow, gentle shadows creating depth.
Details: Modern windowsill with clean lines, contemporary home interior in background, minimalist decor elements, fresh and current aesthetic, well-maintained modern space.
Mood: Calm, educational, welcoming, winter care atmosphere, natural and inviting, contemporary lifestyle.
Color palette: Muted Morandi colors, desaturated tones, cream and sage, dusty coral flower accents, soft terracotta, warm wood.
Color control: Use dusty coral instead of bright orange, soft terracotta for warm accents, desaturated color palette, low saturation throughout, Morandi color scheme.
Style: Realistic lifestyle photography, soft focus, film-like quality, editorial feel, natural but healthy plant, modern home setting, NOT product photography, NOT studio lighting.
NO TEXT. NO WORDS. NO LETTERS. NO PEOPLE. NO STUDIO LIGHTING. NO BRIGHT COLORS.
```

### 🔒 固定部分（不要修改）

这些部分经过多次迭代确认，修改会导致质量下降：

#### 1. 植物描述（健康且真实的平衡）
```
Plant details: Healthy Clivia miniata with natural flower stalks in dusty coral and soft terracotta tones, in a cream ceramic pot, vibrant but not artificial, flowers in natural bloom with organic arrangement, leaves in healthy green with natural growth pattern.
```

**关键词**：
- ✅ `Healthy` - 确保植物健康有活力
- ✅ `vibrant but not artificial` - 有活力但不假
- ✅ `natural bloom` - 自然盛开状态
- ✅ `organic arrangement` - 有机排列（不是完美对称）
- ✅ `natural growth pattern` - 自然生长模式

**避免使用**：
- ❌ `elegant`, `perfect`, `multiple flower stalks` - 导致过于完美
- ❌ `natural imperfections`, `some leaves may show aging` - 导致不健康外观
- ❌ `NOT perfect specimen` - 过度强调不完美

#### 2. 颜色控制（真实感的核心）
```
Color palette: Muted Morandi colors, desaturated tones, cream and sage, dusty coral flower accents, soft terracotta, warm wood.
Color control: Use dusty coral instead of bright orange, soft terracotta for warm accents, desaturated color palette, low saturation throughout, Morandi color scheme.
```

**关键词**：
- ✅ `Muted Morandi colors` - 莫兰迪色系
- ✅ `desaturated tones` - 降低饱和度
- ✅ `dusty coral` - 替代鲜艳的橙色/红色
- ✅ `soft terracotta` - 柔和的陶土色

#### 3. 光线和氛围
```
Lighting: Soft natural window light, warm golden hour glow, gentle shadows creating depth.
Mood: Calm, educational, welcoming, winter care atmosphere, natural and inviting, contemporary lifestyle.
```

**关键词**：
- ✅ `Soft natural window light` - 柔和自然窗光
- ✅ `warm golden hour glow` - 温暖的黄金时段光线
- ✅ `gentle shadows` - 柔和阴影

#### 4. 风格约束
```
Style: Realistic lifestyle photography, soft focus, film-like quality, editorial feel, natural but healthy plant, modern home setting, NOT product photography, NOT studio lighting.
NO TEXT. NO WORDS. NO LETTERS. NO PEOPLE. NO STUDIO LIGHTING. NO BRIGHT COLORS.
```

**关键约束**：
- ✅ `Realistic lifestyle photography` - 真实生活摄影
- ✅ `film-like quality` - 胶片质感
- ✅ `editorial feel` - 编辑感
- ✅ `natural but healthy plant` - 自然但健康的植物
- ❌ `NOT product photography` - 不是产品摄影
- ❌ `NOT studio lighting` - 不是棚拍

### 🔄 可调整部分（根据具体内容修改）

#### 1. 场景描述
```
Scene: A healthy Clivia miniata plant on a clean modern windowsill in a bright contemporary living room, authentic home environment with modern aesthetic.
```

**可替换**：
- 植物名称：`Clivia miniata` → 其他植物
- 场景位置：`windowsill` → `coffee table`, `shelf`, `desk`
- 空间类型：`living room` → `bedroom`, `study`, `balcony`

**保持**：
- `clean modern` - 现代清爽
- `bright contemporary` - 明亮当代
- `authentic home environment` - 真实家居环境
- `modern aesthetic` - 现代美学

#### 2. 环境细节
```
Details: Modern windowsill with clean lines, contemporary home interior in background, minimalist decor elements, fresh and current aesthetic, well-maintained modern space.
```

**可替换**：
- 具体装饰元素
- 背景物品

**保持**：
- `modern`, `contemporary`, `minimalist` - 现代简约风格
- `clean lines` - 简洁线条
- `fresh and current aesthetic` - 新鲜当代美感
- `well-maintained` - 维护良好

#### 3. 情绪关键词
```
Mood: Calm, educational, welcoming, winter care atmosphere, natural and inviting, contemporary lifestyle.
```

**可替换**：
- 季节：`winter care` → `spring growth`, `summer blooming`
- 具体情绪词

**保持**：
- `Calm`, `welcoming`, `natural and inviting` - 平静、欢迎、自然
- `contemporary lifestyle` - 当代生活方式

### 📊 迭代过程总结

| 版本 | 主要问题 | 调整内容 | 结果 |
|------|---------|---------|------|
| v1 (cover.png) | 花有些假 | 初始版本 | 场景真实，花不够真实 |
| v4 (cover_v4.png) | 花发蔫、不健康 | 过度强调不完美 | 真实但不健康 ❌ |
| v5 (cover_v5.png) | 家居环境有些旧 | 平衡健康与真实 | 花朵效果好 ✅ |
| v6 (cover_v6.png) | 花又变假了 | 现代化家居环境 | 环境好，花变假 ❌ |
| **Final** | ✅ 满意 | 组合 v5 花朵 + v6 环境 | 两者兼顾 ✅ |

### 🎓 关键经验

#### 1. 真实感 ≠ 不健康
- ❌ 错误：添加 "natural imperfections", "aging leaves" 导致植物看起来发蔫
- ✅ 正确：使用 "healthy", "vibrant but not artificial", "natural but healthy"

#### 2. 避免完美 ≠ 要有缺陷
- ❌ 错误：使用 "NOT perfect specimen", "NO PERFECT FLOWERS"
- ✅ 正确：使用 "organic arrangement", "natural growth pattern"

#### 3. 现代感 ≠ 冷淡
- ❌ 错误：只强调 "modern" 可能导致冷淡感
- ✅ 正确：结合 "warm", "inviting", "welcoming" 保持温度

#### 4. 迭代策略
- ❌ 错误：每次大幅修改整个 prompt，导致之前调好的部分变差
- ✅ 正确：识别确认好的部分，只修改需要改进的部分

### ⚠️ 常见错误

#### 错误 1：过度强调不完美
```
❌ 错误示例：
"natural imperfections, some leaves may show natural aging,
flowers in natural arrangement not perfectly symmetrical"
```
**后果**：植物看起来发蔫、不健康

**正确做法**：
```
✅ 正确示例：
"vibrant but not artificial, flowers in natural bloom with
organic arrangement, leaves in healthy green with natural growth pattern"
```

#### 错误 2：使用鲜艳颜色词
```
❌ 错误示例：
"bright orange flowers, vivid red blooms, colorful arrangement"
```
**后果**：生成假的、棚拍感的图片

**正确做法**：
```
✅ 正确示例：
"dusty coral and soft terracotta tones, muted Morandi colors,
desaturated color palette"
```

#### 错误 3：场景描述过于老旧
```
❌ 错误示例：
"wooden windowsill, lived-in atmosphere, cozy lived-in setting,
books or small home accessories nearby"
```
**后果**：家居环境看起来老旧、过时

**正确做法**：
```
✅ 正确示例：
"clean modern windowsill, contemporary living room,
minimalist decor elements, fresh and current aesthetic"
```

### 🔧 使用建议

1. **生成类似植物封面图时**：
   - 直接使用本案例的固定部分
   - 只替换植物名称和场景位置
   - 保持颜色控制和风格约束不变

2. **调整时的优先级**：
   - 第一优先：保持颜色控制（真实感的核心）
   - 第二优先：保持植物健康描述（避免发蔫）
   - 第三优先：保持光线和风格约束
   - 最后：调整场景和环境细节

3. **验证清单**：
   - [ ] 是否包含 "muted", "desaturated", "dusty" 等饱和度控制词？
   - [ ] 是否强调 "healthy", "vibrant but not artificial"？
   - [ ] 是否避免了 "bright", "vivid", "perfect" 等词？
   - [ ] 是否包含 "natural window light", "film-like quality"？
   - [ ] 是否明确排除 "NOT product photography", "NOT studio lighting"？

---

## 使用模板

### 快速生成模板（基于案例 1）

```
Generate an image: A 2.35:1 wide banner photograph in dreamy realistic style.
Scene: A healthy [植物名称] on a clean modern [位置] in a bright contemporary [空间], authentic home environment with modern aesthetic.
Plant details: Healthy [植物名称] with natural flower stalks in dusty coral and soft terracotta tones, in a cream ceramic pot, vibrant but not artificial, flowers in natural bloom with organic arrangement, leaves in healthy green with natural growth pattern.
Lighting: Soft natural window light, warm golden hour glow, gentle shadows creating depth.
Details: Modern [位置] with clean lines, contemporary home interior in background, minimalist decor elements, fresh and current aesthetic, well-maintained modern space.
Mood: Calm, educational, welcoming, [季节] care atmosphere, natural and inviting, contemporary lifestyle.
Color palette: Muted Morandi colors, desaturated tones, cream and sage, dusty coral flower accents, soft terracotta, warm wood.
Color control: Use dusty coral instead of bright orange, soft terracotta for warm accents, desaturated color palette, low saturation throughout, Morandi color scheme.
Style: Realistic lifestyle photography, soft focus, film-like quality, editorial feel, natural but healthy plant, modern home setting, NOT product photography, NOT studio lighting.
NO TEXT. NO WORDS. NO LETTERS. NO PEOPLE. NO STUDIO LIGHTING. NO BRIGHT COLORS.
```

**填空说明**：
- `[植物名称]`：替换为具体植物（如 Monstera, Pothos, Fiddle Leaf Fig）
- `[位置]`：windowsill, coffee table, shelf, desk, plant stand
- `[空间]`：living room, bedroom, study, balcony
- `[季节]`：spring, summer, fall, winter

---

## 🔄 跨平台应用指南

### 如何将本案例应用到其他平台

#### 应用到小红书（3:4 竖版）

**需要调整**：
1. 比例：`A 2.35:1 wide banner` → `A 3:4 photograph`
2. 构图：`Wide horizontal layout` → `Vertical composition`
3. 尺寸：900×383px → 1080×1440px

**保持不变**：
- 颜色控制（muted Morandi colors）
- 植物健康描述（healthy, vibrant but not artificial）
- 光线和风格约束（natural window light, film-like quality）

#### 应用到视频号（9:16 竖版）

**需要调整**：
1. 比例：`A 2.35:1 wide banner` → `A 9:16 vertical`
2. 构图：适应竖屏构图
3. 尺寸：900×383px → 1080×1920px

**保持不变**：
- 所有核心约束（颜色、健康、光线、风格）

### 跨平台参考原则

1. **核心约束通用**：颜色控制、真实感约束、光线描述在所有平台都适用
2. **比例需调整**：根据目标平台调整比例描述
3. **构图需适配**：横版 vs 竖版的构图逻辑不同
4. **优先本平台**：如果本平台有成功案例，优先使用本平台案例

---

## 案例 2：小红书多肉养护封面（3:4 竖版，带文字）

### 📋 基本信息

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

*最后更新：2026-01-30*
*案例数量：1*
*支持平台：微信公众号（主）、小红书（需调整）、视频号（需调整）*
