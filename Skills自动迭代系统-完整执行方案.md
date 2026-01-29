# Skills 自动迭代系统 - 完整执行方案

> **文档用途**：本文档是 Opus 4.5 Thinking 与用户深度讨论后的完整方案，供后续会话继续执行。
> **创建时间**：2026-01-27
> **状态**：待执行

---

## 第一部分：项目背景与痛点分析

### 1.1 用户原始痛点（完整复述）

用户在使用 Claude Code / OpenCode 的 Skills 系统时，遇到以下问题：

1. **新建 Skills 没有标准架构体系**
2. **使用率不高，有的 Skills 建完就搁置**
3. **大模型不知道什么时候调用哪个 Skill，除非明确调用**
4. **执行结果质量不稳定，有时满意有时很差**
5. **技能体系越来越庞大混乱**
6. **规则制定有矛盾点，前后不统一**
7. **需要 Skills 能够自动迭代，而不是手动更新**

用户背景：无编程基础，以 AI 深度使用者身份使用 Claude Code / OpenCode。

### 1.2 痛点因果链分析

```
┌─────────────────────────────────────────────────────────────────────┐
│                        痛点因果链                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [根因1] 没有标准架构 ──────┬──→ [症状A] 结构不一致                  │
│                            ├──→ [症状B] 规则矛盾/冲突                │
│                            └──→ [症状C] 维护越来越混乱               │
│                                                                     │
│  [根因2] 没有自动激活机制 ──┬──→ [症状D] 大模型不知道调用哪个         │
│                            └──→ [症状E] 使用率低，Skills闲置         │
│                                                                     │
│  [根因3] 没有质量评估机制 ──┬──→ [症状F] 执行结果质量不稳定           │
│                            └──→ [症状G] 不知道什么是「好」的输出      │
│                                                                     │
│  [根因4] 没有学习反馈机制 ──┬──→ [症状H] 需要手动迭代                 │
│                            └──→ [症状I] 每次优化可能引入新矛盾        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.3 关键发现：hooks 目录不存在

诊断时发现：
- `~/.claude/hooks/` 目录 **不存在**
- `~/.claude/settings.json` 中没有 hooks 配置
- 这是导致「Skills 不能自动激活」的根本原因

### 1.4 用户环境信息

| 工具 | 版本 | 说明 |
|------|------|------|
| Claude Code | 2.1.20 | 支持 hooks |
| OpenCode | 1.1.36 | 支持 plugins（更强大） |
| 主要使用 | OpenCode | 用户表示 OpenCode 使用频率更高 |

---

## 第二部分：三个开源项目的核心贡献

用户提供了三个 GitHub 开源项目作为参考：

### 2.1 diet103/claude-code-infrastructure-showcase

**项目地址**：https://github.com/diet103/claude-code-infrastructure-showcase
**Star 数**：8.6k
**核心贡献**：

1. **skill-rules.json** - 定义每个 Skill 的触发条件
2. **UserPromptSubmit hook** - 分析用户输入，自动建议 Skill
3. **PostToolUse hook** - 追踪工具使用情况
4. **500行规则** - 主文件 <500 行，复杂内容放 resources/

**关键机制**：
```json
// skill-rules.json 示例
{
  "xiaohongshu-content-generator": {
    "triggers": [
      {"type": "keyword", "keywords": ["小红书", "种草", "笔记"]},
      {"type": "file_pattern", "pattern": "**/小红书/**"}
    ],
    "auto_suggest": true
  }
}
```

### 2.2 affaan-m/everything-claude-code

**项目地址**：https://github.com/affaan-m/everything-claude-code
**核心贡献**：

1. **continuous-learning-v2** - 持续学习系统
2. **eval-harness** - 质量评估框架
3. **verification-loop** - 验证循环机制
4. **instinct 数据结构** - 学习积累的模式记录

**instinct 数据结构**：
```json
{
  "id": "instinct-001",
  "pattern": "生成订阅号内容时，用户偏好深度干货类型",
  "confidence": 0.85,
  "usage_count": 12,
  "success_rate": 0.92,
  "context": {
    "skill": "wechat-content-generator",
    "content_type": "深度干货"
  }
}
```

### 2.3 hesreallyhim/awesome-claude-code

**项目地址**：https://github.com/hesreallyhim/awesome-claude-code
**核心贡献**：

- 社区最佳实践汇总
- 各种 Skill 模板参考
- 配置示例

### 2.4 三个项目解决的问题对照

| 用户痛点 | 解决方案来源 |
|----------|--------------|
| Skill 调用不稳定 | diet103: skill-rules.json + hooks |
| 质量不稳定 | affaan-m: eval-harness + verification-loop |
| 手动维护负担重 | affaan-m: continuous-learning-v2 |
| 不知道何时调用 | diet103: UserPromptSubmit hook |

---

## 第三部分：用户现有 Skills 清单

用户在 `~/.claude/skills/` 下有 **20 个 Skills**（通过符号链接指向 `/Users/dj/Desktop/小静的skills/`）：

### 3.1 内容生产类（高频使用）

| Skill | 用途 | 行数 | 评估 |
|-------|------|------|------|
| xiaohongshu-content-generator | 小红书图文生成 | 175 | ✅ 优秀 |
| wechat-content-generator | 微信公众号内容生成 | - | 高频 |
| video-script-generator | 视频脚本生成 | - | 高频 |
| content-production-workflow | 内容生产工作流（指挥中心） | 389 | ✅ 良好 |

### 3.2 选题与热点类

| Skill | 用途 |
|-------|------|
| topic-discovery | 选题发现（基于热点，不绑定商品库） |
| marketing-calendar | 营销日历（节气、节日） |

### 3.3 商品相关类

| Skill | 用途 |
|-------|------|
| product-catalog | 商品库管理 |
| product-selector | 选品分析 |
| product-optimizer | 商品优化 |
| product-pipeline | 商品优化流水线 |

### 3.4 账号与数据类

| Skill | 用途 |
|-------|------|
| account-stage-manager | 账号阶段管理（粉丝数、互动数据） |
| competitor-monitor | 对标账号监控 |
| traffic-diagnosis | 流量诊断与二发优化 |

### 3.5 工具类

| Skill | 用途 |
|-------|------|
| compliance-checker | 违禁词检查 |
| knowledge-extractor | 知识文档整理 |
| docs-scraper | 文档网站抓取 |
| pdf-processing | PDF处理 |

### 3.6 Skill 开发类

| Skill | 用途 |
|-------|------|
| skill-standards | Skill 开发标准规范库 |
| skill-suitability-evaluator | Skill 适配性评估 |

### 3.7 已弃用

| Skill | 说明 |
|-------|------|
| content-production-pipeline | 已弃用，被 content-production-workflow 替代 |

---

## 第四部分：规则体系诊断

### 4.1 四层规则结构

用户的规则体系分布在多个位置，形成四层结构：

```
┌────────────────────────────────────────────────────────────────────────────┐
│                              规则体系完整地图                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  【最高层】CLAUDE.md 账号阶段配置                                            │
│  ├── 位置：~/.claude/CLAUDE.md                                             │
│  ├── 内容：各平台粉丝数、账号阶段、商品策略                                   │
│  └── 状态：✅ 存在，Skills 会读取                                           │
│                                                                            │
│  【品牌层】慢养四季调性规则                                                   │
│  ├── 位置：/Documents/slowseasons AI工厂/_shared_knowledge/project_slowseasons/│
│  │   ├── 慢养四季_品牌风格指南.md（核心调性）                                 │
│  │   └── 慢养四季_各平台定位策略.md（平台分工）                               │
│  └── 问题：❌ Skills 没有引用这些文件！【断裂点1】                            │
│                                                                            │
│  【技巧层】实操手册 + 博主经验                                                │
│  ├── 位置：/Desktop/全域自媒体运营/实操手册/                                  │
│  │   └── 绿植园艺全域运营实操手册（2026完全版）.md                            │
│  └── 问题：❌ 与品牌调性、账号阶段有冲突【断裂点2】                            │
│                                                                            │
│  【执行层】Skills 内部规则                                                    │
│  ├── 位置：~/.claude/skills/*/knowledge/*.md                                │
│  │   ├── content-generation-rules.md（禁止具体人设）                         │
│  │   └── xiaohongshu_tactics.md（双标题、钩子等）                            │
│  └── 问题：❌ 没有统一引用「品牌调性」源文件【断裂点3】                        │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 具体冲突点分析

#### 冲突1：商品/价格策略

| 来源 | 说法 | 用户实际情况 |
|------|------|--------------|
| 实操手册 L155 | "推荐具体商品（给出价格和理由）" | 用户在起号期，不应该说价格 |
| xiaohongshu SKILL L42 | "起号期：纯干货，商品仅作为道具" | ✅ 这个是对的 |
| CLAUDE.md | "禁止价格" | ✅ 这个是对的 |

**解决方案**：实操手册的「商品推荐」段落需要改为「账号阶段适配版」

#### 冲突2：人设/第一人称

| 来源 | 说法 | 品牌调性要求 |
|------|------|--------------|
| 实操手册 L91 | "这份《北京花市地图》我整理了3天..." | 具体人设 |
| content-generation-rules.md | "禁止设定具体人设" | 禁止 |
| 品牌风格指南 L39 | "第一人称分享（根据平台调整）" | 可以用"我"，但不能具体化 |

**解决方案**：三者其实不矛盾，需要明确规则：
- ✅ 可以用「我」
- ❌ 不能说「我去年春天...」「我养花3年...」
- ✅ 可以说「我发现这个方法很有效」（泛化的我）

#### 冲突3：品牌调性 vs 平台特色

用户反馈：后期没有引入品牌调性，因为发现会限制内容生成方向。

**分析对比**：

| 维度 | 品牌调性要求 | 小红书起号策略 | 冲突程度 |
|------|-------------|---------------|---------|
| 标题 | "禁止夸张标题" | "痛点+情绪+数字" | ⚠️ 中度冲突 |
| 钩子 | "平静、温和、不急促" | "制造焦虑" "利益前置" | ⚠️ 中度冲突 |
| 语气 | "朋友分享，不是推销" | "强留粉钩子" | ⚠️ 轻度冲突 |
| 视觉 | "克制、不过度修图" | "精致美学、高对比度" | ✅ 不冲突 |
| 专业 | "真实、专业、有支撑" | "干货、知识科普" | ✅ 不冲突 |

### 4.3 解决方案：分阶段调性策略

**用户确认同意此方案**：

```
起号期（0-2000粉）：
├── 放宽：可以用情绪化标题、可以用钩子、可以蹭热点
├── 保留底线：不虚假承诺、不过度营销、保持专业
└── 目标：先起量，建立粉丝基础

成长期（2000-10000粉）：
├── 逐步收紧：标题情绪化减少，内容深度增加
├── 开始建立IP：慢养四季的调性开始渗透
└── 目标：精准粉丝，建立信任

成熟期（10000+粉）：
├── 完全回归调性：自然、克制、温和、专业、治愈
├── 品牌IP明确：用户一看就知道是"慢养四季"
└── 目标：变现闭环
```

### 4.4 规则优先级系统

```
优先级高 → 优先级低

账号阶段规则 > 品牌调性规则 > Skill 内部规则 > 实操手册模板
     ↑                                              ↓
  动态（会变）                                    静态（参考）
```

**效果**：
- 账号阶段「起号期」→ 自动放宽调性限制
- 品牌调性「禁止夸张」→ 保留底线（不虚假承诺）
- 实操手册仅作为「可选参考」，不强制执行

---

## 第五部分：系统架构设计

### 5.1 完整四层架构

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                       Skills 自动迭代系统 v1.1 - 完整架构                              │
├───────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│  │ 配置层（知识统一源）                                                              │ │
│  ├─────────────────────────────────────────────────────────────────────────────────┤ │
│  │ ~/.claude/                                                                       │ │
│  │ ├── CLAUDE.md                    # 账号阶段配置（最高优先级）                     │ │
│  │ └── skills/                                                                      │ │
│  │     ├── _global_config/          # 全局配置目录（新建）                          │ │
│  │     │   ├── rule-priority.json   # 规则优先级 + 分阶段调性配置                   │ │
│  │     │   ├── brand-tonality.md    # 品牌调性（符号链接）                          │ │
│  │     │   ├── platform-strategy.md # 平台定位策略（符号链接）                      │ │
│  │     │   ├── skill-rules.json     # 22个 Skill 触发规则                          │ │
│  │     │   ├── quality-standards.json # 质量评估标准                               │ │
│  │     │   └── instincts.json       # 学习积累                                     │ │
│  │     └── [各个 Skill 目录]                                                        │ │
│  └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 1: 自动激活层                                                               │ │
│  ├─────────────────────────────────────────────────────────────────────────────────┤ │
│  │ OpenCode Plugin: skill-activation.ts                                             │ │
│  │ ├── 监听事件：tool.execute.before                                                │ │
│  │ ├── 读取：skill-rules.json                                                       │ │
│  │ ├── 匹配用户输入 → 建议相关 Skill                                                │ │
│  │ └── 兼容 Claude Code：通过 settings.json 配置 hooks                              │ │
│  │                                                                                   │ │
│  │ 效果：用户说"帮我写个小红书笔记"→ 自动建议 xiaohongshu-content-generator         │ │
│  └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 2: 规则注入层                                                               │ │
│  ├─────────────────────────────────────────────────────────────────────────────────┤ │
│  │ 执行顺序：                                                                        │ │
│  │ 1. 读取 CLAUDE.md → 获取账号阶段                                                  │ │
│  │ 2. 读取 rule-priority.json → 获取当前阶段的调性配置                              │ │
│  │ 3. 读取 brand-tonality.md → 获取品牌调性底线                                     │ │
│  │ 4. 读取 Skill 内部规则 → 获取平台特有规则                                        │ │
│  │ 5. 按优先级合并 → 生成最终执行规则                                                │ │
│  │                                                                                   │ │
│  │ 效果：                                                                            │ │
│  │ ├── 账号阶段「起号期」→ 自动放宽调性限制                                         │ │
│  │ ├── 品牌调性「禁止虚假承诺」→ 保留底线                                           │ │
│  │ └── 实操手册仅作为「可选参考」                                                    │ │
│  └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 3: 质量评估层                                                               │ │
│  ├─────────────────────────────────────────────────────────────────────────────────┤ │
│  │ OpenCode Plugin: quality-evaluator.ts                                            │ │
│  │ ├── 监听事件：tool.execute.after                                                 │ │
│  │ ├── 读取：quality-standards.json                                                 │ │
│  │ ├── 评估维度：结构完整性、调性符合度、合规性、账号阶段适配                        │ │
│  │ ├── 不合格 → 自动重试（最多 3 次）                                               │ │
│  │ └── 记录评分 → 用于后续学习                                                      │ │
│  │                                                                                   │ │
│  │ 效果：生成内容后自动评估，不合格自动重试                                          │ │
│  └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│  │ Layer 4: 持续学习层（含自动迭代）                                                 │ │
│  ├─────────────────────────────────────────────────────────────────────────────────┤ │
│  │                                                                                   │ │
│  │ 【输入源1】内部：会话执行结果                                                     │ │
│  │ ├── 成功模式提取 → instincts.json                                               │ │
│  │ └── 失败模式标记 → 避免重复                                                      │ │
│  │                                                                                   │ │
│  │ 【输入源2】外部：competitor-monitor                                               │ │
│  │ ├── 对标账号爆文分析 → 发现成功模式                                              │ │
│  │ ├── 热门标题/封面拆解 → 更新内容生成模板                                         │ │
│  │ └── 选题热度趋势 → 更新 topic-discovery 策略                                     │ │
│  │                                                                                   │ │
│  │ 【输入源3】外部：traffic-diagnosis                                                │ │
│  │ ├── 笔记表现数据 → 诊断问题根因                                                  │ │
│  │ ├── CTR/互动率分析 → 更新封面/标题规则                                           │ │
│  │ └── 二发成功案例 → 学习有效优化模式                                              │ │
│  │                                                                                   │ │
│  │ 【处理机制】                                                                      │ │
│  │ ├── 模式聚类 → 发现高频成功模式                                                  │ │
│  │ ├── 规则更新建议 → 人工确认后执行（自动发现+人工确认模式）                        │ │
│  │ └── Skill 迭代建议 → 人工确认后执行                                              │ │
│  │                                                                                   │ │
│  │ 【输出】                                                                          │ │
│  │ ├── 更新 skill-rules.json（触发规则）                                            │ │
│  │ ├── 更新 quality-standards.json（质量标准）                                      │ │
│  │ ├── 更新各 Skill 的 knowledge/*.md（平台规则）                                   │ │
│  │ └── 生成新 Skill（如发现新的高频模式）                                           │ │
│  │                                                                                   │ │
│  │ 【自动报告（每周）】                                                              │ │
│  │ ├── Skill 使用率排名                                                             │ │
│  │ ├── 质量评分统计                                                                 │ │
│  │ ├── 需要优化的 Skill 清单                                                        │ │
│  │ └── 新发现的模式清单                                                             │ │
│  │                                                                                   │ │
│  └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 学习闭环流程

```
competitor-monitor（成功案例）
        ↓
    学习成功模式
        ↓
更新内容生成规则 ←─────────────┐
        ↓                      │
   生成新内容                   │
        ↓                      │
   发布到平台                   │
        ↓                      │
traffic-diagnosis（分析表现）   │
        ↓                      │
   如果成功 → 强化模式 ─────────┘
   如果失败 → 调整规则 ─────────┘
```

### 5.3 全局配置生效范围

| 目录 | Claude Code | OpenCode | 任意目录生效 |
|------|-------------|----------|-------------|
| `~/.claude/skills/` | ✅ 支持 | ✅ 支持 | ✅ 是 |
| `~/.claude/CLAUDE.md` | ✅ 支持 | ✅ 支持 | ✅ 是 |
| `~/.config/opencode/plugins/` | ❌ | ✅ 支持 | ✅ 是（仅 OpenCode） |

**结论**：`~/.claude/skills/_global_config/` 是全局目录，无论在哪个文件夹打开 terminal 都会生效

---

## 第六部分：22个 Skills 触发规则配置

### 6.1 skill-rules.json 完整配置

```json
{
  "version": "1.0",
  "description": "Skills 自动激活触发规则配置",
  "last_updated": "2026-01-27",
  
  "skills": {
    "xiaohongshu-content-generator": {
      "triggers": [
        {"type": "keyword", "keywords": ["小红书", "种草", "笔记", "xhs"]},
        {"type": "file_pattern", "pattern": "**/小红书/**"},
        {"type": "intent", "intents": ["生成小红书内容", "写小红书"]}
      ],
      "priority": "high",
      "auto_suggest": true,
      "dependencies": ["compliance-checker", "account-stage-manager"]
    },
    
    "wechat-content-generator": {
      "triggers": [
        {"type": "keyword", "keywords": ["公众号", "订阅号", "服务号", "微信文章"]},
        {"type": "file_pattern", "pattern": "**/订阅号/**"},
        {"type": "file_pattern", "pattern": "**/服务号/**"}
      ],
      "priority": "high",
      "auto_suggest": true,
      "dependencies": ["compliance-checker", "account-stage-manager"]
    },
    
    "video-script-generator": {
      "triggers": [
        {"type": "keyword", "keywords": ["视频脚本", "视频号", "抖音", "快手", "短视频"]},
        {"type": "file_pattern", "pattern": "**/视频脚本/**"}
      ],
      "priority": "high",
      "auto_suggest": true,
      "dependencies": ["compliance-checker", "account-stage-manager"]
    },
    
    "content-production-workflow": {
      "triggers": [
        {"type": "keyword", "keywords": ["内容规划", "周内容", "排期", "批量生成"]},
        {"type": "intent", "intents": ["规划本周内容", "生成排期表"]}
      ],
      "priority": "high",
      "auto_suggest": true,
      "note": "这是内容生产的指挥中心，会调用其他内容生成 Skills"
    },
    
    "topic-discovery": {
      "triggers": [
        {"type": "keyword", "keywords": ["选题", "热点", "爆款", "趋势"]},
        {"type": "intent", "intents": ["找选题", "搜索热点"]}
      ],
      "priority": "medium",
      "auto_suggest": true
    },
    
    "marketing-calendar": {
      "triggers": [
        {"type": "keyword", "keywords": ["营销日历", "节气", "节日", "营销节点"]},
        {"type": "intent", "intents": ["查看营销节点", "今天有什么节日"]}
      ],
      "priority": "medium",
      "auto_suggest": true
    },
    
    "product-catalog": {
      "triggers": [
        {"type": "keyword", "keywords": ["商品库", "商品数据", "有赞商品"]},
        {"type": "file_pattern", "pattern": "**/商品库/**"}
      ],
      "priority": "low",
      "auto_suggest": false,
      "note": "内部服务技能，通常被其他 Skill 调用"
    },
    
    "product-selector": {
      "triggers": [
        {"type": "keyword", "keywords": ["选品", "1688", "爆款潜力"]},
        {"type": "intent", "intents": ["分析选品", "推荐商品"]}
      ],
      "priority": "medium",
      "auto_suggest": true
    },
    
    "product-optimizer": {
      "triggers": [
        {"type": "keyword", "keywords": ["商品优化", "SKU精简", "卖点提炼"]},
        {"type": "intent", "intents": ["优化商品", "提炼卖点"]}
      ],
      "priority": "medium",
      "auto_suggest": true
    },
    
    "product-pipeline": {
      "triggers": [
        {"type": "keyword", "keywords": ["商品流水线", "批量优化商品"]},
        {"type": "file_pattern", "pattern": "**/商品/**/*.xlsx"}
      ],
      "priority": "medium",
      "auto_suggest": true
    },
    
    "account-stage-manager": {
      "triggers": [
        {"type": "keyword", "keywords": ["账号阶段", "粉丝数", "更新粉丝"]},
        {"type": "intent", "intents": ["更新账号状态", "查看账号阶段"]}
      ],
      "priority": "high",
      "auto_suggest": true,
      "note": "账号阶段变更会影响所有内容生成 Skills 的行为"
    },
    
    "competitor-monitor": {
      "triggers": [
        {"type": "keyword", "keywords": ["对标账号", "竞品分析", "爆文分析"]},
        {"type": "intent", "intents": ["分析对标", "找对标账号"]}
      ],
      "priority": "medium",
      "auto_suggest": true,
      "note": "需要 MediaCrawler 支持"
    },
    
    "traffic-diagnosis": {
      "triggers": [
        {"type": "keyword", "keywords": ["流量诊断", "二发", "数据分析", "CTR"]},
        {"type": "intent", "intents": ["分析笔记数据", "诊断流量问题"]}
      ],
      "priority": "medium",
      "auto_suggest": true
    },
    
    "compliance-checker": {
      "triggers": [
        {"type": "keyword", "keywords": ["违禁词", "合规检查", "敏感词"]},
        {"type": "intent", "intents": ["检查违禁词", "文案合规"]}
      ],
      "priority": "high",
      "auto_suggest": false,
      "note": "通常被内容生成 Skills 自动调用"
    },
    
    "knowledge-extractor": {
      "triggers": [
        {"type": "keyword", "keywords": ["知识整理", "提取方法论", "文档整理"]},
        {"type": "file_pattern", "pattern": "**/知识库/**"}
      ],
      "priority": "low",
      "auto_suggest": true
    },
    
    "docs-scraper": {
      "triggers": [
        {"type": "keyword", "keywords": ["抓取文档", "下载文档", "同步文档"]},
        {"type": "intent", "intents": ["抓取网页文档", "下载帮助文档"]}
      ],
      "priority": "low",
      "auto_suggest": true
    },
    
    "pdf-processing": {
      "triggers": [
        {"type": "keyword", "keywords": ["PDF", "转换PDF", "处理PDF"]},
        {"type": "file_pattern", "pattern": "**/*.pdf"}
      ],
      "priority": "low",
      "auto_suggest": true
    },
    
    "skill-standards": {
      "triggers": [
        {"type": "keyword", "keywords": ["创建Skill", "优化Skill", "Skill规范"]},
        {"type": "intent", "intents": ["新建技能", "优化技能"]}
      ],
      "priority": "medium",
      "auto_suggest": true,
      "note": "Skill 开发的标准规范库"
    },
    
    "skill-suitability-evaluator": {
      "triggers": [
        {"type": "keyword", "keywords": ["评估Skill", "是否适合做Skill"]},
        {"type": "intent", "intents": ["判断任务是否适合做成Skill"]}
      ],
      "priority": "low",
      "auto_suggest": true
    }
  },
  
  "global_settings": {
    "default_auto_suggest": false,
    "suggestion_threshold": 0.7,
    "max_suggestions": 3
  }
}
```

### 6.2 触发规则说明

| 触发类型 | 说明 | 示例 |
|----------|------|------|
| keyword | 用户输入包含关键词 | "帮我写个小红书笔记" → 匹配"小红书" |
| file_pattern | 当前操作的文件路径匹配 | 编辑 `/小红书/xxx.md` → 匹配 |
| intent | 用户意图识别 | "生成小红书内容" → 匹配意图 |

### 6.3 优先级说明

| 优先级 | 说明 | Skills |
|--------|------|--------|
| high | 高频使用，优先建议 | 内容生成类、账号管理类 |
| medium | 中频使用 | 选题、商品、诊断类 |
| low | 低频或内部调用 | 工具类、开发类 |

---

## 第七部分：完整文件清单

### 7.1 需要创建的文件

| 文件路径 | 类型 | 用途 | Phase |
|----------|------|------|-------|
| `/Users/dj/Desktop/全域自媒体运营/品牌调性/` | 目录 | 品牌调性文件新位置 | 0 |
| `/Users/dj/Desktop/全域自媒体运营/品牌调性/慢养四季_品牌风格指南.md` | 迁移 | 从 Slow Seasons 迁移 | 0 |
| `/Users/dj/Desktop/全域自媒体运营/品牌调性/慢养四季_各平台定位策略.md` | 迁移 | 从 Slow Seasons 迁移 | 0 |
| `/Users/dj/Desktop/全域自媒体运营/品牌调性/分阶段调性配置.md` | 新建 | 起号期/成长期/成熟期调性 | 0 |
| `~/.claude/skills/_global_config/` | 目录 | 全局配置目录 | 0 |
| `~/.claude/skills/_global_config/rule-priority.json` | 新建 | 规则优先级 + 分阶段调性 | 0 |
| `~/.claude/skills/_global_config/skill-rules.json` | 新建 | 22个 Skill 触发规则 | 0 |
| `~/.claude/skills/_global_config/brand-tonality.md` | 符号链接 | → 品牌调性/慢养四季_品牌风格指南.md | 0 |
| `~/.claude/skills/_global_config/platform-strategy.md` | 符号链接 | → 品牌调性/慢养四季_各平台定位策略.md | 0 |
| `~/.claude/skills/_global_config/stage-tonality.md` | 符号链接 | → 品牌调性/分阶段调性配置.md | 0 |
| `~/.config/opencode/plugins/skill-activation.ts` | 新建 | 自动激活插件 | 1 |
| `~/.claude/settings.json` | 修改 | 添加 hooks 配置 | 1 |
| `~/.claude/skills/_global_config/quality-standards.json` | 新建 | 质量评估标准 | 2 |
| `~/.config/opencode/plugins/quality-evaluator.ts` | 新建 | 质量评估插件 | 2 |
| `~/.claude/skills/_global_config/instincts.json` | 新建 | 学习积累（初始为空） | 3 |
| `~/.config/opencode/plugins/continuous-learning.ts` | 新建 | 持续学习插件 | 3 |

### 7.2 需要修改的文件

| 文件路径 | 修改内容 | Phase |
|----------|----------|-------|
| `~/.claude/skills/competitor-monitor/SKILL.md` | 新增学习模块触发 | 3 |
| `~/.claude/skills/traffic-diagnosis/SKILL.md` | 新增问题记录功能 | 3 |
| 各内容生成 Skill | 添加品牌调性引用声明 | 1 |

---

## 第八部分：详细执行步骤

### Phase 0：配置层搭建（Day 1）

#### Step 0.1：创建品牌调性目录

```bash
mkdir -p "/Users/dj/Desktop/全域自媒体运营/品牌调性"
```

#### Step 0.2：迁移品牌调性文件

从 Slow Seasons AI工厂 复制以下文件：
- 源：`/Users/dj/Documents/slowseasons AI工厂/_shared_knowledge/project_slowseasons/慢养四季_品牌风格指南.md`
- 目标：`/Users/dj/Desktop/全域自媒体运营/品牌调性/慢养四季_品牌风格指南.md`

- 源：`/Users/dj/Documents/slowseasons AI工厂/_shared_knowledge/project_slowseasons/慢养四季_各平台定位策略.md`
- 目标：`/Users/dj/Desktop/全域自媒体运营/品牌调性/慢养四季_各平台定位策略.md`

#### Step 0.3：创建分阶段调性配置

创建文件：`/Users/dj/Desktop/全域自媒体运营/品牌调性/分阶段调性配置.md`

内容：
```markdown
# 分阶段调性配置

