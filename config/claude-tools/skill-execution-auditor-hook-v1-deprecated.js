#!/usr/bin/env node

/**
 * Skill Execution Auditor Hook for Claude Code
 *
 * 审计 Skill 执行流程的完整性
 * Hook 类型: ToolUseResult
 */

const fs = require('fs');
const path = require('path');

// 配置路径
const instinctsPath = path.join(process.env.HOME, '.claude/skills/_global_config/instincts.json');

// 从环境变量获取工具调用信息
const toolName = process.env.TOOL_NAME || '';
const toolResult = process.env.TOOL_RESULT || '';

// 检查是否是 Skill 调用
// 通用检测：所有在 .claude/skills/ 目录下的 SKILL.md 都会被检测
// 真正的"所有 Skills"，无需命名规范限制
const isSkillCall = toolName.includes('/.claude/skills/') &&
                    toolName.endsWith('/SKILL.md');

if (!isSkillCall) {
  // 不是 Skill 调用，跳过审计
  process.exit(0);
}

// 提取 Skill 名称
const skillName = toolName.split('/').pop().replace('.md', '');

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
    const stepTitle = match[2];
    steps.push({
      number: parseInt(match[1]),
      title: stepTitle,
      required: stepTitle.includes('[必需]') || stepTitle.includes('必须')
    });
  }

  return steps;
}

// 检测实际执行的步骤
function detectExecutedSteps(toolResult) {
  const executed = [];

  // 检测网络搜索
  if (toolResult.includes('WebSearch') || toolResult.includes('网络搜索') || toolResult.includes('web search')) {
    executed.push('网络搜索');
  }

  // 检测本地搜索
  if (toolResult.includes('Glob') || toolResult.includes('Grep') || toolResult.includes('本地搜索')) {
    executed.push('本地搜索');
  }

  // 检测知识整合
  if (toolResult.includes('知识整合') || toolResult.includes('整合') || toolResult.includes('integration')) {
    executed.push('知识整合');
  }

  // 检测违禁词检查
  if (toolResult.includes('compliance-checker') || toolResult.includes('违禁词')) {
    executed.push('违禁词检查');
  }

  // 检测知识归档
  if (toolResult.includes('知识归档') || toolResult.includes('归档') || toolResult.includes('archive')) {
    executed.push('知识归档');
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
      const stepKeywords = step.title.toLowerCase();
      const executed = executedSteps.some(e => {
        const keyword = e.toLowerCase();
        return stepKeywords.includes(keyword) || keyword.includes(stepKeywords.split('[')[0].trim().toLowerCase());
      });

      if (!executed) {
        audit.missing_steps.push(step.title);
        audit.warnings.push(
          `⚠️ 缺少必需步骤: ${step.title.replace('[必需]', '').trim()}`
        );
      }
    }
  }

  return audit;
}

// 记录问题到 instincts.json
function recordToInstincts(skillName, missingSteps) {
  let instincts = {
    last_updated: null,
    skill_issues: [],
    reminders: []
  };

  try {
    if (fs.existsSync(instinctsPath)) {
      instincts = JSON.parse(fs.readFileSync(instinctsPath, 'utf-8'));
    }
  } catch (e) {
    console.error('[执行流程审计] 无法读取 instincts.json');
  }

  // 更新或添加问题记录
  const existingIssue = instincts.skill_issues.find(issue => issue.skill === skillName);

  if (existingIssue) {
    existingIssue.issue = `跳过了步骤: ${missingSteps.join(', ')}`;
    existingIssue.detected_at = new Date().toISOString();
    existingIssue.frequency = (existingIssue.frequency || 1) + 1;
  } else {
    instincts.skill_issues.push({
      skill: skillName,
      issue: `跳过了步骤: ${missingSteps.join(', ')}`,
      detected_at: new Date().toISOString(),
      frequency: 1,
      status: 'active'
    });
  }

  // 更新提醒
  const existingReminder = instincts.reminders.find(r => r.skill === skillName);
  const reminderMessage = `上次执行时跳过了 ${missingSteps.join(', ')}，这次请确保执行`;

  if (existingReminder) {
    existingReminder.message = reminderMessage;
    existingReminder.priority = 'high';
  } else {
    instincts.reminders.push({
      skill: skillName,
      message: reminderMessage,
      priority: 'high'
    });
  }

  instincts.last_updated = new Date().toISOString();

  // 保存更新后的数据
  try {
    const dir = path.dirname(instinctsPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(instinctsPath, JSON.stringify(instincts, null, 2));
  } catch (e) {
    console.error('[执行流程审计] 无法保存 instincts.json:', e.message);
  }
}

// 执行审计
const audit = auditExecution(skillName, toolResult);

if (audit.warnings.length > 0) {
  console.log('\n[执行流程审计] 发现问题:');
  audit.warnings.forEach(w => console.log(`  ${w}`));
  console.log('\n建议:');
  console.log('  - 检查 SKILL.md 的执行流程');
  console.log('  - 确保所有必需步骤都已执行');
  console.log('  - 参考: /Users/dj/Desktop/小静的skills/skill-standards/knowledge/execution-quality-assurance.md');

  // 记录问题
  recordToInstincts(skillName, audit.missing_steps);
  console.log(`\n问题已记录到: ${instinctsPath}`);
} else {
  console.log('\n[执行流程审计] ✅ 执行流程完整');
}

process.exit(0);
