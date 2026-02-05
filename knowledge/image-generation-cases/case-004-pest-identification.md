# 案例 004：病虫害识别图（示意图 + 真实参考图层）

> **返回索引**：[案例库索引](./README.md)

---

## 📋 基本信息

- **来源平台**：小红书
- **适用平台**：所有平台（教学型内容通用）
- **验证状态**：✅ 已验证（2026-01-31）
- **文章主题**：春季防虫大作战
- **图片类型**：病虫害识别图（教学型）
- **特殊要求**：必须准确，不能误导用户
- **最终解决方案**：AI生成教学示意图（75%）+ 真实参考图层（25%圆形inset）

---

## 🚨 核心原则（最高优先级）

### ⚠️ 教学型/识别型内容的特殊要求

**对于病虫害、疾病症状、植物问题诊断等教学型内容：**

1. **禁止生成虚假的"真实照片"**
   - ❌ 不能凭想象生成病虫害照片
   - ❌ 不能用 AI 生成完全"写实"的虫害图作为唯一参考
   - ⚠️ 原因：会误导用户，导致错误识别和处理

2. **采用示意图 + 真实参考的组合方案**
   - ✅ 主体：教学示意图（75%），简化特征，清晰标注
   - ✅ 辅助：真实参考图层（25%圆形inset），提供真实感参考
   - ✅ 基于准确的昆虫学特征生成（体长、颜色、形态）
   - ✅ 明确标注"示意图"，避免误导

3. **为什么这个方案可行**
   - ✅ AI 可以完全执行，无需手动下载图片
   - ✅ 示意图突出关键识别特征，易于理解
   - ✅ 真实参考图层提供视觉对照，增强可信度
   - ✅ 基于科学文献的准确特征描述

---

## 🎨 最终解决方案：示意图 + 真实参考图层

### 方案概述

**单张图片包含两个图层：**

```
┌─────────────────────────────────────┐
│                                     │
│  教学示意图（75%）        ┌─────┐  │
│  - 简化线条               │真实 │  │
│  - 清晰标注               │参考 │  │
│  - 识别要点框             │图层 │  │
│  - 中文说明               │25% │  │
│                           └─────┘  │
│  底部标注："示意图"                 │
└─────────────────────────────────────┘
```

### 核心优势

1. **完全可执行**：AI 一次性生成，无需手动操作
2. **教学清晰**：示意图突出关键特征，易于识别
3. **真实参考**：inset 提供真实感对照
4. **准确可靠**：基于科学文献的特征描述

---

## 📐 Prompt 结构模板

### 通用模板

```
Educational schematic diagram for [pest name] identification with realistic reference inset.

Main layer (75% of image):
- Clean, simplified schematic illustration showing key identification features
- Muted educational colors: [color palette]
- Simple line art style with clear outlines
- Chinese labels pointing to key features

Key features to highlight in schematic:
- [Feature 1: size, shape, color]
- [Feature 2: distinctive markings]
- [Feature 3: typical location]
- [Feature 4: damage symptoms]

Realistic reference inset (25% of image):
- Circular frame in upper right corner
- Macro photography style showing actual pest appearance
- Realistic details: [specific visual details]
- Natural lighting, sharp focus on pest details

Knowledge points box on left side with Chinese text:
识别要点：
• [识别点1]
• [识别点2]
• [识别点3]
• [识别点4]

Text requirements:
- All Chinese text must be SHARP, CLEAR, and LEGIBLE
- Use clean sans-serif font
- High contrast for readability
- Labels with arrows pointing to features

Bottom label: "示意图" (centered, small text)

Layout: Vertical 3:4 format
Color palette: Muted tones - [specific colors]
Style: Educational illustration with realistic reference, not photorealistic overall

Image size: 1024x1024 pixels (will be resized to 1080x1440).

CRITICAL: All Chinese text must be SHARP, CLEAR, and PERFECTLY LEGIBLE. NO BLURRY TEXT.
```

---

## 📊 实际案例：春季防虫大作战

### 案例1：小黑飞（Fungus Gnats）

**昆虫学特征**：
- 学名：Sciaridae
- 体长：2-8mm
- 颜色：深灰至黑色
- 特征：细长身体，长腿长触角，Y型翅脉
- 位置：潮湿土壤表面

**Prompt 示例**：