## 起号期（0-2000粉）

### 放宽规则
- ✅ 可以使用情绪化标题（痛点+情绪+数字）
- ✅ 可以使用钩子（利益前置、制造焦虑、身份认同）
- ✅ 可以蹭热点
- ✅ 可以使用强留粉钩子（关注我、收藏防走丢）

### 保留底线
- ❌ 禁止虚假承诺
- ❌ 禁止过度营销
- ❌ 禁止说商品价格
- ✅ 保持专业、真实

### 商品策略
- 商品仅作为道具提及
- 不挂链接
- 不说价格
- 评论区不引导购买

---

## 成长期（2000-10000粉）

### 调整规则
- 标题情绪化程度减少
- 内容深度增加
- 开始建立 IP 调性

### 商品策略
- 可软植入（1-2个要点提及）
- 评论区可引导询价
- 仍不说具体价格

---

## 成熟期（10000+粉）

### 完全回归品牌调性
- 自然、克制、温和、专业、治愈
- 品牌 IP 明确

### 商品策略
- 可挂链接
- 可说价格
- 正常带货
```

#### Step 0.4：创建全局配置目录

```bash
mkdir -p ~/.claude/skills/_global_config
```

#### Step 0.5：创建 rule-priority.json

创建文件：`~/.claude/skills/_global_config/rule-priority.json`

内容：
```json
{
  "version": "1.0",
  "description": "规则优先级配置",
  "last_updated": "2026-01-27",
  
  "priority_order": [
    {
      "level": 1,
      "name": "account_stage",
      "source": "CLAUDE.md + account-stage-manager",
      "description": "账号阶段规则，最高优先级"
    },
    {
      "level": 2,
      "name": "stage_tonality",
      "source": "_global_config/stage-tonality.md",
      "description": "分阶段调性配置"
    },
    {
      "level": 3,
      "name": "brand_tonality",
      "source": "_global_config/brand-tonality.md",
      "description": "品牌调性底线"
    },
    {
      "level": 4,
      "name": "skill_specific",
      "source": "各 Skill 的 knowledge/*.md",
      "description": "平台特有规则"
    },
    {
      "level": 5,
      "name": "handbook_reference",
      "source": "实操手册",
      "description": "参考资料，不强制执行"
    }
  ],
  
  "conflict_resolution": {
    "rule": "高优先级覆盖低优先级",
    "example": "账号阶段「起号期」说「禁止价格」→ 覆盖实操手册的「说价格」"
  }
}
```

#### Step 0.6：创建 skill-rules.json

创建文件：`~/.claude/skills/_global_config/skill-rules.json`

内容：参见第六部分的完整配置

#### Step 0.7：创建符号链接

```bash
# 品牌调性
ln -s "/Users/dj/Desktop/全域自媒体运营/品牌调性/慢养四季_品牌风格指南.md" \
      ~/.claude/skills/_global_config/brand-tonality.md

