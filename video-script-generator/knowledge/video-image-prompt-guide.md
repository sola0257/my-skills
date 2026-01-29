# 视频脚本配图生成指南 v1.0

**版本**：v1.0
**创建日期**：2026-01-29
**用途**：为视频脚本生成提供详细的配图规范和 prompt 模板

---

## 🎬 视频生成原理

**重要**：视频是通过多张静态图 + 运镜 + 转场来实现动态效果

### 配图节奏

**时间规则**：每3-5秒配一张静态图
**计算公式**：配图数量 = 视频时长（秒）÷ 4（平均值）

**示例**：
- 30秒视频 → 7-10张配图
- 1分钟视频 → 12-20张配图
- 3分钟视频 → 36-60张配图

### 配图要求

**连贯性**：
- 相邻配图风格要统一
- 色调要协调
- 场景要有逻辑关联

**运镜适配**：
- 推进镜头：从远到近的构图
- 拉远镜头：从近到远的构图
- 平移镜头：横向构图，留出移动空间

**转场适配**：
- 淡入淡出：色调相近
- 切换：对比明显
- 推拉：景深变化

---

## 📐 平台尺寸规范

### 四平台配图尺寸

| 平台 | 封面尺寸 | 分镜配图尺寸 | 说明 |
|------|---------|-------------|------|
| **小红书** | 3:4竖版（1080×1440） | 3:4竖版 | 竖屏观看 |
| **视频号** | 3:4竖版（1080×1440） | 3:4竖版 | 竖屏观看 |
| **快手** | 9:16竖版（1080×1920） | 9:16竖版 | 全屏竖版 |
| **抖音** | 9:16竖版（1080×1920） | 9:16竖版 | 全屏竖版 |

### 尺寸选择规则

**默认**：如果用户未指定平台，生成3:4竖版（适配小红书/视频号）

**多平台**：如果需要全平台发布，优先生成9:16竖版（可裁剪为3:4）

---

## 🎨 配图风格规则

### 封面图风格

**选择依据**：按照视频整体类型选择

**知识分享类**：
- 风格：真实感、专业感
- 关键词：`realistic`, `documentary photography`, `educational`
- 色调：Morandi 色系、低饱和度

**生活感悟类**：
- 风格：治愈感、氛围感
- 关键词：`dreamy`, `soft focus`, `lifestyle photography`
- 色调：温暖色调、柔和光线

### 分镜配图风格

**选择依据**：按照对应分镜内容选择

**场景类分镜**：
- 风格：真实感场景
- Prompt 模板：`A realistic [场景描述]...`

**特写类分镜**：
- 风格：细节特写
- Prompt 模板：`A close-up of [对象]...`

**氛围类分镜**：
- 风格：意境营造
- Prompt 模板：`A dreamy scene showing [氛围]...`

---

## 📝 Prompt 模板库

### 封面图 Prompt

#### 知识分享类封面

**3:4竖版**：
```
A [尺寸] vertical format cover image for educational video.
Subject: [主题相关视觉元素]
Scene: [场景描述], authentic home environment
Lighting: Natural soft lighting, professional but approachable
Composition: Centered subject, rule of thirds, vertical framing
Style: Documentary photography, realistic, educational feel
Color: Muted Morandi palette, desaturated tones
NO TEXT, NO WORDS, NO LETTERS.
```

**9:16竖版**：
```
A 9:16 ultra-vertical format cover image for short video.
Subject: [主题相关视觉元素]
Scene: [场景描述], full-screen vertical composition
Lighting: Natural lighting, cinematic feel
Composition: Vertical framing, subject fills frame, dynamic angle
Style: Modern short video aesthetic, realistic
Color: Vibrant but natural, eye-catching
NO TEXT, NO WORDS, NO LETTERS.
```

#### 生活感悟类封面

**3:4竖版**：
```
A [尺寸] vertical format cover image for lifestyle video.
Subject: [情感相关意象]
Scene: [治愈场景], lived-in atmosphere, cozy setting
Lighting: Soft golden hour light, warm and inviting
Composition: Dreamy vertical framing, generous negative space
Style: Lifestyle photography, soft focus, film-like quality
Color: Warm tones, muted pastels, gentle atmosphere
NO TEXT, NO WORDS, NO LETTERS.
```

---

### 分镜配图 Prompt

#### 场景类分镜

**真实场景**：
```
A [尺寸] vertical format scene for video frame.
Scene: [具体场景描述]
Details: [场景细节元素]
Lighting: [光线描述]
Mood: [情绪氛围]
Composition: [构图说明 - 考虑运镜方向]
Style: Realistic, documentary feel, natural
Color: [色调要求]
Camera angle: [镜头角度 - 适配运镜]
NO TEXT, NO WORDS, NO LETTERS.
```

**示例（推进镜头）**：
```
A 3:4 vertical format scene for video frame with push-in camera movement.
Scene: A cozy living room corner with plants on wooden shelf
Details: Multiple potted plants, natural wood furniture, soft textiles
Lighting: Warm afternoon sunlight through window
Mood: Calm, inviting, homey
Composition: Wide shot with subject in center, space for camera to push in
Style: Realistic lifestyle photography, natural feel
Color: Muted Morandi tones, warm wood and green accents
Camera angle: Eye level, straight on, ready for push-in movement
NO TEXT, NO WORDS, NO LETTERS.
```

#### 特写类分镜

**细节特写**：
```
A [尺寸] vertical format close-up for video frame.
Subject: [特写对象]
Details: [细节描述]
Focus: Sharp focus on [焦点], shallow depth of field
Lighting: [光线描述]
Composition: [构图 - 考虑转场]
Style: Macro photography, detailed, realistic
Color: [色调]
NO TEXT, NO WORDS, NO LETTERS.
```

