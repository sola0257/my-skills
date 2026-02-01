# 架构合规保障系统

**创建时间**：2026-02-02
**目的**：确保 illustration-converter Skill 持续遵循"渐进式披露"和"Skill 精简"原则

---

## 📋 系统概述

本系统通过**四层保障机制**确保每次更新都符合架构原则：

1. **文档规范层**：UPDATE-GUIDELINES.md
2. **自动检查层**：check-skill-structure.sh
3. **Hook 提醒层**：skill-update-guard-hook.js
4. **SKILL.md 提醒层**：更新规范章节

---

## 🛡️ 四层保障机制

### 第1层：文档规范（UPDATE-GUIDELINES.md）

**位置**：`/Users/dj/.claude/skills/illustration-converter/UPDATE-GUIDELINES.md`

**内容**：
- 核心原则说明（渐进式披露、Skill 精简）
- 更新前检查清单（3个关键问题）
- 4种更新场景的具体规范
- 禁止的更新模式（3个反面案例）
- 更新后检查清单
- 快速决策树

**使用时机**：每次更新前必读

---

### 第2层：自动检查（check-skill-structure.sh）

**位置**：`/Users/dj/.claude/skills/illustration-converter/check-skill-structure.sh`

**功能**：
- ✅ 检查 SKILL.md 行数（警告 > 500 行）
- ✅ 检查 knowledge/ 目录结构
- ✅ 检查必要文档是否存在（UPDATE-GUIDELINES.md, knowledge/README.md）
- ✅ 输出彩色检查报告

**使用方法**：
```bash
cd /Users/dj/.claude/skills/illustration-converter
./check-skill-structure.sh
```

**使用时机**：每次更新后运行

**当前状态**：
```
📄 SKILL.md 行数: 443 ✅
📚 knowledge/ 文档数量: 13 ✅
✅ 更新规范文档存在
✅ knowledge/README.md 存在
```

---

### 第3层：Hook 提醒（skill-update-guard-hook.js）

**位置**：`/Users/dj/Desktop/小静的skills/config/claude-hooks/skill-update-guard-hook.js`

**全局链接**：`/Users/dj/.claude/hooks/skill-update-guard-hook.js`

**功能**：
- 🔍 自动检测更新关键词（"更新 SKILL.md"、"修改 SKILL.md"等）
- 📢 在用户输入后立即显示提醒
- 📋 显示检查清单
- 📖 提示阅读 UPDATE-GUIDELINES.md

**触发关键词**：
- 更新 SKILL.md
- 修改 SKILL.md
- 优化 Skill
- 更新 skill
- 添加到 SKILL.md
- 编辑 SKILL.md
- update SKILL.md
- modify SKILL.md
- edit SKILL.md

**工作原理**：
1. Claude Code 在用户输入后自动调用所有 hooks
2. Hook 读取用户输入，检测关键词
3. 如果匹配，输出提醒信息
4. Claude 看到提醒，在执行更新前会注意遵循规范

**示例输出**：
```
⚠️ 检测到 Skill 更新操作

请遵循以下原则：
1. SKILL.md 保持精简（< 500 行）
2. 详细内容放在 knowledge/
3. 通过引用而非复制关联内容

详细规范：UPDATE-GUIDELINES.md

请在更新前完成检查清单：
- [ ] 这个内容是核心流程吗？
- [ ] 是否会造成重复？
- [ ] SKILL.md 是否保持精简？

更新完成后请运行：./check-skill-structure.sh
```

---

### 第4层：SKILL.md 提醒

**位置**：SKILL.md 的"更新规范"章节（第385行）

**内容**：
```markdown
## 📝 更新规范

**重要**：更新本 Skill 时，必须遵循"渐进式披露"和"Skill 精简"原则

**核心原则**：
- SKILL.md 保持精简（< 500 行）
- 详细内容放在 knowledge/ 目录
- 通过引用而非复制关联内容

**详细更新规范**：`UPDATE-GUIDELINES.md`

**自动检查工具**：`./check-skill-structure.sh`
```

**作用**：在 SKILL.md 中直接提醒更新者

---

## 📊 系统架构图

```
用户输入："更新 SKILL.md，添加新功能"
    ↓
[Hook 层] skill-update-guard-hook.js
    ↓ 检测关键词
    ↓ 输出提醒
    ↓
Claude 看到提醒
    ↓
[文档层] 读取 UPDATE-GUIDELINES.md
    ↓
[执行层] 遵循规范执行更新
    ↓
[检查层] 运行 check-skill-structure.sh
    ↓
完成更新
```

---

## 🔄 标准更新流程

### 步骤1：更新前（自动触发）
1. 用户输入包含更新关键词
2. Hook 自动检测并显示提醒
3. Claude 读取 UPDATE-GUIDELINES.md
4. Claude 完成更新前检查清单

### 步骤2：执行更新
1. 判断内容类型（核心流程 vs 详细内容）
2. 决定放置位置（SKILL.md vs knowledge/）
3. 如果是详细内容 → 创建/更新 knowledge/ 文档
4. 如果是核心流程 → 在 SKILL.md 简要说明 + 引用
5. 更新 knowledge/README.md（如果需要）

### 步骤3：更新后（手动执行）
1. 运行 `./check-skill-structure.sh`
2. 检查输出，确保所有检查通过
3. 完成更新后检查清单
4. 更新版本号和更新日志

---

## 🎯 快速决策指南

### 问：这个内容应该放在哪里？

```
是核心工作流程？
├─ 是 → SKILL.md（1-3句简要说明）
│         + knowledge/（详细内容）
│         + SKILL.md 中添加引用
└─ 否 → knowledge/（详细内容）
          + SKILL.md 中添加引用（如果需要）
```

