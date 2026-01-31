# 案例库使用指南

## 📚 案例库的价值

案例库是持续优化插画生成效果的核心工具，通过积累正面和反面案例，可以：

1. **建立质量标准**：明确什么是好的效果
2. **避免重复错误**：记录失败案例，避免再犯
3. **提取成功模式**：总结可复用的 Prompt 片段
4. **持续改进**：基于案例分析，不断优化模板

---

## 🗂️ 案例库结构

```
knowledge/cases/
├── INDEX.md                    # 索引文档（包含所有案例的链接和简介）
├── CASE_TEMPLATE.md            # 案例模板
├── positive/                   # 正面案例目录
│   ├── case-001-watercolor-oriental-succulent.md
│   ├── case-002-ink-oriental-orchid.md
│   └── ...
└── negative/                   # 反面案例目录
    ├── case-001-oversaturated-colors.md
    ├── case-002-lack-of-whitespace.md
    └── ...
```

---

## ✅ 添加正面案例

### 步骤1：生成并评估

1. 使用 Skill 生成插画
2. 评估效果（视觉效果、风格符合度、可复用性）
3. 如果效果优秀，决定添加到案例库

### 步骤2：创建案例文件

```bash
# 1. 复制模板
cp knowledge/cases/CASE_TEMPLATE.md \
   knowledge/cases/positive/case-001-watercolor-oriental-succulent.md

# 2. 编辑文件，填写以下内容：
#    - 基本信息（编号、风格、植物、日期、评分）
#    - 效果展示（图片和描述）
#    - 成功要素（Prompt 关键点、视觉效果分析）
#    - 完整 Prompt
#    - 经验总结
```

### 步骤3：保存图片

```bash
# 将生成的图片复制到案例库
cp .tmp/watercolor_oriental_20260131_123456_桃蛋多肉.png \
   .tmp/case-001.png
```

### 步骤4：更新索引

在 `INDEX.md` 中添加案例链接：

```markdown
### 清新水彩（东方）

- [案例 001：多肉植物桃蛋](./positive/case-001-watercolor-oriental-succulent.md) ⭐⭐⭐⭐⭐
  - 简介：完美展示了东方水彩的留白和淡雅特点
  - 关键词：留白、淡雅、晕染
  - 日期：2026-01-31
```

---

## ❌ 添加反面案例

### 步骤1：识别问题

1. 生成效果不理想
2. 分析问题所在（色彩、构图、风格等）
3. 决定添加到反面案例库

### 步骤2：创建案例文件

```bash
# 1. 复制模板
cp knowledge/cases/CASE_TEMPLATE.md \
   knowledge/cases/negative/case-001-oversaturated-colors.md

# 2. 编辑文件，填写以下内容：
#    - 基本信息（编号、问题类型、风格、日期）
#    - 问题展示（图片和描述）
#    - 问题分析（主要问题、Prompt 问题、根本原因）
#    - 修正方案（正确的 Prompt、修正要点）
#    - 避免方法（禁止词汇、必须词汇、检查清单）
```

### 步骤3：保存对比图片

```bash
# 保存问题图片
cp .tmp/failed_image.png .tmp/negative-case-001-before.png

# 如果有修正后的图片，也保存
cp .tmp/fixed_image.png .tmp/negative-case-001-after.png
```

### 步骤4：更新索引

在 `INDEX.md` 中添加案例链接：

```markdown
### 常见问题

- [反面案例 001：色彩过饱和](./negative/case-001-oversaturated-colors.md)
  - 问题：使用了 bright/vivid 等高饱和度词汇
  - 修正：改用 muted/dusty/soft 等降低饱和度的词汇
  - 日期：2026-01-31
```

---

## 📊 案例评分标准

### 正面案例评分

| 评分 | 标准 |
|------|------|
| ⭐⭐⭐⭐⭐ | 完美：视觉效果优秀，完全符合风格特征，可作为标准参考 |
| ⭐⭐⭐⭐ | 优秀：效果很好，基本符合风格特征，有小瑕疵 |
| ⭐⭐⭐ | 良好：效果可接受，符合基本要求，有改进空间 |

### 反面案例分类

| 类型 | 说明 |
|------|------|
| `color-issue` | 色彩问题（过饱和、色调不符等） |
| `composition-issue` | 构图问题（缺少留白、布局不当等） |
| `style-mismatch` | 风格不符（不符合东方/西方美感特征） |
| `technical-error` | 技术错误（生成失败、格式错误等） |

---

## 🔍 案例分析方法

### 1. 视觉分析

**色彩**：
- 饱和度是否合适？
- 色调是否符合风格？
- 色彩搭配是否和谐？

**构图**：
- 留白是否充足？
- 主体位置是否合理？
- 整体平衡感如何？

**质感**：
- 笔触是否自然？
- 材质表现是否到位？
- 细节是否丰富？

### 2. Prompt 分析

**关键词提取**：
- 哪些词汇起到了关键作用？
- 哪些描述是可复用的？

**问题识别**：
- 哪些词汇导致了问题？
- 哪些描述需要避免？

### 3. 经验总结

**成功模式**：
- 提取可复用的 Prompt 片段
- 总结成功的关键要素

**失败教训**：
- 记录禁止使用的词汇
- 建立检查清单

---

## 📈 案例库的维护

### 定期Review

**每月一次**：
- 回顾所有案例
- 更新评分和标签
- 删除过时的案例

### 持续优化

**基于案例优化**：
1. 提取成功案例的共同特征
2. 更新 Prompt 模板
3. 优化风格-模型映射
4. 完善检查清单

### 知识沉淀

**从案例到规则**：
- 当某个模式出现3次以上，考虑写入规范
- 当某个问题反复出现，加入强制检查
- 定期总结案例库的insights

---

## 🎯 使用案例库的最佳实践

### 1. 生成前

**查阅相关案例**：
- 查看同风格的正面案例
- 参考成功的 Prompt 片段
- 避免反面案例中的错误

### 2. 生成后

**评估效果**：
- 对比正面案例的标准
- 检查是否有反面案例中的问题
- 决定是否添加到案例库

### 3. 优化时

**基于案例改进**：
- 分析失败原因
- 参考成功案例的做法
- 迭代优化 Prompt

---

## 📝 案例编号规则

### 正面案例

```
case-[编号]-[风格代码]-[植物名称].md

示例：
- case-001-watercolor-oriental-succulent.md
- case-002-ink-oriental-orchid.md
- case-003-pencil-western-rose.md
```

### 反面案例

```
case-[编号]-[问题描述].md

示例：
- case-001-oversaturated-colors.md
- case-002-lack-of-whitespace.md
- case-003-style-mismatch.md
```

---

## 🔗 相关文档

- [INDEX.md](./INDEX.md) - 案例库索引
- [CASE_TEMPLATE.md](./CASE_TEMPLATE.md) - 案例模板
- [style-prompt-templates.md](../style-prompt-templates.md) - Prompt 模板库
- [style-model-mapping.md](../style-model-mapping.md) - 风格-模型映射表

---

**最后更新**：2026-01-31
**维护者**：illustration-converter Skill
