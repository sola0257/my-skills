# Skill 执行质量保证四层机制

**文档版本**：v1.0
**创建日期**：2026-01-29
**适用场景**：所有需要确保执行流程完整性的 Skills

---

## 📋 文档用途

### 什么时候使用这个文档？

**场景1：发现 Skill 执行不完整**
- 症状：AI 跳过了某些步骤
- 时机：用户发现问题后
- 使用方式：将此文档内容提供给 AI，要求按照四层机制修正

**场景2：创建新的内容生成类 Skill**
- 症状：需要确保执行流程完整
- 时机：Skill 开发阶段
- 使用方式：参考四层机制设计 Skill

**场景3：优化现有 Skill**
- 症状：Skill 经常被不完整执行
- 时机：Skill 优化阶段
- 使用方式：按照四层机制逐层检查和改进

### 如何使用这个文档？

**给 AI 的指令示例**：
```
我发现你在执行 [skill-name] 时跳过了 [某个步骤]。
请阅读 /Users/dj/Desktop/小静的skills/skill-standards/knowledge/execution-quality-assurance.md
然后按照四层机制修正这个问题。
```

---

## 🎯 核心问题

### 问题描述
AI 在执行 Skill 时可能会：
- 跳过某些步骤（如网络搜索）
- 选择性执行（认为"这次不需要"）
- 理解错误（误解指令含义）

### 根本原因
**单一机制无法解决问题**：
- 仅靠 SKILL.md 指令 → AI 可能理解错误
- 仅靠 CLAUDE.md 规则 → AI 可能认为是例外
- 仅靠 Hook 检测 → 事后发现，无法阻止
- 仅靠反馈机制 → 需要多次迭代才生效

**需要多层机制配合**，形成完整的质量保证体系。

---

## 🏗️ 四层机制架构

```
┌─────────────────────────────────────────────┐
│  第1层：指令层（SKILL.md）                    │
│  - 明确标注 [必需] 步骤                       │
│  - 添加执行检查点                             │
│  - 说明跳过步骤的后果                         │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  第2层：规则层（CLAUDE.md）                   │
│  - 全局强制规则                               │
│  - 适用于所有相关 Skills                      │
│  - 在执行前就有约束                           │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  第3层：检测层（Hooks）                       │
│  - 执行后检测流程完整性                       │
│  - 标记缺失步骤                               │
│  - 记录问题到 instincts.json                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  第4层：反馈层（instincts.json）              │
│  - 记录历史问题                               │
│  - 下次执行前提醒                             │
│  - 形成学习闭环                               │
└─────────────────────────────────────────────┘
```

---

## 📐 第1层：指令层（SKILL.md）

### 目标
让 AI 清楚知道哪些步骤是必需的，不能跳过。

### 实施方法

#### 1. 标注必需步骤
```markdown
### Step 2: 网络搜索与知识整合 [必需]

⚠️ **强制执行**：此步骤为必需步骤，不可跳过

**适用场景**：
- ✅ 深度内容（>1000字）
- ✅ 科普类内容
- ✅ 养护指南
- ✅ 专业知识分享

**执行要求**：
1. 使用 WebSearch 搜索相关权威知识
2. 搜索本地知识库
3. 整合网络和本地知识
4. 记录知识来源
```

#### 2. 添加执行检查点
```markdown
**执行检查点**：
- [ ] 已使用 WebSearch 搜索相关知识
- [ ] 已搜索本地知识库
- [ ] 已整合网络和本地知识
- [ ] 已记录知识来源

**如果跳过此步骤**：
- ❌ 内容可能缺少最新知识
- ❌ 内容可能缺少权威来源
- ❌ 知识库无法扩充
```

#### 3. 说明后果
```markdown
**跳过此步骤的后果**：
1. 内容质量不达标（缺少权威来源）
2. 知识库无法扩充（无法持续积累）
3. 可能包含过时信息（未获取最新知识）
```

### 注意事项
- ✅ 保持 SKILL.md 精简，不要过度扩充
- ✅ 只标注真正必需的步骤
- ✅ 使用清晰的标记（如 `[必需]`）
- ❌ 不要把所有细节都写在 SKILL.md 中

---

## 📜 第2层：规则层（CLAUDE.md）

### 目标
建立全局规则，在 AI 执行前就有约束。

### 实施方法

#### 1. 添加全局规则
在 CLAUDE.md 中添加：