# 平台策略
ln -s "/Users/dj/Desktop/全域自媒体运营/品牌调性/慢养四季_各平台定位策略.md" \
      ~/.claude/skills/_global_config/platform-strategy.md

# 分阶段调性
ln -s "/Users/dj/Desktop/全域自媒体运营/品牌调性/分阶段调性配置.md" \
      ~/.claude/skills/_global_config/stage-tonality.md
```

---

### Phase 1：自动激活层（Week 1）

#### Step 1.1：创建 OpenCode 插件目录

```bash
mkdir -p ~/.config/opencode/plugins
```

#### Step 1.2：创建 skill-activation.ts

创建文件：`~/.config/opencode/plugins/skill-activation.ts`

内容：
```typescript
import type { Plugin } from "@opencode-ai/plugin"
import { readFileSync } from "fs"
import { join } from "path"

export const SkillActivationPlugin: Plugin = async (ctx) => {
  // 读取 skill-rules.json
  const rulesPath = join(process.env.HOME!, ".claude/skills/_global_config/skill-rules.json")
  let skillRules: any = { skills: {} }
  
  try {
    skillRules = JSON.parse(readFileSync(rulesPath, "utf-8"))
  } catch (e) {
    console.log("skill-rules.json not found, using defaults")
  }
  
  return {
    "tui.prompt.append": async (input, output) => {
      const userInput = output.prompt?.toLowerCase() || ""
      const suggestions: string[] = []
      
      // 遍历所有 skill 规则
      for (const [skillName, config] of Object.entries(skillRules.skills)) {
        const skillConfig = config as any
        if (!skillConfig.auto_suggest) continue
        
        // 检查关键词匹配
        for (const trigger of skillConfig.triggers || []) {
          if (trigger.type === "keyword") {
            for (const keyword of trigger.keywords || []) {
              if (userInput.includes(keyword.toLowerCase())) {
                suggestions.push(skillName)
                break
              }
            }
          }
        }
      }
      
      // 如果有匹配的 skill，添加提示
      if (suggestions.length > 0) {
        const uniqueSuggestions = [...new Set(suggestions)].slice(0, 3)
        output.prompt = `${output.prompt}\n\n[系统提示] 检测到可能需要使用以下 Skill：${uniqueSuggestions.join(", ")}`
      }
    }
  }
}
```

#### Step 1.3：修改 Claude Code settings.json（兼容）

修改文件：`~/.claude/settings.json`

添加 hooks 配置（如果 Claude Code 支持）：
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "node ~/.claude/hooks/skill-activation-hook.js"
      }
    ]
  }
}
```

