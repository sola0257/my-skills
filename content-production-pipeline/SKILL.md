# 智能内容生产流水线 v1.5（精简版）

**版本**：v1.5
**更新日期**：2026-01-29
**重大变更**：按照四层机制精简 SKILL.md

---

## 🚨 静默执行协议

**执行规则：**
- ❌ 禁止请求确认以继续
- ✅ 必须一次性完成整个流水线
- ✅ 自动处理错误并继续

---

## 📋 核心功能

自动完成全流程：
1. 选题发现（topic-discovery）
2. 平台选题分配
3. 小红书内容生成
4. 公众号内容生成
5. 视频脚本生成

---

## 🔄 执行流程

### Step 1: 选题发现 [必需]
- 调用 topic-discovery skill
- 获取3-5个选题

### Step 2: 平台分配 [必需]
- 同一天不同平台使用不同选题
- 避免内容重复

### Step 3: 内容生成 [必需]
- 调用 xiaohongshu-content-generator
- 调用 wechat-content-generator
- 调用 video-script-generator

### Step 4: 进度追踪 [必需]
- 记录每个步骤的状态
- 错误恢复机制

**检查点**：
- [ ] 已完成选题发现
- [ ] 已完成平台分配
- [ ] 已生成所有平台内容

---

## 📦 输出结构

```
/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/
├── 小红书/2026-01-29_选题A/
├── 订阅号/2026-01-29_选题B/
└── 视频脚本/2026-01-29_选题C/
```

---

## 🔧 依赖

- `topic-discovery` (Skill)
- `xiaohongshu-content-generator` (Skill)
- `wechat-content-generator` (Skill)
- `video-script-generator` (Skill)

---

**版本历史**：
- v1.5 (2026-01-29): 按照四层机制精简 SKILL.md
- v1.4 (2026-01-25): 新增错误恢复机制
