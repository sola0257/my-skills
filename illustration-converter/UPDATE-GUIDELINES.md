# Skill 更新规范

**目的**：确保每次更新都遵循"渐进式披露"和"Skill 精简"原则

---

## 📋 核心原则

### 1. 渐进式披露（Progressive Disclosure）
- **SKILL.md**：只包含用户需要立即知道的信息
- **knowledge/**：包含详细的技术细节、案例、分析

### 2. Skill 精简（Skill Simplicity）
- **SKILL.md**：保持简洁，通过引用而非复制
- **避免重复**：同一内容不应同时出现在 SKILL.md 和 knowledge/

---

## ✅ 更新前检查清单

### 准备更新时，先问自己：

1. **这个内容属于哪里？**
   - [ ] 核心工作流程 → SKILL.md
   - [ ] 详细说明/案例/分析 → knowledge/
   - [ ] 技术实现细节 → scripts/ 或 knowledge/

2. **是否会造成重复？**
   - [ ] 检查 SKILL.md 是否已有类似内容
   - [ ] 检查 knowledge/ 是否已有类似文档
   - [ ] 如果有重复，考虑合并或引用

3. **SKILL.md 是否保持精简？**
   - [ ] SKILL.md 行数是否合理（建议 < 500 行）
   - [ ] 是否可以用引用替代详细内容
   - [ ] 是否有内容应该移到 knowledge/

---

## 📝 更新场景和规范

### 场景1：添加新功能

**步骤**：
1. 在 SKILL.md 中添加简要说明（1-3 句话）
2. 在 knowledge/ 创建详细文档
3. 在 SKILL.md 的"Knowledge"章节添加引用
4. 更新 knowledge/README.md

**示例**：
```markdown
# SKILL.md
## 新功能：批量生成
支持一次生成多个植物的插画。详见 `knowledge/batch-generation-guide.md`

# knowledge/batch-generation-guide.md
[详细的使用说明、参数、示例...]
```

---

### 场景2：优化现有功能

**步骤**：
1. 如果是流程变化 → 更新 SKILL.md
2. 如果是细节优化 → 更新 knowledge/ 对应文档
3. 不要在 SKILL.md 中添加优化细节

**示例**：
```markdown
# 错误做法 ❌
## SKILL.md
Step 5: 图片生成
- 使用 generate_series() 方法
- 参数1：style_code（风格代码）
- 参数2：subject（主题）
- 参数3：details（细节描述）
- [20行详细说明...]

# 正确做法 ✅
## SKILL.md
Step 5: 图片生成
调用 `generate_series()` 生成系列图。详见 `knowledge/generation-api-reference.md`

## knowledge/generation-api-reference.md
[完整的 API 文档、参数说明、示例...]
```

---

### 场景3：记录问题和解决方案

**步骤**：
1. 问题记录 → knowledge/anti-patterns-cases.md
2. 优化历程 → knowledge/complete-optimization-record.md
3. 不要在 SKILL.md 中记录详细问题

**示例**：
```markdown
# SKILL.md
## 禁止行为
- ❌ 禁止让 AI 自动选择模型
- ❌ 禁止跳过交互式提问
详见 `knowledge/anti-patterns-cases.md`

# knowledge/anti-patterns-cases.md
[详细的反面案例、问题分析、解决方案...]
```

---

### 场景4：添加配置或参数

**步骤**：
1. 简要说明 → SKILL.md
2. 详细配置 → knowledge/configuration-guide.md
3. 技术实现 → scripts/ 注释

**示例**：
```markdown
# SKILL.md
## 配置
所有风格默认使用 gemini-3-pro-image-preview
详见 `knowledge/style-model-mapping.md`

# knowledge/style-model-mapping.md
[完整的映射表、选择原因、性能对比...]
```

---

## 🚨 禁止的更新模式

### ❌ 反面模式1：在 SKILL.md 中堆积细节
```markdown
# 错误示例
## Step 5: 图片生成

### 彩铅风格 Prompt 构建
1. 基础描述：A 3:4 colored pencil illustration...
2. 风格定义：Western realistic style...
3. 技术参数：Layered burnishing...
[50行详细 Prompt...]

### 水彩风格 Prompt 构建
[又是50行...]
```

**问题**：SKILL.md 变得臃肿，难以维护

**正确做法**：
```markdown
## Step 5: 图片生成
根据选择的风格构建 Prompt 并生成图片。
Prompt 模板详见 `knowledge/style-prompt-templates.md`
```

---

### ❌ 反面模式2：重复内容
```markdown
# SKILL.md 和 knowledge/xxx.md 都包含相同的详细内容
```

**问题**：维护困难，容易不同步

**正确做法**：
- SKILL.md：简要说明 + 引用
- knowledge/：完整内容

---

### ❌ 反面模式3：缺少引用
```markdown
# SKILL.md
## Step 5: 图片生成
详细说明请查看相关文档

# 没有说明是哪个文档
```

**问题**：用户不知道去哪里找详细信息

**正确做法**：
```markdown
## Step 5: 图片生成
详细说明请查看 `knowledge/generation-guide.md`
```

---

## 📊 更新后检查清单

### 完成更新后，检查：

1. **SKILL.md 检查**
   - [ ] 行数是否合理（< 500 行）
   - [ ] 是否只包含核心流程
   - [ ] 是否有详细内容应该移到 knowledge/
   - [ ] 引用是否清晰明确

2. **knowledge/ 检查**
   - [ ] 新文档是否在 SKILL.md 中被引用
   - [ ] knowledge/README.md 是否更新
   - [ ] 文档之间的引用关系是否清晰

3. **一致性检查**
   - [ ] 是否有内容在多处重复
   - [ ] 版本号是否更新
   - [ ] 更新日志是否记录

---

## 🔄 定期维护

### 每月检查（建议）

1. **SKILL.md 瘦身检查**
   - 检查是否有内容可以移到 knowledge/
   - 检查是否有过时的内容

2. **knowledge/ 整理**
   - 合并相似的文档
   - 更新过时的信息
   - 检查引用关系

3. **文档质量检查**
   - 是否有断裂的引用
   - 是否有重复的内容
   - 是否有缺失的文档

---

## 📚 参考模板

### SKILL.md 章节模板
```markdown
## [功能名称]

[1-3句简要说明]

**详细说明**：`knowledge/[对应文档].md`
```

### knowledge/ 文档模板
```markdown
# [文档标题]

**目的**：[为什么需要这个文档]

---

## [章节1]
[详细内容...]

## [章节2]
[详细内容...]

---

**创建时间**：YYYY-MM-DD
**适用范围**：[说明适用场景]
```

---

## 🎯 快速决策树

```
需要更新内容
    ↓
是核心工作流程？
    ├─ 是 → SKILL.md（简要）+ knowledge/（详细）
    └─ 否 → knowledge/（详细）
        ↓
    SKILL.md 中添加引用
        ↓
    更新 knowledge/README.md
        ↓
    检查是否有重复内容
        ↓
    完成
```

---

## 💡 最佳实践

### 1. 先写 knowledge/，再写 SKILL.md
- 先完成详细文档
- 再提炼核心要点到 SKILL.md
- 这样可以确保 SKILL.md 保持精简

### 2. 使用明确的引用格式
```markdown
详见 `knowledge/xxx.md`
参考 `knowledge/xxx.md` 的 [章节名称]
完整说明：`knowledge/xxx.md`
```

### 3. 定期审查
- 每次大更新后审查一次
- 每月定期检查一次
- 发现问题及时调整

---

## 🚀 自动化检查（未来）

### 可以考虑的自动化检查：
1. SKILL.md 行数检查（警告 > 500 行）
2. 重复内容检测
3. 断裂引用检测
4. 文档结构验证

---

**创建时间**：2026-02-02
**遵循原则**：渐进式披露、Skill 精简
**维护者**：所有更新 Skill 的人员