---

### Phase 2：质量评估层（Week 2）

#### Step 2.1：创建 quality-standards.json

创建文件：`~/.claude/skills/_global_config/quality-standards.json`

内容：
```json
{
  "version": "1.0",
  "description": "内容质量评估标准",
  "last_updated": "2026-01-27",
  
  "platforms": {
    "xiaohongshu": {
      "dimensions": [
        {
          "name": "结构完整性",
          "weight": 25,
          "criteria": [
            "有视觉标题（≤20字）",
            "有正文（纯文本，无Markdown）",
            "有标签（≤10个）",
            "有封面图"
          ]
        },
        {
          "name": "调性符合度",
          "weight": 25,
          "criteria": [
            "符合当前账号阶段的调性要求",
            "无虚假承诺",
            "无过度营销"
          ]
        },
        {
          "name": "合规性",
          "weight": 25,
          "criteria": [
            "无违禁词",
            "无引流词",
            "无夸张绝对化用词"
          ]
        },
        {
          "name": "账号阶段适配",
          "weight": 25,
          "criteria": [
            "起号期：无价格、无购买引导",
            "成长期：软植入、评论区引导",
            "成熟期：可挂链接"
          ]
        }
      ],
      "pass_threshold": 70,
      "retry_on_fail": true,
      "max_retries": 3
    },
    
    "wechat_subscription": {
      "dimensions": [
        {
          "name": "结构完整性",
          "weight": 25,
          "criteria": [
            "有标题",
            "有摘要（≤25字）",
            "有正文（1000-3000字）",
            "有配图"
          ]
        },
        {
          "name": "内容深度",
          "weight": 30,
          "criteria": [
            "有专业知识支撑",
            "有实操步骤",
            "引用知识库干货"
          ]
        },
        {
          "name": "调性符合度",
          "weight": 20,
          "criteria": [
            "专业但亲切",
            "娓娓道来",
            "符合品牌调性"
          ]
        },
        {
          "name": "合规性",
          "weight": 25,
          "criteria": [
            "无违禁词",
            "无引流词"
          ]
        }
      ],
      "pass_threshold": 70,
      "retry_on_fail": true,
      "max_retries": 3
    }
  }
}
```

