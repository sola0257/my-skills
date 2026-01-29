# 四层机制使用指南

## 📋 快速参考

### 什么时候使用？

**场景1：发现 AI 跳过步骤**
```
症状：AI 在执行 Skill 时跳过了某些步骤
时机：用户发现问题后
指令：请阅读 /Users/dj/Desktop/小静的skills/skill-standards/knowledge/execution-quality-assurance.md
      然后按照四层机制修正 [skill-name] 的问题
```

**场景2：创建新 Skill**
```
症状：需要确保新 Skill 执行完整
时机：Skill 开发阶段
指令：参考 execution-quality-assurance.md 设计 Skill
```

**场景3：优化现有 Skill**
```
症状：Skill 经常被不完整执行
时机：Skill 优化阶段
指令：按照 execution-quality-assurance.md 的四层机制逐层检查
```

---

## 🎯 四层机制概览

```
第1层：指令层（SKILL.md）
  ↓ 标注 [必需] 步骤

第2层：规则层（CLAUDE.md）
  ↓ 全局强制规则

第3层：检测层（Hooks）
  ↓ 执行后检测

第4层：反馈层（instincts.json）
  ↓ 学习闭环
```

---

## 📖 完整文档

详细说明请查看：
`/Users/dj/Desktop/小静的skills/skill-standards/knowledge/execution-quality-assurance.md`

---

**最后更新**：2026-01-29