```
Educational schematic diagram for fungus gnat (小黑飞) identification with realistic reference inset.

Main layer (75% of image):
- Clean, simplified schematic illustration showing key identification features
- Muted educational colors: dark gray body, cream background, sage green accents
- Simple line art style with clear outlines
- Chinese labels pointing to key features

Key features to highlight in schematic:
- Small size (2-8mm) with size comparison to grain of rice
- Dark gray to black slender body
- Long legs and antennae
- Distinctive Y-shaped wing vein pattern
- Typical location: on moist soil surface

Realistic reference inset (25% of image):
- Circular frame in upper right corner
- Macro photography style showing actual fungus gnat appearance
- Realistic details: dark slender insect, visible wing veins, long legs
- Natural lighting, sharp focus on insect details

Knowledge points box on left side with Chinese text:
识别要点：
• 体长2-8mm（米粒大小）
• 深灰至黑色细长身体
• Y型翅脉特征明显
• 常见于潮湿土表

Text requirements:
- All Chinese text must be SHARP, CLEAR, and LEGIBLE
- Use clean sans-serif font
- High contrast for readability
- Labels with arrows pointing to features

Bottom label: "示意图" (centered, small text)

Layout: Vertical 3:4 format
Color palette: Muted tones - dark gray, cream, sage green, soft beige
Style: Educational illustration with realistic reference, not photorealistic overall

Image size: 1024x1024 pixels (will be resized to 1080x1440).

CRITICAL: All Chinese text must be SHARP, CLEAR, and PERFECTLY LEGIBLE. NO BLURRY TEXT.
```

**生成结果**：`01_final_v2_小黑飞识别图.png`

---

### 案例2：红蜘蛛（Spider Mites）

**昆虫学特征**：
- 学名：Tetranychidae
- 体长：0.5mm（针尖大小）
- 颜色：红色或黄橙色
- 特征：8条腿（蛛形纲），叶背丝网，针尖状黄斑
- 位置：叶片背面

**Prompt 示例**：

```
Educational schematic diagram for spider mite (红蜘蛛/叶螨) identification with realistic reference inset.

Main layer (75% of image):
- Clean, simplified schematic illustration showing key identification features
- Muted educational colors: sage green for leaves, dusty coral for mites, cream background
- Simple line art style with clear outlines
- Chinese labels pointing to key features

Key features to highlight in schematic:
- Tiny size (0.5mm, 针尖大小) with size comparison
- Yellow stippling damage on leaves (针尖大的小白点)
- Fine webbing on leaf undersides (背面有丝网)
- Leaf yellowing symptoms (叶子发黄)
- Typical location: leaf undersides

Realistic reference inset (25% of image):
- Circular frame in upper right corner
- Macro photography style showing actual spider mite appearance
- Realistic details: reddish-orange tiny mites, fine webbing, leaf damage
- Natural lighting, sharp focus on mite details

Knowledge points box on left side with Chinese text:
识别要点：
• 体长0.5mm（针尖大）
• 叶背有细丝网
• 叶面针尖状黄斑
• 需放大镜观察

Text requirements:
- All Chinese text must be SHARP, CLEAR, and LEGIBLE
- Use clean sans-serif font
- High contrast for readability
- Labels with arrows pointing to features

Bottom label: "示意图" (centered, small text)

Layout: Vertical 3:4 format
Color palette: Muted tones - sage green, dusty coral, cream, soft gray
Style: Educational illustration with realistic reference, not photorealistic overall

Image size: 1024x1024 pixels (will be resized to 1080x1440).

CRITICAL: All Chinese text must be SHARP, CLEAR, and PERFECTLY LEGIBLE. NO BLURRY TEXT.
```

**生成结果**：`04_红蜘蛛识别图.png`

---

### 案例3：蚧壳虫（Scale Insects）

**昆虫学特征**：
- 学名：Coccoidea
- 体长：2-5mm
- 颜色：白色蜡质外壳
- 特征：固定不动，椭圆形，像小疙瘩
- 位置：茎干或叶背

**Prompt 示例**：

```
Educational schematic diagram for scale insect (蚧壳虫) identification with realistic reference inset.

Main layer (75% of image):
- Clean, simplified schematic illustration showing key identification features
- Muted educational colors: sage green for stems/leaves, cream white for scales, soft background
- Simple line art style with clear outlines
- Chinese labels pointing to key features

Key features to highlight in schematic:
- White waxy coating appearance (白色蜡质外壳)
- Oval shape, 2-5mm size
- Attached to stems and leaf undersides (粘在茎干或叶子背面)
- Immobile (looks like bumps, 固定不动)
- Hard to remove by hand (抠都抠不下来)

Realistic reference inset (25% of image):
- Circular frame in upper right corner
- Macro photography style showing actual scale insect appearance
- Realistic details: white waxy bumps on plant stem, clustered appearance
- Natural lighting, sharp focus on scale details

Knowledge points box on left side with Chinese text:
识别要点：
• 白色蜡质外壳
• 固定不动（像小疙瘩）
• 体长2-5mm
• 茎干或叶背

Text requirements:
- All Chinese text must be SHARP, CLEAR, and LEGIBLE
- Use clean sans-serif font
- High contrast for readability
- Labels with arrows pointing to features

Bottom label: "示意图" (centered, small text)

Layout: Vertical 3:4 format
Color palette: Muted tones - sage green, cream white, soft gray, dusty beige
Style: Educational illustration with realistic reference, not photorealistic overall

Image size: 1024x1024 pixels (will be resized to 1080x1440).

CRITICAL: All Chinese text must be SHARP, CLEAR, and PERFECTLY LEGIBLE. NO BLURRY TEXT.
```

