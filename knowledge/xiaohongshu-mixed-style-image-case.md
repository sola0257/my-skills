# 小红书混合风格配图生成案例

**案例日期**：2026-01-29
**案例主题**：多肉养护教程
**配图数量**：15张（1封面 + 14正文）
**核心策略**：根据内容类型混用三种风格

---

## 📋 案例背景

### 内容类型
- **平台**：小红书
- **主题**：养了2年多肉才明白：新手最容易犯的3个错误
- **内容结构**：
  - 开篇介绍
  - 3个核心要点（浇水、光照、配土）
  - 每个要点包含：问题描述 + 解决方案
  - 总结 + 互动引导

### 配图需求
- 数量：12-15张
- 尺寸：3:4竖版（1080×1440）
- 风格：需要对比图、步骤图、细节图
- 要求：部分图片需要中文标注

---

## 🎨 风格策略

### 核心原则
**根据内容类型选择风格，而非统一风格**

| 内容类型 | 使用风格 | 原因 | 文字处理 |
|---------|---------|------|---------|
| 场景展示 | dreamy-photo | 真实感、代入感强 | 无文字，命名提供建议 |
| 细节特写 | dreamy-photo | 真实感、细节清晰 | 无文字，命名提供建议 |
| 对比图 | infographic-sketch | 清晰展示差异 | 含中文标注 |
| 步骤图 | cozy-sketch | 教程感、可标注 | 含中文说明 |
| 总结图 | infographic-sketch | 信息整合 | 含中文标注 |

---

## 📊 配图清单

### 封面（1张）
- **cover.png** - dreamy-photo
- 内容：多肉植物场景，展示健康和问题状态
- 文字：无

### 真实感图片（9张）- dreamy-photo
1. **01_我的多肉小花园.png** - 场景展示
2. **03_叶片积水要注意.png** - 细节特写（浇水过多）
3. **04_这就是烂根的样子.png** - 细节特写（烂根问题）
4. **06_南向阳台最适合.png** - 场景展示（充足光照）
5. **07_徒长就是缺光照.png** - 场景展示（光照不足）
6. **08_晒足太阳就紧凑.png** - 场景展示（健康状态）
7. **10_园土容易积水.png** - 问题展示（积水问题）
8. **12_养好多肉的成就感.png** - 场景展示（养护成果）
9. **14_欢迎评论区交流.png** - 场景展示（互动氛围）

**文字处理**：
- 图片中无文字
- 文件名中的中文是具体的、可直接添加到图片上的文字建议
- 示例："叶片积水要注意" - 可以直接作为图片标注使用

### 信息图（3张）- infographic-sketch
1. **02_健康对比.png** - 对比图
   - 含中文："健康多肉" vs "徒长多肉"
   - 标注："叶片紧凑""颜色饱满" vs "茎部拉长""叶片稀疏"

2. **09_土壤对比.png** - 对比图
   - 含中文："三种土壤对比"
   - 标注："园土-易积水""泥炭土-保水性好""颗粒土-透气排水"

3. **13_三要素总结.png** - 总结图
   - 含中文："多肉养护三要素"
   - 标注："控水-7-10天一次""光照-每天4小时+""透气土-泥炭+颗粒"

**文字处理**：
- 图片中直接包含中文标注
- 使用清晰的手写风格字体（类似马克笔或毛笔字）
- 文字必须清晰、锐利、易读

### 手绘教程（2张）- cozy-sketch
1. **05_正确浇水.png** - 步骤图
   - 含中文："正确浇水方式"
   - 标注："浇在土壤上""避免浇到叶片""土干透再浇"

2. **11_配土方法.png** - 步骤图
   - 含中文："配土方法"
   - 标注："泥炭土40%""颗粒土60%""1.准备材料 2.混合均匀 3.装盆使用"

**文字处理**：
- 图片中直接包含中文说明
- 使用清晰的手写风格字体
- 文字必须清晰、锐利、易读

---

## 🎯 Prompt 模板

### dreamy-photo 模板（真实感）
```
A 3:4 photograph in dreamy realistic style.
Scene: [具体场景描述], authentic home environment, lived-in atmosphere.
Lighting: Soft natural window light, warm golden hour glow, gentle shadows.
Details: [场景细节元素]
Mood: [情绪关键词], cozy, inviting.
Color palette: Muted Morandi colors, desaturated tones, cream and sage.
Color control: Use dusty coral instead of red, muted rose instead of pink, soft terracotta for warm accents.
Style: Realistic lifestyle photography, soft focus, film-like quality, NOT product photography.
NO TEXT. NO WORDS. NO LETTERS. NO PEOPLE. NO STUDIO LIGHTING.
```

