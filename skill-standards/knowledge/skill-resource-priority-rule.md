# Skill 资源优先使用规则

> **创建日期**: 2026-01-29
> **目的**: 避免重复造轮子，优先使用 Skill 现有资源

---

## 问题背景

在执行任务时，AI 经常会直接开始编写新代码，而忽略了相关 Skill 下已经存在的脚本和工具。这导致：
- 重复工作
- 浪费时间
- 无法利用已有的经验和最佳实践

## 核心原则

**执行任务前，优先检查相关 Skill 的现有资源，避免重复造轮子。**

---

## 强制检查顺序

当需要执行某个平台或功能相关的操作时（如推送、发布、生成等），**必须**按以下顺序检查：

### 1. 检查对应 Skill 的 scripts/ 目录

```bash
# 示例：需要推送微信公众号文章
# 首先检查：/Users/dj/Desktop/小静的skills/wechat-content-generator/scripts/
ls -la /Users/dj/Desktop/小静的skills/[skill-name]/scripts/
```

### 2. 检查对应 Skill 的 knowledge/ 目录

```bash
# 查找相关文档和配置
ls -la /Users/dj/Desktop/小静的skills/[skill-name]/knowledge/
```

### 3. 检查 Skill 的 SKILL.md

```bash
# 查看 Skill 的使用说明和工作流程
```

### 4. 如果都没有，再考虑创建新的

---

## 平台与 Skill 对应关系

| 任务类型 | 对应 Skill | 优先检查目录 |
|---------|-----------|------------|
| 微信公众号推送/发布 | wechat-content-generator | scripts/wechat_publish.py |
| 小红书发布 | xiaohongshu-content-generator | scripts/ |
| 视频脚本生成 | video-script-generator | scripts/ |
| 商品管理 | product-catalog, product-optimizer | scripts/ |
| 内容生成 | 对应平台的 content-generator | knowledge/ + scripts/ |

---

## 行为规范

### ❌ 禁止的行为

**错误示例**：
```
用户：推送到订阅号草稿箱
Claude：让我创建一个推送脚本...（直接开始写代码）
```

**问题**：
- 没有检查现有资源
- 重复造轮子
- 浪费时间

### ✅ 正确的行为

**正确示例**：
```
用户：推送到订阅号草稿箱
Claude：让我先检查 wechat-content-generator 下是否有现成的推送脚本
       → 检查 scripts/ 目录
       → 找到 wechat_publish.py
       → 直接使用现有脚本
```

**优点**：
- 利用现有资源
- 节省时间
- 保持一致性

---

## 执行检查清单

执行任务前，自问：

- [ ] 这个任务是否与某个 Skill 相关？
- [ ] 我是否检查了该 Skill 的 scripts/ 目录？
- [ ] 我是否检查了该 Skill 的 knowledge/ 目录？
- [ ] 我是否阅读了该 Skill 的 SKILL.md？
- [ ] 如果有现成的脚本/工具，我是否优先使用？

---

## 为什么这个规则重要

### 1. 避免重复工作
现有脚本已经过测试和优化，直接使用可以节省大量时间。

### 2. 保持一致性
使用统一的工具和流程，确保所有操作的一致性。

### 3. 节省时间
不需要重新编写和调试代码。

### 4. 知识积累
现有资源包含了历史经验和最佳实践，直接使用可以避免重复踩坑。

---

## 实际案例

### 案例：推送微信公众号文章

**错误做法**：
1. 用户说"推送到订阅号草稿箱"
2. AI 直接开始编写新的推送脚本
3. 浪费时间重新实现已有功能

**正确做法**：
1. 用户说"推送到订阅号草稿箱"
2. AI 检查 `wechat-content-generator/scripts/`
3. 发现 `wechat_publish.py` 已存在
4. 直接使用现有脚本
5. 成功推送

**结果对比**：
- 错误做法：花费 10-15 分钟编写和调试
- 正确做法：花费 1-2 分钟检查和使用
- 节省时间：80-90%

---

## 规则执行

### 自动化检查

在 CLAUDE.md 中添加此规则，确保 AI 在执行任务前自动检查。

### 人工审查

如果发现 AI 没有遵循此规则，应该：
1. 指出问题
2. 要求 AI 先检查现有资源
3. 将此案例记录到 instincts.json

---

## 相关文档

- CLAUDE.md: 全局规则配置
- skill-standards/knowledge/optimization-rules.md: Skill 优化规则
- instincts.json: AI 学习记录

---

*创建日期：2026-01-29*
*版本：v1.0*