**示例（淡入淡出转场）**：
```
A 3:4 vertical format close-up for video frame with fade transition.
Subject: Plant leaves with water droplets
Details: Fresh green leaves, morning dew, soft texture
Focus: Sharp focus on droplets, blurred background
Lighting: Soft morning light, backlit for glow
Composition: Centered subject, soft edges for smooth fade
Style: Macro photography, dreamy, natural
Color: Soft greens and whites, gentle tones for easy transition
NO TEXT, NO WORDS, NO LETTERS.
```

#### 氛围类分镜

**意境营造**：
```
A [尺寸] vertical format atmospheric shot for video frame.
Mood: [情绪关键词]
Scene: [意境场景]
Elements: [氛围元素]
Lighting: [光线氛围]
Composition: [构图 - 留白]
Style: Dreamy, soft focus, cinematic
Color: [色调氛围]
NO TEXT, NO WORDS, NO LETTERS.
```

---

## 🎬 运镜适配策略

### 推进镜头（Push In）

**配图要求**：
- 构图：从远到近，主体居中
- 景深：有层次感
- 细节：远景有环境，近景有细节

**Prompt 关键词**：
```
wide shot with subject in center
space for camera to push in
layered composition with depth
```

### 拉远镜头（Pull Out）

**配图要求**：
- 构图：从近到远，逐渐展开
- 环境：周围有丰富场景
- 过渡：自然扩展

**Prompt 关键词**：
```
close-up with room to reveal surroundings
environmental context visible
expandable composition
```

### 平移镜头（Pan）

**配图要求**：
- 构图：横向延展
- 空间：左右留出移动空间
- 连贯：相邻画面有关联

**Prompt 关键词**：
```
horizontal composition
space on sides for panning
continuous scene elements
```

### 静止镜头（Static）

**配图要求**：
- 构图：稳定平衡
- 焦点：明确清晰
- 持续：画面可停留

**Prompt 关键词**：
```
balanced composition
clear focal point
stable framing
```

---

## 🔄 转场适配策略

### 淡入淡出（Fade）

**配图要求**：
- 色调：相近或渐变
- 边缘：柔和
- 氛围：连贯

**相邻配图示例**：
```
图A: Soft morning light, muted greens, gentle atmosphere
图B: Warm afternoon light, muted browns, calm mood
→ 色调相近，氛围连贯，适合淡入淡出
```

### 切换（Cut）

**配图要求**：
- 对比：明显
- 节奏：清晰
- 冲击：适度

**相邻配图示例**：
```
图A: Close-up of plant leaves, green, detailed
图B: Wide shot of room, warm tones, environmental
→ 景别对比，适合直接切换
```

### 推拉转场

**配图要求**：
- 景深：变化明显
- 主体：保持关联
- 过渡：自然

---

## 📊 配图数量规划

### 根据视频时长

| 视频时长 | 配图数量 | 说明 |
|---------|---------|------|
| 15秒 | 4-5张 | 快节奏，每3-4秒一张 |
| 30秒 | 7-10张 | 标准节奏，每3-4秒一张 |
| 1分钟 | 12-20张 | 标准节奏，每3-5秒一张 |
| 2分钟 | 24-40张 | 标准节奏，每3-5秒一张 |
| 3分钟 | 36-60张 | 标准节奏，每3-5秒一张 |

### 根据视频类型

**知识分享类**：
- 节奏：稍慢，每4-5秒一张
- 原因：需要时间理解内容

**生活感悟类**：
- 节奏：稍快，每3-4秒一张
- 原因：氛围营造，画面流动

---

## ✅ 配图生成检查清单

### 生成前检查

- [ ] 已确定目标平台（决定尺寸）
- [ ] 已确定视频时长（决定数量）
- [ ] 已确定视频类型（决定风格）
- [ ] 已规划运镜方式（决定构图）
- [ ] 已规划转场方式（决定色调）

### 生成后检查

- [ ] 配图数量符合时长要求
- [ ] 配图尺寸符合平台规格
- [ ] 相邻配图风格连贯
- [ ] 色调适配转场方式
- [ ] 构图适配运镜方式
- [ ] 封面突出主题

---

## 🎯 实战示例

### 示例1：30秒知识分享类视频（小红书）

**视频信息**：
- 时长：30秒
- 类型：知识分享类
- 平台：小红书
- 主题：多肉浇水技巧

**配图规划**：
- 尺寸：3:4竖版（1080×1440）
- 数量：8张（封面1张 + 分镜7张）
- 节奏：每4-5秒一张

**配图列表**：
1. 封面：多肉植物特写，真实感
2. 分镜1：浇水前的多肉（静止镜头）
3. 分镜2：浇水动作特写（推进镜头）
4. 分镜3：水滴在土壤上（特写）
5. 分镜4：健康多肉对比（切换）
6. 分镜5：烂根多肉对比（切换）
7. 分镜6：正确浇水示范（平移镜头）
8. 分镜7：养护后的效果（拉远镜头）

### 示例2：1分钟生活感悟类视频（抖音）

**视频信息**：
- 时长：1分钟
- 类型：生活感悟类
- 平台：抖音
- 主题：植物陪伴的治愈时光

**配图规划**：
- 尺寸：9:16竖版（1080×1920）
- 数量：16张（封面1张 + 分镜15张）
- 节奏：每3-4秒一张

**配图列表**：
1. 封面：温馨植物角落，治愈氛围
2-16. 分镜：按照逐字稿内容，每3-4秒一张，淡入淡出转场

---

**最后更新**：2026-01-29
**版本**：v1.0