### infographic-sketch 模板（信息图）
```
A 3:4 infographic in hand-drawn sketchnote style.
Topic: [主题]
Title at top: "[中文标题]" in clear bold handwritten Chinese font.
Structure: [信息结构描述]
Visual elements: [图标、图表、箭头等]
Text: Include Chinese labels "[具体中文内容]" in clear handwriting.
Background: Clean notebook paper or lined paper.
Color palette: Functional colors for categorization, yellow highlighter accents.
Style: Educational sketchnote aesthetic.
Chinese text must use clear, legible handwritten style font similar to marker or brush pen writing.
NO ENGLISH TEXT.
```

### cozy-sketch 模板（手绘教程）
```
A 3:4 illustration in hand-drawn sketch style.
Subject: [主题]
Title: "[中文标题]" in clear handwritten Chinese font.
Details: Pencil line drawings with soft watercolor washes.
Elements: [具体元素]
Annotations: Include Chinese text "[具体说明]" in neat handwriting.
Color palette: Muted beige, dusty rose, sage green watercolor accents.
Style: Cozy sketchbook aesthetic, educational, natural imperfect lines.
Chinese text must use clear, legible handwritten style font.
NO ENGLISH TEXT. NO PEOPLE FACES.
```

---

## ✅ 关键要点

### 1. 风格选择规则
- **对比图** → infographic-sketch（清晰对比）
- **步骤图** → cozy-sketch（教程感）
- **细节图** → dreamy-photo（真实感）
- **场景图** → dreamy-photo（生活感）
- **总结图** → infographic-sketch（信息整合）

### 2. 文字处理规则
- **真实感图片**：
  - 图片中无文字
  - 文件名提供具体的、可操作的文字建议
  - 格式：`序号_具体文字建议.png`
  - 示例：`03_叶片积水要注意.png`

- **信息图/教程**：
  - 图片中直接包含中文
  - 使用清晰的手写风格字体
  - 必须在 prompt 中明确指定中文内容
  - 必须强调：`Chinese text must use clear, legible handwritten style font`

### 3. 中文字体标准
- **可接受的字体效果**：
  - 清晰的手写风格
  - 类似马克笔或毛笔字
  - 笔画清晰、易读
  - 参考：05、11、13号图的字体效果

- **需要避免的字体效果**：
  - 模糊不清
  - 笔画断裂
  - 过于潦草
  - 难以辨认

### 4. 色彩统一性
- 所有图片使用 Morandi 色系
- 低饱和度、柔和光线
- 避免高饱和度颜色
- 使用替代词：dusty coral（代替red）、muted rose（代替pink）、sage green（代替green）

---

## 📈 执行效果

### 数量达标
- ✅ 生成15张配图（12-15张范围内）
- ✅ 1封面 + 14正文

### 风格多样
- ✅ dreamy-photo: 10张（67%）
- ✅ infographic-sketch: 3张（20%）
- ✅ cozy-sketch: 2张（13%）

### 规格统一
- ✅ 全部3:4竖版（1080×1440）
- ✅ 命名规范：序号_中文说明.png
- ✅ 色调协调：Morandi色系

### 功能性强
- ✅ 对比图清晰展示差异
- ✅ 步骤图易于理解
- ✅ 真实感图片代入感强
- ✅ 文字处理符合使用需求

---

## 🔄 可复用性

### 适用场景
此配图方案适用于以下类型的小红书内容：
- 教程类（养护、DIY、技巧）
- 避坑类（对比、问题解决）
- 科普类（知识点、原理说明）
- 经验分享类（真实体验、案例展示）

### 调整建议
根据不同内容类型，可调整风格比例：
- **纯教程类**：增加 cozy-sketch 比例
- **纯对比类**：增加 infographic-sketch 比例
- **纯经验类**：增加 dreamy-photo 比例

---

## 📝 经验总结

### 成功要素
1. **风格混用**：根据内容类型选择，而非统一风格
2. **文字分离**：真实感图片无文字，信息图含文字
3. **命名规范**：真实感图片的命名提供具体文字建议
4. **字体标准**：信息图/教程使用清晰手写风格字体
5. **色调统一**：虽然风格混用，但色调保持一致

### 注意事项
1. 必须在 prompt 中明确指定中文内容
2. 必须强调字体清晰度要求
3. 真实感图片的命名要具体、可操作
4. 信息图的文字布局要合理
5. 所有图片保持 Morandi 色系统一

---

**案例路径**：`/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/小红书/2026-01-30_多肉养护`

**最后更新**：2026-01-29