**生成结果**：`06_蚧壳虫识别图.png`

---

## ✅ 质量检查清单

生成病虫害识别图后，必须检查：

### 示意图部分
- [ ] 明确标注"示意图"（底部居中）
- [ ] 突出了关键识别特征
- [ ] 使用教学风格（简化线条，非写实）
- [ ] 中文标注清晰易读，SHARP且LEGIBLE
- [ ] 颜色柔和（muted tones）

### 真实参考inset部分
- [ ] 圆形框架位于右上角
- [ ] 占比约25%
- [ ] 呈现真实感（macro photography style）
- [ ] 与示意图形成对比

### 组合效果
- [ ] 示意图 + inset 形成清晰对比
- [ ] 布局清晰，易于理解
- [ ] 尺寸符合平台要求（1080x1440）
- [ ] 文件命名规范

---

## 🎓 关键经验总结

### 1. 为什么不能生成虚假的"真实照片"

**教训：**
- AI 生成的虫害照片可能不准确
- 用户依赖这些图片识别虫害
- 错误识别导致错误处理
- 损害内容可信度

**正确做法：**
- 教学型内容使用示意图 + 真实参考组合
- 基于科学文献的准确特征描述
- 明确标注图片类型

### 2. 示意图 vs 真实参考的分工

| 类型 | 作用 | 优势 | 局限 |
|------|------|------|------|
| **示意图（75%）** | 突出关键特征 | 清晰、易懂、教学性强 | 简化，缺少真实感 |
| **真实参考（25%）** | 提供真实对照 | 增强可信度 | 细节复杂，不够清晰 |
| **组合使用** | 互补 | 准确 + 易懂 + 可信 | 需要精心设计prompt |

### 3. 方案演进过程

**方案1（初始）**：直接生成"真实感"虫害照片
- ❌ 问题：无法保证准确性，可能误导用户

**方案2（改进）**：使用真实照片 + AI生成示意图
- ❌ 问题：AI无法下载真实照片，给用户增加工作量

**方案3（最终）**：示意图 + 真实参考inset
- ✅ 优势：AI完全可执行，教学清晰，真实参考，准确可靠

### 4. 适用范围

**必须使用此方案的内容类型：**
- ✅ 病虫害识别
- ✅ 植物疾病诊断
- ✅ 植物品种识别
- ✅ 生长问题诊断
- ✅ 任何需要用户"对照识别"的内容

**可以使用纯AI生成的内容类型：**
- ✅ 场景氛围图
- ✅ 养护步骤示意
- ✅ 装饰性配图
- ✅ 概念展示

---

## 🔧 实施建议

### 对于内容创作者

1. **规划阶段**
   - 识别哪些图片需要病虫害识别图
   - 收集准确的昆虫学特征描述
   - 确定识别要点

2. **制作阶段**
   - 使用统一的prompt模板
   - 确保中文文字SHARP且LEGIBLE
   - 检查示意图和inset的比例

3. **发布阶段**
   - 标注"示意图"
   - 提供识别要点文字说明
   - 说明基于科学特征描述

### 对于 AI 执行者

1. **识别内容类型**
   - 判断是否为教学/识别型内容
   - 如果是，使用示意图 + inset方案

2. **准备特征描述**
   - 搜索准确的昆虫学特征
   - 包括：体长、颜色、形态、位置
   - 基于科学文献

3. **生成图片**
   - 使用统一模板
   - 强调中文文字清晰度
   - 确保示意图风格（非写实）

4. **质量检查**
   - 检查所有清单项
   - 确保准确性
   - 保存元数据

---

## 📚 参考资源

### 昆虫学特征参考
- [Fungus Gnats Visual ID Guide](https://onenaturalist.blog/pictures-gnats-visual-identification-guide/)
- [Spider Mite Images Guide](https://finenaturalist.blog/spider-mite-images-visual-identification-guide)
- [Mealybugs ID & Control](https://openlearning.blog/mealybugs-on-plants-guide)

---

**相关案例**：
- [案例 001：微信公众号君子兰封面](./case-001-wechat-cover.md)
- [案例 002：小红书多肉养护封面（带文字）](./case-002-xhs-cover.md)
- [案例 003：小红书真实场景图（手写文字）](./case-003-xhs-scene.md)

**返回**：[案例库索引](./README.md)
