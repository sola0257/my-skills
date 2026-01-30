# 场景化工作流升级完成报告

**完成日期**：2026-01-30
**升级范围**：所有内容生成类 Skills

---

## ✅ 已完成的修改

### 1. wechat-content-generator

**文件**：`/Users/dj/.claude/skills/wechat-content-generator/SKILL.md`

**版本**：v4.0 → v4.1

**修改内容**：
- ✅ 增加场景识别部分
- ✅ 增加流程B：编辑内容（Step E0-E6）
- ✅ 增加编辑场景检查清单
- ✅ 强调质量检查不能省略

---

### 2. xiaohongshu-content-generator

**文件**：`/Users/dj/.claude/skills/xiaohongshu-content-generator/SKILL.md`

**版本**：v8.0 → v8.1

**修改内容**：
- ✅ 增加场景识别部分
- ✅ 增加流程B：编辑内容（Step E0-E6）
- ✅ 增加编辑场景检查清单
- ✅ 强调小红书特定规范（双标题、12-15张配图、封面设计）

---

### 3. video-script-generator

**文件**：`/Users/dj/.claude/skills/video-script-generator/SKILL.md`

**版本**：v3.0 → v3.1

**修改内容**：
- ✅ 增加场景识别部分
- ✅ 增加流程B：编辑内容（Step E0-E6）
- ✅ 增加编辑场景检查清单
- ✅ 强调视频特定规范（分镜结构、4平台封面、逐字稿质量）

---

### 4. 全局配置文件

**新建文件**：
1. ✅ `/Users/dj/Desktop/小静的skills/_global_config/content-editing-standards.md`
   - 编辑场景统一规范
   - 标准流程定义
   - 质量检查清单
   - 常见错误示例

2. ✅ `/Users/dj/Desktop/小静的skills/_global_config/scenario-based-workflow-upgrade.md`
   - 升级记录
   - 使用示例
   - 预期效果

3. ✅ `/Users/dj/Desktop/小静的skills/_global_config/product-matching-rules-fix.md`
   - 商品匹配规则修正记录

4. ✅ `/Users/dj/Desktop/小静的skills/_global_config/unified-content-workflow.md`
   - 统一工作流文档（已更新商品匹配规则）

---

### 5. CLAUDE.md

**文件**：`/Users/dj/.claude/CLAUDE.md`

**修改内容**：
- ✅ 增加场景识别说明
- ✅ 增加新建内容工作流（8步）
- ✅ 增加编辑内容工作流（6步）
- ✅ 增加编辑场景规范文档链接
- ✅ 增加禁止行为：编辑场景跳过质量检查
- ✅ 修正商品匹配规则

---

## 🎯 核心改进

### 1. 场景识别机制

**新建内容场景**：
- 触发词："生成"、"创建"、"写一篇"
- 执行：完整工作流（Step 0-8/9）

**编辑内容场景**：
- 触发词："修改"、"优化"、"重写"
- 执行：简化工作流（Step E0-E6）

### 2. 编辑场景标准流程

```
Step E0: 场景识别和内容定位
Step E1: 读取已有内容
Step E2: 询问修改需求
Step E3: 执行修改
Step E4: 质量检查（强制，不能省略）✅
Step E5: 保存文件
Step E6: 询问后续操作
```

### 3. 质量检查不能省略

**所有平台共同检查**：
- ✅ 违禁词检查
- ✅ 配图规范检查
- ✅ 内容质量检查
- ✅ 账号阶段策略检查
- ✅ 信任型内容原则检查

**平台特定检查**：
- 小红书：双标题系统、12-15张配图、封面设计
- 微信：长文/图文格式、配图尺寸
- 视频：分镜结构、4平台封面、逐字稿质量

### 4. 商品匹配规则修正

**修正前**：
- 起号期：默认不执行商品匹配 ❌

**修正后**：
- 起号期：执行商品匹配，但仅作案例提及，禁止价格 ✅
- 成长期：软植入，评论区引导，可提价格 ✅
- 成熟期：可挂链接，可说价格，可直接推荐 ✅

---

## 📊 预期效果

### 效率提升