### 问：如何判断是否"核心工作流程"？

**核心工作流程**：
- ✅ 用户执行 Skill 必须知道的步骤
- ✅ 影响 Skill 执行顺序的决策点
- ✅ 必须的输入/输出说明

**不是核心流程**：
- ❌ 详细的技术实现
- ❌ 完整的 Prompt 模板
- ❌ 问题分析和案例
- ❌ 优化历程和记录

---

## 📈 系统验证

### 验证 Hook 是否安装

```bash
ls -la /Users/dj/.claude/hooks/ | grep skill-update
```

**期望输出**：
```
lrwxr-xr-x  1 dj  staff  80 Feb  2 01:02 skill-update-guard-hook.js -> /Users/dj/Desktop/小静的skills/config/claude-hooks/skill-update-guard-hook.js
```

### 验证文档是否完整

```bash
cd /Users/dj/.claude/skills/illustration-converter
./check-skill-structure.sh
```

**期望输出**：
```
📄 SKILL.md 行数: 443 ✅
📚 knowledge/ 文档数量: 13 ✅
✅ 更新规范文档存在
✅ knowledge/README.md 存在
```

### 测试 Hook 是否工作

在 Claude Code 中输入：
```
更新 SKILL.md，添加新功能
```

**期望行为**：
- Hook 自动触发
- 显示提醒信息
- Claude 在执行前读取 UPDATE-GUIDELINES.md

---

## 🔧 维护指南

### 定期维护（建议每月）

1. **运行结构检查**
   ```bash
   cd /Users/dj/.claude/skills/illustration-converter
   ./check-skill-structure.sh
   ```

2. **审查 SKILL.md**
   - 是否有内容可以移到 knowledge/
   - 是否有过时的内容
   - 引用是否清晰

3. **整理 knowledge/**
   - 合并相似文档
   - 更新过时信息
   - 检查引用关系

### 发现问题时

1. **SKILL.md 过长**
   - 识别可以移到 knowledge/ 的内容
   - 创建对应的 knowledge/ 文档
   - 在 SKILL.md 中用引用替代

2. **内容重复**
   - 确定权威来源（通常是 knowledge/）
   - 删除重复内容
   - 添加引用

3. **Hook 不工作**
   - 检查 Hook 文件是否存在
   - 检查 Hook 是否可执行（chmod +x）
   - 检查符号链接是否正确

---

## 💡 最佳实践

### 1. 先写详细，再提炼
- 先在 knowledge/ 写完整文档
- 再提炼核心要点到 SKILL.md
- 这样可以确保 SKILL.md 保持精简

### 2. 使用明确的引用
```markdown
✅ 详见 `knowledge/xxx.md`
✅ 参考 `knowledge/xxx.md` 的 [章节名称]
❌ 详见相关文档（不明确）
```

### 3. 定期运行检查
- 每次更新后运行
- 每月定期检查
- 发现问题及时调整

### 4. 信任 Hook 系统
- Hook 会自动提醒
- 不需要手动记住规则
- 专注于内容质量

---

## 📚 相关文档

| 文档 | 位置 | 用途 |
|------|------|------|
| UPDATE-GUIDELINES.md | 当前目录 | 完整更新规范 |
| check-skill-structure.sh | 当前目录 | 自动检查脚本 |
| skill-update-guard-hook.js | config/claude-hooks/ | Hook 实现 |
| HOW-TO-MAINTAIN-ARCHITECTURE.md | 当前目录 | 架构维护指南 |
| knowledge/README.md | knowledge/ | 文档结构说明 |
| SKILL.md | 当前目录 | 主文档（含更新规范章节） |

---

## ✅ 系统状态总结

### 已完成的工作

1. ✅ **文档规范层**
   - UPDATE-GUIDELINES.md（完整更新规范）
   - HOW-TO-MAINTAIN-ARCHITECTURE.md（架构维护指南）

2. ✅ **自动检查层**
   - check-skill-structure.sh（结构检查脚本）
   - 可执行权限已设置

3. ✅ **Hook 提醒层**
   - skill-update-guard-hook.js（Hook 实现）
   - 已安装到全局 hooks 目录
   - 符号链接已创建

4. ✅ **SKILL.md 提醒层**
   - "更新规范"章节已添加
   - 引用了 UPDATE-GUIDELINES.md

5. ✅ **验证测试**
   - 结构检查通过（443行，13个文档）
   - Hook 安装验证通过

### 系统优势

1. **自动化**：Hook 自动检测，无需手动记忆
2. **多层保障**：4层机制确保不遗漏
3. **易于维护**：清晰的文档和工具
4. **可扩展**：可以添加更多检查规则

### 使用建议

1. **更新前**：等待 Hook 提醒，阅读 UPDATE-GUIDELINES.md
2. **更新时**：遵循决策树和场景规范
3. **更新后**：运行 check-skill-structure.sh
4. **定期**：每月审查和整理

---

## 🎓 学习资源

### 理解架构原则

**渐进式披露（Progressive Disclosure）**：
- 用户首先看到最重要的信息
- 详细信息通过引用逐步展开
- 避免信息过载

**Skill 精简（Skill Simplicity）**：
- 保持 SKILL.md 简洁易读
- 通过引用而非复制关联内容
- 便于维护和更新

### 三个关键问题

每次更新时问自己：
1. 这个内容是核心流程吗？
2. 是否会造成重复？
3. SKILL.md 是否保持精简？

### 一个核心原则

**SKILL.md 精简，knowledge/ 详细，通过引用关联**

---

**创建时间**：2026-02-02
**适用范围**：illustration-converter Skill
**维护者**：所有更新 Skill 的人员
**系统版本**：v1.0