#### Step 2.2：创建 quality-evaluator.ts

创建文件：`~/.config/opencode/plugins/quality-evaluator.ts`

（插件代码，用于在内容生成后自动评估质量）

---

### Phase 3：持续学习层（Week 3）

#### Step 3.1：创建 instincts.json

创建文件：`~/.claude/skills/_global_config/instincts.json`

初始内容：
```json
{
  "version": "1.0",
  "description": "学习积累的模式",
  "last_updated": "2026-01-27",
  "instincts": [],
  "failed_patterns": [],
  "statistics": {
    "total_learned": 0,
    "promoted_to_rules": 0
  }
}
```

#### Step 3.2：创建 continuous-learning.ts

创建文件：`~/.config/opencode/plugins/continuous-learning.ts`

（插件代码，用于在会话结束时提取学习模式）

#### Step 3.3：修改 competitor-monitor

在 `~/.claude/skills/competitor-monitor/SKILL.md` 中添加：

```markdown
## 🔄 学习模块触发（v1.1 新增）

执行完成后，自动触发学习模块：
1. 提取爆文的成功模式（标题结构、封面特征）
2. 记录到 `_global_config/instincts.json`
3. 高频模式（出现 ≥2 次）自动提升为规则建议
```

#### Step 3.4：修改 traffic-diagnosis