| 场景 | 之前 | 现在 | 提升 |
|------|------|------|------|
| 新建内容 | 完整流程 | 完整流程 | 无变化 |
| 编辑内容 | 完整流程或无流程 | 简化流程 | 50% |
| 质量保证 | 不稳定 | 稳定 | 100% |

### 质量保证

| 检查项 | 之前 | 现在 |
|-------|------|------|
| 场景识别 | 无 | 强制执行 |
| 违禁词检查 | 不稳定 | 强制执行 |
| 配图规范 | 不稳定 | 强制执行 |
| 账号阶段策略 | 不稳定 | 强制执行 |
| 信任型原则 | 不稳定 | 强制执行 |

---

## 📋 使用指南

### 新建内容

```
用户：生成一篇订阅号长文，主题是多肉养护
↓
AI：识别为"新建内容"场景
↓
执行：完整工作流（Step 0-8）
```

### 编辑内容

```
用户：修改昨天生成的订阅号文章，优化一下标题
↓
AI：识别为"编辑内容"场景
↓
执行：简化工作流（Step E0-E6）
- 读取已有内容
- 询问修改需求
- 执行修改
- 质量检查（强制）✅
- 保存
- 询问是否推送
```

### 重写内容

```
用户：重写一下这篇文章，增加商品推荐
↓
AI：识别为"编辑内容"场景（重写）
↓
执行：简化工作流（Step E0-E6）
- 读取原文章
- 分析账号阶段（起号期）
- 重写内容，增加商品案例提及（不是推荐）
- 质量检查（强制）✅
  - 确认商品植入方式：仅作案例提及，无价格
  - 违禁词检查：通过
  - 配图规范检查：通过
- 保存
- 询问是否推送
```

---

## 🔑 关键要点

### 1. 场景识别是第一步

**每次执行内容生成任务时，第一步就是识别场景**：
- 新建 or 编辑？
- 根据场景选择对应流程

### 2. 编辑场景有明确流程

**不再是"随意修改"**：
- 有标准的6步流程
- 质量检查是强制步骤
- 不能因为是"修改"就降低要求

### 3. 质量检查不能省略

**这是最关键的改进**：
- 编辑场景虽然简化了前期步骤
- 但质量检查不能省略
- 所有 Skill 规范都必须遵循

### 4. 商品匹配规则已修正

**起号期也可以执行商品匹配**：
- 目的是了解有哪些相关商品
- 但只能"仅作案例提及"
- 禁止价格，禁止直接推荐

---

## 📁 文件清单

### 已修改的文件

1. ✅ `/Users/dj/.claude/skills/wechat-content-generator/SKILL.md` (v4.1)
2. ✅ `/Users/dj/.claude/skills/xiaohongshu-content-generator/SKILL.md` (v8.1)
3. ✅ `/Users/dj/.claude/skills/video-script-generator/SKILL.md` (v3.1)
4. ✅ `/Users/dj/.claude/CLAUDE.md`

### 新建的文件

1. ✅ `/Users/dj/Desktop/小静的skills/_global_config/content-editing-standards.md`
2. ✅ `/Users/dj/Desktop/小静的skills/_global_config/scenario-based-workflow-upgrade.md`
3. ✅ `/Users/dj/Desktop/小静的skills/_global_config/product-matching-rules-fix.md`
4. ✅ `/Users/dj/Desktop/小静的skills/_global_config/content-workbench-prd.md`

### 已更新的文件

1. ✅ `/Users/dj/Desktop/小静的skills/_global_config/unified-content-workflow.md`

---

## 🎉 升级完成

所有内容生成类 Skills 已完成场景化工作流升级！

**现在的工作流**：
- ✅ 区分新建和编辑场景
- ✅ 新建场景：完整工作流（苏格拉底式提问 + 去重检查 + 静默执行）
- ✅ 编辑场景：简化工作流（跳过前期步骤 + 强制质量检查）
- ✅ 商品匹配规则已修正
- ✅ 所有 Skill 规范都必须遵循

**下一步**：
- 测试新的工作流
- 验证是否按照新流程执行
- 检查是否还有重复沟通的问题

---

**升级完成时间**：2026-01-30
**升级人**：Claude (claude-sonnet-4-5-20250929-thinking)