```markdown
## 内容生成强制规则

### 规则：深度内容必须进行网络搜索

**适用范围**：
- wechat-content-generator
- xiaohongshu-content-generator
- video-script-generator
- 所有内容生成类 Skills

**触发条件**：
当生成以下类型的内容时，必须先进行网络搜索：
- 深度教程（>1000字）
- 科普类内容
- 养护指南
- 专业知识分享

**执行流程**：
1. 识别内容类型
2. 判断是否需要网络搜索
3. 如果需要，必须先执行 WebSearch
4. 整合网络和本地知识
5. 生成内容
6. 归档新知识到本地库

**违反此规则的后果**：
- 内容质量不达标
- 缺少权威来源
- 知识库无法扩充
```

#### 2. 添加执行前检查规则
```markdown
### 规则：执行 Skill 前读取 instincts.json

**目的**：从历史问题中学习

**执行流程**：
1. 执行 Skill 前，读取 ~/.claude/skills/_global_config/instincts.json
2. 检查是否有关于此 Skill 的历史问题记录
3. 如果有，特别注意避免重复问题
4. 执行完成后，Hook 会检测是否还有问题

**示例**：
如果 instincts.json 记录：
- "wechat-content-generator 上次跳过了网络搜索"

那么这次执行时，AI 应该：
- 特别注意执行网络搜索步骤
- 确保不再跳过
```

### 优势
- ✅ 全局规则，适用于所有相关 Skills
- ✅ 在执行前就有约束
- ✅ 不依赖单个 SKILL.md

---

## 🔍 第3层：检测层（Hooks）

### 目标
执行后检测流程完整性，发现问题并记录。

### 实施方法

#### 1. 创建 skill-execution-auditor-hook.js

**Hook 位置**：`~/.claude/hooks/skill-execution-auditor-hook.js`

**触发时机**：Skill 执行后（ToolUseResult）

**检测内容**：
1. 读取 SKILL.md 的执行流程
2. 检测实际执行的步骤
3. 对比并标记缺失的必需步骤
4. 输出警告信息
5. 记录问题到 instincts.json

**核心逻辑**：
```javascript
// 读取 SKILL.md 获取期望步骤
function getExpectedSteps(skillName) {
  // 提取 Step 1, Step 2, Step 3...
  // 识别 [必需] 标记
}

// 检测实际执行的步骤
function detectExecutedSteps(toolResult) {
  // 检测 WebSearch 调用
  // 检测 Glob/Grep 调用
  // 检测其他关键步骤
}

// 审计执行流程
function auditExecution(skillName, toolResult) {
  const expected = getExpectedSteps(skillName);
  const executed = detectExecutedSteps(toolResult);

  // 对比并标记缺失步骤
  const missing = findMissingSteps(expected, executed);

  if (missing.length > 0) {
    // 输出警告
    console.log('⚠️ 发现缺失步骤:', missing);

    // 记录到 instincts.json
    recordToInstincts(skillName, missing);
  }
}
```

#### 2. Hook 输出示例
```
[执行流程审计] 发现问题:
  ⚠️ 缺少必需步骤: 网络搜索与知识整合

建议:
  - 检查 SKILL.md 的执行流程
  - 确保所有必需步骤都已执行
  - 考虑更新 Skill 以自动执行缺失步骤

问题已记录到: ~/.claude/skills/_global_config/instincts.json
```

### 局限性
- ❌ 只能事后检测，不能阻止
- ❌ 依赖工具调用记录，可能不准确
- ✅ 但能提供及时反馈给用户
- ✅ 能记录问题供下次参考

---

## 🔄 第4层：反馈层（instincts.json）

### 目标
记录历史问题，形成学习闭环。

### 实施方法

#### 1. instincts.json 结构
```json
{
  "last_updated": "2026-01-29T17:00:00+08:00",
  "skill_issues": [
    {
      "skill": "wechat-content-generator",
      "issue": "跳过了网络搜索步骤",
      "detected_at": "2026-01-29T16:00:00+08:00",
      "frequency": 2,
      "status": "active"
    }
  ],
  "reminders": [
    {
      "skill": "wechat-content-generator",
      "message": "上次执行时跳过了网络搜索，这次请确保执行",
      "priority": "high"
    }
  ]
}
```

#### 2. 执行前读取
在 CLAUDE.md 中添加规则：
```markdown
### 执行 Skill 前读取 instincts.json

**步骤**：
1. 读取 ~/.claude/skills/_global_config/instincts.json
2. 检查是否有关于此 Skill 的提醒
3. 如果有，在执行时特别注意
4. 执行完成后，Hook 会检测是否改进
```

#### 3. 学习闭环
```
第1次执行
    ↓
Hook 发现问题 → 记录到 instincts.json
    ↓
第2次执行前
    ↓
读取 instincts.json → 看到提醒
    ↓
执行时更加注意
    ↓
Hook 再次检测
    ↓
如果改进 → 更新 status 为 "resolved"
如果未改进 → frequency +1，升级 priority
```