在 `~/.claude/skills/traffic-diagnosis/SKILL.md` 中添加：

```markdown
## 🔄 问题记录功能（v1.1 新增）

诊断完成后，自动记录问题根因：
1. CTR 低 → 记录封面/标题问题模式
2. 互动率低 → 记录内容结构问题模式
3. 二发成功 → 记录有效优化模式
4. 所有记录存入 `_global_config/instincts.json`
```

---

### Phase 4：整合测试（Week 4）

#### Step 4.1：验证配置生效

```bash
# 检查符号链接
ls -la ~/.claude/skills/_global_config/

# 检查 skill-rules.json
cat ~/.claude/skills/_global_config/skill-rules.json | head -20

# 检查 OpenCode 插件
ls -la ~/.config/opencode/plugins/
```

#### Step 4.2：测试自动激活

1. 打开 OpenCode
2. 输入"帮我写个小红书笔记"
3. 验证是否自动建议 `xiaohongshu-content-generator`

#### Step 4.3：测试质量评估

1. 调用 `/xiaohongshu-content-generator`
2. 验证生成后是否有质量评分
3. 验证不合格时是否自动重试

#### Step 4.4：测试学习功能

1. 执行 `/competitor-monitor analyze`
2. 检查 `instincts.json` 是否有新记录
3. 执行 `/traffic-diagnosis` 分析一篇笔记
4. 检查问题模式是否被记录

