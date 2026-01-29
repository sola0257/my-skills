# Skills 自迭代系统 Hooks 分析报告

**分析日期**：2026-01-29
**问题**：为什么 hooks 没有自动检测到"缺少网络搜索"的问题？

---

## 📋 现有 Hooks 清单

### 1. quality-evaluator-hook.js
**触发时机**：Skill 执行后（ToolUseResult）
**检测内容**：
- ✅ 结构完整性（必需元素）
- ✅ 信任型调性符合度
- ✅ 合规性（违禁词）
- ✅ 账号阶段适配

**局限性**：
- ❌ 不检测执行流程完整性
- ❌ 不检测是否跳过步骤
- ❌ 不检测知识来源质量
- ❌ 只评估"内容质量"，不评估"生成过程"

### 2. continuous-learning-hook.js
**触发时机**：会话结束时（SessionEnd）
**检测内容**：
- ✅ Skill 使用情况统计
- ✅ 成功模式提取
- ✅ 失败案例收集
- ✅ 优化建议生成

**局限性**：
- ❌ 会话结束才触发，无法实时检测
- ❌ 主要是统计分析，不是流程检查
- ❌ 依赖会话数据，可能无法捕获细节

### 3. skill-change-detector.js
**触发时机**：检测 git 变更
**检测内容**：
- ✅ SKILL.md 文件变更
- ✅ 版本号变化
- ✅ 变更类型分析
- ✅ 同步建议生成

**局限性**：
- ❌ 只检测文件变更，不检测执行过程
- ❌ 事后检测，不是实时检测

### 4. skill-activation-hook.js
**触发时机**：（未读取，待分析）

---

## 🔍 本次问题分析

### 问题描述
在生成君子兰冬季养护的订阅号长文时：
1. 我跳过了"网络搜索"步骤
2. 仅使用本地知识库生成内容
3. 没有进行知识整合和归档

### 为什么 Hooks 没有检测到？

**quality-evaluator-hook**：
- 只评估生成的"内容质量"（调性、合规性等）
- 不评估"生成过程"是否完整
- 即使内容质量合格，也无法发现流程缺陷

**continuous-learning-hook**：
- 会话结束才触发，此时内容已生成
- 主要是统计分析，不是流程审计
- 无法实时检测执行步骤的遗漏

**skill-change-detector**：
- 只检测文件变更，不检测执行过程
- 与本次问题无关

---

## 🚨 缺失的 Hook

### 需要：Skill 执行流程审计 Hook

**名称**：`skill-execution-auditor-hook.js`
**触发时机**：Skill 执行过程中或执行后
**检测内容**：

1. **步骤完整性检查**
   - 读取 SKILL.md 的执行流程（Step 1, 2, 3...）
   - 检测实际执行的步骤
   - 标记跳过的步骤

2. **必需步骤验证**
   - 定义哪些步骤是必需的
   - 检测是否执行了必需步骤
   - 例如：内容生成类 Skills 必须进行知识搜索

3. **知识来源审计**
   - 检测是否进行了网络搜索
   - 检测是否使用了本地知识库
   - 检测是否进行了知识整合

4. **输出质量审计**
   - 检测是否生成了所有必需的输出文件
   - 检测是否进行了知识归档
   - 检测是否记录了知识来源

### 实现方案

