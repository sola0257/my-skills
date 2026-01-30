# 小红书配图文字样式参考（基于2026-01-30实际案例）

> **来源**：/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/小红书/已发布/2026-01-30_多肉养护/
> **创建日期**：2026-01-30
> **用途**：作为后续生成小红书配图时的文字样式参考

---

## 一、封面图文字样式

**文件**：`cover_养了2年多肉才明白：新手最容易犯的3个错误.png`

**文字样式**：
- 字体：白色粗体+黑边（4-6px黑色描边）
- 位置：顶部居中
- 大小：大字号，占顶部约1/4-1/3空间
- 效果：SHARP, CLEAR, BOLD - 专业图形设计文字叠加效果
- 内容：视觉标题（吸引点击）

**Prompt关键要求**：
```
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
- Effect: SHARP, CLEAR, and BOLD - like professional graphic design text overlay
```

---

## 二、真实场景图文字样式（dreamy-photo）

### 样式特点总结

**核心规律**：
- 字体：白色手写体（非粗体，非黑边）
- 位置：根据画面构图灵活调整（左下、右上、左上等）
- 大小：中等字号，不遮挡主体
- 效果：柔和、自然融入画面
- 内容：图片内容的简短描述

### 具体案例

#### 案例1：`01_我的多肉小花园.png`
- **文字位置**：左下角
- **文字内容**："我的多肉小花园"
- **文字样式**：白色手写体，有描边/阴影效果

#### 案例2：`03_叶片积水要注意.png`
- **文字位置**：右上角
- **文字内容**："叶片积水要注意"
- **文字样式**：白色手写体

#### 案例3：`04_这就是烂根的样子.png`
- **文字位置**：左上角
- **文字内容**："这就是烂根的样子"
- **文字样式**：白色手写体

**Prompt关键要求**（真实场景图）：
```
Composition: Leave some empty space in [position] area for text overlay.

TEXT OVERLAY REQUIREMENTS:
Add CLEAR CHINESE TEXT in [position]:
"[文字内容]" in white color with subtle shadow for readability.
Text should be clean, handwritten style font, SHARP and LEGIBLE.
```

---

## 三、手绘教程图文字样式（cozy-sketch）

**文件示例**：`05_正确浇水.png`

**文字样式**：
- 顶部标题：深色手写体（非白色）
- 标注文字：深色手写体，融入画面
- 底部说明框：框内文字
- 位置：多处标注（顶部、侧边、底部）

**文字内容示例**：
- 顶部："正确浇水方式"
- 标注："避免浇到叶片"、"浇在土壤上"
- 底部框："土干透再浇"

**Prompt关键要求**（手绘图）：
```
CRITICAL TEXT REQUIREMENTS:
Include CLEAR CHINESE TEXT annotations:
Top area "[标题]" in clear printed style,
Left side "[标注1]" with arrow,
Right side "[标注2]" with arrow,
Bottom decorative banner with "[总结]" in bold.
Text must be SHARP, CLEAR, and LEGIBLE Chinese characters.
```

---

## 四、对比信息图文字样式（infographic-sketch）

**文件示例**：`02_健康对比.png`, `09_土壤对比.png`

**文字样式**：
- 标题：深色手写体
- 对比标签：清晰的中文标签
- 说明文字：简短说明

**Prompt关键要求**（对比图）：
```
CRITICAL TEXT REQUIREMENTS:
Include CLEAR CHINESE TEXT labels:
Top left "[左侧标题]" in bold,
Top right "[右侧标题]" in bold,
Left side "[左侧说明]" near subject,
Right side "[右侧说明]" near subject,
Center top "[总标题]" as title.
Text must be SHARP, CLEAR, and LEGIBLE Chinese characters, NOT handwritten style but printed style.
```

---

## 五、文字位置选择规则

### 根据画面构图选择文字位置

| 画面构图 | 推荐文字位置 | 原因 |
|---------|-------------|------|
| 主体在中下部 | 左上角或右上角 | 不遮挡主体 |
| 主体在左侧 | 右上角或右下角 | 平衡构图 |
| 主体在右侧 | 左上角或左下角 | 平衡构图 |
| 主体居中 | 顶部居中或底部居中 | 对称美感 |
| 留白较多 | 留白区域 | 自然融入 |

### 文字位置表达方式

在Prompt中使用以下表达：
- `upper left corner` - 左上角
- `upper right corner` - 右上角
- `lower left corner` - 左下角
- `lower right corner` - 右下角
- `top center` - 顶部居中
- `bottom center` - 底部居中

---

## 六、关键经验总结

### ✅ 正确做法

1. **封面图**：使用白色粗体+黑边，顶部居中，大字号
2. **真实场景图**：使用白色手写体，位置灵活，融入画面
3. **手绘图/对比图**：使用深色手写体或印刷体，多处标注
4. **文字位置**：根据画面构图灵活调整，不遮挡主体

### ❌ 常见错误

1. 所有图片都用同一种文字样式（封面样式）
2. 文字位置固定不变（总是左下角）
3. 文字过大遮挡主体
4. 文字颜色与背景对比度不足

---

## 七、Prompt模板

### 封面图Prompt模板

```
[场景描述]

Composition: Leave generous empty space in the top 1/3 of the image.

TEXT OVERLAY REQUIREMENTS (CRITICAL):
Add Chinese text at the top center of the image:
Line 1: "[标题第一行]"
Line 2: "[标题第二行]"

Text style (MUST FOLLOW EXACTLY):
- Font: Bold, thick, chunky Chinese font
- Color: Pure white (#FFFFFF) with 4-6px black stroke
- Size: Large and prominent (占据顶部约1/4空间)
- Position: Top center, horizontally centered
- Effect: SHARP, CLEAR, and BOLD

Image size: 1080x1440 pixels. NO ENGLISH TEXT. NO PEOPLE.
```

### 真实场景图Prompt模板

```
[场景描述]

Composition: Leave some empty space in [position] area for text overlay.

TEXT OVERLAY REQUIREMENTS:
Add CLEAR CHINESE TEXT in [position]:
"[文字内容]" in white color with subtle shadow for readability.
Text should be clean, handwritten style font, SHARP and LEGIBLE.

Image size: 1080x1440 pixels. NO ENGLISH TEXT. NO PEOPLE.
```

### 手绘图Prompt模板

```
[场景描述]

CRITICAL TEXT REQUIREMENTS:
Include CLEAR CHINESE TEXT annotations:
Top area "[标题]" in clear printed style,
[Position] "[标注1]" with arrow,
[Position] "[标注2]" with arrow,
Bottom decorative banner with "[总结]" in bold.
Text must be SHARP, CLEAR, and LEGIBLE Chinese characters.

Image size: 1080x1440 pixels.
```

---

**最后更新**：2026-01-30
**版本**：v1.0