### 优势
- ✅ 形成学习闭环
- ✅ AI 能从错误中学习
- ✅ 逐步减少问题
- ✅ 提供历史数据分析

---

## 🎯 完整执行流程

### 理想的执行流程

```
用户请求执行 Skill
    ↓
[第4层] 读取 instincts.json
    ├─ 检查历史问题
    └─ 看到提醒："上次跳过了网络搜索"
    ↓
[第2层] 应用 CLAUDE.md 全局规则
    ├─ "深度内容必须网络搜索"
    └─ 确认需要执行网络搜索
    ↓
[第1层] 读取 SKILL.md 执行流程
    ├─ Step 1: 解析输入
    ├─ Step 2: 网络搜索 [必需] ← 特别注意
    ├─ Step 3: 生成内容
    └─ ...
    ↓
AI 执行 Skill
    ├─ 执行 Step 1 ✓
    ├─ 执行 Step 2 ✓ (因为有提醒和规则)
    ├─ 执行 Step 3 ✓
    └─ ...
    ↓
[第3层] Hook 检测
    ├─ 读取 SKILL.md 期望步骤
    ├─ 检测实际执行步骤
    ├─ 对比：所有必需步骤都已执行 ✓
    └─ 输出：✅ 执行流程完整
    ↓
[第4层] 更新 instincts.json
    └─ 标记问题为 "resolved"
```

---

## 📊 实施优先级

### 短期（立即实施）

**优先级1：规则层（CLAUDE.md）**
- 影响：最大
- 难度：低
- 效果：立即生效
- 行动：添加全局规则

**优先级2：指令层（SKILL.md）**
- 影响：大
- 难度：低
- 效果：立即生效
- 行动：标注 [必需] 步骤

**优先级3：检测层（Hook）**
- 影响：中
- 难度：中
- 效果：提供反馈
- 行动：创建 skill-execution-auditor-hook.js

### 中期（逐步完善）

**优先级4：反馈层（instincts.json）**
- 影响：中
- 难度：中
- 效果：长期改进
- 行动：建立学习闭环

---

## 🔧 实施检查清单

### 第1层：指令层
- [ ] 在 SKILL.md 中标注 [必需] 步骤
- [ ] 添加执行检查点
- [ ] 说明跳过步骤的后果
- [ ] 保持 SKILL.md 精简

### 第2层：规则层
- [ ] 在 CLAUDE.md 中添加全局规则
- [ ] 定义适用范围和触发条件
- [ ] 说明执行流程
- [ ] 添加执行前检查规则

### 第3层：检测层
- [ ] 创建 skill-execution-auditor-hook.js
- [ ] 实现步骤检测逻辑
- [ ] 实现警告输出
- [ ] 实现问题记录到 instincts.json

### 第4层：反馈层
- [ ] 创建 instincts.json 结构
- [ ] 在 CLAUDE.md 中添加读取规则
- [ ] 实现学习闭环机制
- [ ] 定期清理已解决的问题

---

## 💡 使用示例

### 示例1：修正 wechat-content-generator

**问题**：AI 跳过了网络搜索步骤

**解决方案**：

1. **第1层（SKILL.md）**：
```markdown
### Step 2: 网络搜索与知识整合 [必需]

⚠️ **强制执行**：此步骤为必需步骤，不可跳过
```

2. **第2层（CLAUDE.md）**：
```markdown
## 内容生成强制规则

深度内容必须进行网络搜索
```

3. **第3层（Hook）**：
创建 skill-execution-auditor-hook.js

4. **第4层（instincts.json）**：
记录问题，下次提醒

### 示例2：创建新的内容生成 Skill

**参考四层机制设计**：

1. 在 SKILL.md 中明确标注必需步骤
2. 在 CLAUDE.md 中添加相关规则
3. 确保 Hook 能检测到此 Skill
4. 测试执行流程完整性

---

## 📝 总结

### 核心原则

**单一机制不够，需要多层配合**：
- 指令层：告诉 AI 该做什么
- 规则层：约束 AI 必须做什么
- 检测层：检查 AI 是否做了
- 反馈层：让 AI 从错误中学习

### 预期效果

- ✅ 减少执行不完整的问题
- ✅ 提高内容质量
- ✅ 形成持续改进机制
- ✅ 降低人工发现问题的依赖

### 适用场景

- ✅ 所有内容生成类 Skills
- ✅ 需要确保流程完整性的 Skills
- ✅ 经常被不完整执行的 Skills

---

**文档版本**：v1.0
**最后更新**：2026-01-29
**维护者**：skill-standards
