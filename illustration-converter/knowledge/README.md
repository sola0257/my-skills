# Knowledge 目录说明

本目录包含 illustration-converter skill 的所有知识文档，遵循"渐进式披露"原则。

---

## 📁 文档结构

### 核心模板（必读）
- `style-prompt-templates.md` - 10种风格的完整 Prompt 模板
- `style-model-mapping.md` - 风格-模型映射表
- `professional-painting-steps.md` - 各画种的学术标准步骤定义

### 质量保证（v2.1 新增）
- `quick-reference-guide.md` ⭐ **生成前必读** - 检查清单和快速修复
- `anti-patterns-cases.md` ⭐ **遇到问题时查阅** - 5大反面案例和解决方案
- `user-aesthetic-preferences.md` ⭐ **了解用户偏好** - 审美习惯和判断标准
- `complete-optimization-record.md` - 完整优化记录（6轮优化历程）
- `cross-style-issue-analysis.md` - 跨画风问题分析
- `universal-optimization-log.md` - 通用优化应用日志

---

## 🎯 使用指南

### 场景1：生成新插画前
**必读**：`quick-reference-guide.md`
- 检查 Prompt 是否包含必要约束
- 避免使用禁止词汇
- 使用推荐词汇和模板

### 场景2：生成结果不理想
**查阅**：`anti-patterns-cases.md`
- 识别问题类型（风格、构图、逻辑等）
- 查找对应的反面案例
- 应用正确的 Prompt 修复

### 场景3：了解用户审美偏好
**查阅**：`user-aesthetic-preferences.md`
- 核心审美原则
- 具体审美要求
- 判断标准

### 场景4：深入了解优化历程
**查阅**：`complete-optimization-record.md`
- 6轮优化的完整记录
- 每个问题的根本原因
- 最终优化策略

---

## 📋 文档关系

```
SKILL.md (精简版，核心流程)
    ↓ 引用
knowledge/
    ├── quick-reference-guide.md (快速参考)
    │   ↓ 引用
    ├── anti-patterns-cases.md (反面案例)
    ├── user-aesthetic-preferences.md (用户偏好)
    │   ↓ 详细记录
    └── complete-optimization-record.md (完整记录)
```

---

## 🔄 更新原则

### 渐进式披露
- SKILL.md：只包含核心流程和简要说明
- knowledge/：包含详细内容、案例、分析

### Skill 精简
- 不在 SKILL.md 中重复 knowledge/ 的内容
- 通过引用而非复制来关联文档
- 保持 SKILL.md 的可读性和可维护性

---

## 📝 维护指南

### 添加新文档时
1. 在 knowledge/ 目录创建文档
2. 在 SKILL.md 的"Knowledge"章节添加引用
3. 更新本 README.md
4. 确保文档之间的引用关系清晰

### 更新现有文档时
1. 直接更新 knowledge/ 中的文档
2. 不需要修改 SKILL.md（除非流程变化）
3. 保持文档版本记录

---

**创建时间**：2026-02-02
**遵循原则**：渐进式披露、Skill 精简