---

## 第九部分：competitor-monitor 和 traffic-diagnosis 整合方案

### 9.1 competitor-monitor 改进

#### 现状
- 输出到 `选题库/`
- 只输出报告

#### 改进后
- 保留原输出，新增一份到 `_global_config/competitor-insights/`
- 新增：提取成功模式的标准化 JSON
- 新增：每次分析结果存档（追踪趋势变化）

#### 学习流程
```
/competitor-monitor analyze
       ↓
生成《对标账号分析报告.md》
       ↓
【新增】自动触发学习模块
       ↓
提取成功模式：
├── 爆款标题结构 → 更新 xiaohongshu_tactics.md 的标题模板
├── 高CTR封面特征 → 更新封面生成规则
├── 热门选题方向 → 通知 topic-discovery 优先关注
└── 记录到 instincts.json
```

### 9.2 traffic-diagnosis 改进

#### 现状
- 只输出诊断
- 二发方案是一次性的

#### 改进后
- 新增：问题根因记录到 instincts.json
- 新增：二发成功后记录成功模式
- 建议：每周自动诊断近7天发布的内容

#### 学习流程
```
/traffic-diagnosis [笔记数据]
       ↓
生成诊断报告 + 二发方案
       ↓
【新增】自动触发学习模块
       ↓
分析问题根因：
├── CTR 低 → 封面/标题规则需要调整
├── 互动率低 → 内容结构规则需要调整
├── 发布时间不佳 → 更新最佳发布时间配置
└── 记录问题模式到 instincts.json（标记为"避免"）
```

---

## 第十部分：品牌调性文件迁移方案

### 10.1 迁移清单

| 源文件 | 目标位置 |
|--------|----------|
| `/Documents/slowseasons AI工厂/_shared_knowledge/project_slowseasons/慢养四季_品牌风格指南.md` | `/Desktop/全域自媒体运营/品牌调性/慢养四季_品牌风格指南.md` |
| `/Documents/slowseasons AI工厂/_shared_knowledge/project_slowseasons/慢养四季_各平台定位策略.md` | `/Desktop/全域自媒体运营/品牌调性/慢养四季_各平台定位策略.md` |

### 10.2 符号链接配置