```javascript
#!/usr/bin/env node

/**
 * Skill Execution Auditor Hook
 *
 * 审计 Skill 执行流程的完整性
 * Hook 类型: ToolUseResult
 */

const fs = require('fs');
const path = require('path');

// 读取 SKILL.md 获取执行流程
function getExpectedSteps(skillName) {
  const skillPath = path.join(
    process.env.HOME,
    '.claude/skills',
    skillName,
    'SKILL.md'
  );

  if (!fs.existsSync(skillPath)) {
    return [];
  }

  const content = fs.readFileSync(skillPath, 'utf-8');
  const steps = [];

  // 提取 Step 1, Step 2, Step 3...
  const stepMatches = content.matchAll(/### Step (\d+): (.+)/g);
  for (const match of stepMatches) {
    steps.push({
      number: parseInt(match[1]),
      title: match[2],
      required: isRequiredStep(match[2])
    });
  }

  return steps;
}

// 判断步骤是否必需
function isRequiredStep(stepTitle) {
  const requiredKeywords = [
    '网络搜索',
    '知识搜索',
    '知识整合',
    '违禁词检查',
    '质量验证'
  ];

  return requiredKeywords.some(keyword => stepTitle.includes(keyword));
}

// 检测实际执行的步骤
function detectExecutedSteps(toolResult) {
  const executed = [];

  // 检测网络搜索
  if (toolResult.includes('WebSearch') || toolResult.includes('网络搜索')) {
    executed.push('网络搜索');
  }

  // 检测本地搜索
  if (toolResult.includes('Glob') || toolResult.includes('Grep')) {
    executed.push('本地搜索');
  }

  // 检测知识整合
  if (toolResult.includes('知识整合') || toolResult.includes('整合')) {
    executed.push('知识整合');
  }

  // 检测违禁词检查
  if (toolResult.includes('compliance-checker') || toolResult.includes('违禁词')) {
    executed.push('违禁词检查');
  }

  return executed;
}

// 审计执行流程
function auditExecution(skillName, toolResult) {
  const expectedSteps = getExpectedSteps(skillName);
  const executedSteps = detectExecutedSteps(toolResult);

  const audit = {
    skill: skillName,
    expected_steps: expectedSteps.length,
    executed_steps: executedSteps.length,
    missing_steps: [],
    warnings: []
  };

  // 检查缺失的必需步骤
  for (const step of expectedSteps) {
    if (step.required) {
      const executed = executedSteps.some(e =>
        step.title.includes(e) || e.includes(step.title)
      );

      if (!executed) {
        audit.missing_steps.push(step.title);
        audit.warnings.push(
          `⚠️ 缺少必需步骤: ${step.title}`
        );
      }
    }
  }

  return audit;
}

// 主执行逻辑
const toolName = process.env.TOOL_NAME || '';
const toolResult = process.env.TOOL_RESULT || '';

// 检查是否是内容生成 Skill
const contentSkills = [
  'xiaohongshu-content-generator',
  'wechat-content-generator',
  'video-script-generator'
];

const skillName = contentSkills.find(skill => toolName.includes(skill));

if (skillName) {
  const audit = auditExecution(skillName, toolResult);

  if (audit.warnings.length > 0) {
    console.log('\\n[执行流程审计] 发现问题:');
    audit.warnings.forEach(w => console.log(`  ${w}`));
    console.log('\\n建议:');
    console.log('  - 检查 SKILL.md 的执行流程');
    console.log('  - 确保所有必需步骤都已执行');
    console.log('  - 考虑更新 Skill 以自动执行缺失步骤');
  } else {
    console.log('\\n[执行流程审计] ✅ 执行流程完整');
  }
}

process.exit(0);
```

---

## 📊 对比分析

| Hook | 检测时机 | 检测内容 | 能否发现本次问题 |
|------|---------|---------|----------------|
| quality-evaluator | 执行后 | 内容质量 | ❌ 否 |
| continuous-learning | 会话结束 | 使用统计 | ❌ 否 |
| skill-change-detector | git 变更 | 文件变更 | ❌ 否 |
| **skill-execution-auditor** | **执行后** | **流程完整性** | **✅ 是** |

---

## 🎯 改进建议

### 1. 立即实施
- [ ] 创建 `skill-execution-auditor-hook.js`
- [ ] 配置 hook 触发规则
- [ ] 测试 hook 是否能检测到流程缺陷

### 2. 增强现有 Hooks
- [ ] **quality-evaluator**：添加"知识来源"评估维度
- [ ] **continuous-learning**：添加"流程完整性"分析

### 3. 完善 SKILL.md
- [ ] 在 SKILL.md 中明确标注必需步骤
- [ ] 使用特殊标记（如 `[必需]`）标识关键步骤
- [ ] 添加步骤依赖关系说明

### 4. 更新 skill-standards
- [ ] 添加"执行流程审计"规则（R12）
- [ ] 更新 optimization-rules.md
- [ ] 更新 self-check-list.md

---

## 🔄 自动化流程设计

### 理想的自动检测流程

```
Skill 执行开始
    ↓
[Hook] 记录执行开始时间
    ↓
Skill 执行中...
    ↓
[Hook] 监控工具调用（WebSearch, Glob, Grep等）
    ↓
Skill 执行完成
    ↓
[Hook] skill-execution-auditor
    ├─ 读取 SKILL.md 期望步骤
    ├─ 检测实际执行步骤
    ├─ 对比并标记缺失步骤
    └─ 输出审计报告
    ↓
[Hook] quality-evaluator
    ├─ 评估内容质量
    └─ 输出质量报告
    ↓
如果发现问题
    ├─ 输出警告信息
    ├─ 记录到 learned-patterns.json
    └─ 建议优化方案
    ↓
会话结束
    ↓
[Hook] continuous-learning
    ├─ 分析整体使用情况
    ├─ 提取成功/失败模式
    └─ 生成优化建议
```

---

## 📝 总结

### 问题根源
现有 hooks 主要关注"内容质量"和"使用统计"，缺少"执行流程完整性"的审计机制。

### 解决方案
创建 `skill-execution-auditor-hook.js`，在 Skill 执行后自动审计流程完整性，检测缺失的必需步骤。

### 预期效果
- ✅ 自动检测流程缺陷
- ✅ 实时提供改进建议
- ✅ 减少人工发现问题的依赖
- ✅ 提升 Skills 执行质量

---

**报告生成时间**：2026-01-29 17:15
**下一步行动**：创建 skill-execution-auditor-hook.js