```bash
# 在 _global_config 中创建符号链接
ln -s "/Users/dj/Desktop/全域自媒体运营/品牌调性/慢养四季_品牌风格指南.md" \
      ~/.claude/skills/_global_config/brand-tonality.md

ln -s "/Users/dj/Desktop/全域自媒体运营/品牌调性/慢养四季_各平台定位策略.md" \
      ~/.claude/skills/_global_config/platform-strategy.md

ln -s "/Users/dj/Desktop/全域自媒体运营/品牌调性/分阶段调性配置.md" \
      ~/.claude/skills/_global_config/stage-tonality.md
```

### 10.3 Slow Seasons AI工厂 停用计划

1. 完成迁移后，保留原文件夹作为备份
2. 不再在该文件夹下创建新内容
3. 所有新内容生产工作在 `/Desktop/全域自媒体运营/` 下进行

---

## 第十一部分：关键决策记录

### 11.1 用户确认的决策

| 决策项 | 用户选择 | 说明 |
|--------|----------|------|
| 技术路线 | OpenCode 为主，兼容 Claude Code | OpenCode 使用频率更高 |
| 自动化程度 | 完全自动 | 系统自动判断用哪个 Skill |
| 质量评估 | 自动评分，不合格自动重试 | 最多重试 3 次 |
| 学习频率 | 每次对话后自动提取模式 | 实时学习 |
| 分阶段调性 | 同意 | 起号期放宽，成熟期收紧 |
| 自动迭代模式 | 自动发现 + 人工确认 | 避免 AI 乱改 |
| 品牌调性迁移 | 同意 | 迁移到「全域自媒体运营/品牌调性/」 |
| 全局配置目录命名 | 由 AI 决定 | 使用 `_global_config` |

### 11.2 Sonnet 4.5 Thinking vs Opus 4.5 Thinking 对比

| 维度 | Sonnet 4.5 Thinking | Opus 4.5 Thinking |
|------|---------------------|-------------------|
| 分析风格 | 战略架构设计 | 战术诊断审计 |
| 核心产出 | 完整的系统蓝图 | 现状问题诊断 |
| 优势 | 架构图清晰、时间规划详细 | 实际检查环境、读取现有文件 |
| 发现 | - | hooks 目录不存在、Skills 质量不错 |

**最终方案**：整合两者优点
- 保留 Sonnet 的四层架构思路
- 从 Opus 诊断的起点出发
- 由 Opus 执行（因为读过具体文件）

---

## 第十二部分：后续维护指南

### 12.1 日常使用

1. **正常使用 Skills**：系统会自动激活、评估、学习
2. **查看学习结果**：检查 `~/.claude/skills/_global_config/instincts.json`
3. **确认规则更新**：系统会生成建议，用户确认后执行

### 12.2 账号阶段更新

当粉丝数变化时：
1. 调用 `/account-stage-manager` 更新粉丝数
2. 系统自动判断新的账号阶段
3. 所有内容生成 Skills 自动适配新阶段的规则

### 12.3 添加新 Skill

1. 按照 `skill-standards` 的模板创建
2. 在 `skill-rules.json` 中添加触发规则
3. 系统自动识别并激活

### 12.4 问题排查

| 问题 | 排查方法 |
|------|----------|
| Skill 不自动激活 | 检查 `skill-rules.json` 中的触发规则 |
| 质量评估不生效 | 检查 `quality-standards.json` 配置 |
| 学习不记录 | 检查 `instincts.json` 权限 |
| 符号链接失效 | 重新创建符号链接 |

---

## 附录 A：慢养四季品牌调性核心要点

### 品牌基调
自然、克制、温和、专业、治愈、带一点点传统东方气质

### 核心特征
- ✅ 自然：贴近自然规律，不强求速成
- ✅ 克制：不夸张、不浮夸、不过度营销
- ✅ 温和：平静、温湿、具有生活气息
- ✅ 专业：基于真实经验，有专业支撑
- ✅ 治愈：提供情绪价值和美学体验

### 禁用风格
- ❌ 过度营销
- ❌ 过度学术论文化
- ❌ 过度标题党
- ❌ 浮夸表达
- ❌ 急促表达

---

## 附录 B：各平台定位速查

| 平台 | 任务层级 | 核心任务 | 内容形式 |
|------|----------|----------|----------|
| 小红书 | 理念层+能力层 | 理念传递+能力证明 | 美学展示+知识科普 |
| 快手 | 过程层 | 过程记录器和陪伴者 | 生活记录+知识科普 |
| 视频号 | 理念层 | 生活方式传播者 | 治愈系生活记录 |
| 抖音 | 理念层 | 生活方式展示器 | 视觉冲击短视频 |
| 订阅号 | 能力层 | 知识能力证明器 | 系统化知识文章 |
| 服务号 | 交易层 | 业务服务提供者 | 业务通知 |

---

## 附录 C：执行检查清单

### Phase 0 检查清单
- [ ] 创建 `/Desktop/全域自媒体运营/品牌调性/` 目录
- [ ] 迁移品牌调性文件
- [ ] 创建分阶段调性配置
- [ ] 创建 `~/.claude/skills/_global_config/` 目录
- [ ] 创建 `rule-priority.json`
- [ ] 创建 `skill-rules.json`
- [ ] 创建符号链接

### Phase 1 检查清单
- [ ] 创建 `~/.config/opencode/plugins/` 目录
- [ ] 创建 `skill-activation.ts`
- [ ] 修改 `settings.json`（如需要）
- [ ] 测试自动激活功能

### Phase 2 检查清单
- [ ] 创建 `quality-standards.json`
- [ ] 创建 `quality-evaluator.ts`
- [ ] 测试质量评估功能

### Phase 3 检查清单
- [ ] 创建 `instincts.json`
- [ ] 创建 `continuous-learning.ts`
- [ ] 修改 `competitor-monitor`
- [ ] 修改 `traffic-diagnosis`
- [ ] 测试学习功能

### Phase 4 检查清单
- [ ] 验证所有配置生效
- [ ] 端到端测试
- [ ] 修复发现的问题

---

**文档结束**

> 本文档由 Opus 4.5 Thinking 生成
> 创建时间：2026-01-27
> 用途：供后续会话继续执行
> 
> **下一步**：在新会话中读取本文档，从 Phase 0 开始执行

