#!/usr/bin/env node

/**
 * 通用 Skill 执行审计 Hook v2.0
 *
 * 功能：
 * 1. 检测执行流程完整性
 * 2. 检测输出质量（文件命名、数量、规格）
 * 3. 自动记录问题到 instincts.json
 * 4. 适用于所有 Skills
 *
 * Hook 类型: PostToolUse
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置路径
const HOME = process.env.HOME;
const instinctsPath = path.join(HOME, '.claude/skills/_global_config/instincts.json');
const skillsPath = path.join(HOME, 'Desktop/小静的skills');

// 从环境变量获取工具调用信息
const toolName = process.env.TOOL_NAME || '';
const toolResult = process.env.TOOL_RESULT || '';
const toolInput = process.env.TOOL_INPUT || '';

// 检查是否是 Skill 调用
const isSkillCall = toolName === 'Skill' || toolInput.includes('"skill":');

if (!isSkillCall) {
  process.exit(0);
}

// 提取 Skill 名称
function extractSkillName() {
  try {
    if (toolInput) {
      const inputObj = JSON.parse(toolInput);
      return inputObj.skill || '';
    }
  } catch (e) {
    // 尝试从字符串中提取
    const match = toolInput.match(/"skill":\s*"([^"]+)"/);
    if (match) return match[1];
  }
  return '';
}

const skillName = extractSkillName();

if (!skillName) {
  process.exit(0);
}

console.log(`\n[执行审计] 检查 ${skillName}...`);

// ==================== 1. 执行流程完整性检测 ====================

function getExpectedSteps(skillName) {
  const skillPath = path.join(skillsPath, skillName, 'SKILL.md');

  if (!fs.existsSync(skillPath)) {
    return [];
  }

  const content = fs.readFileSync(skillPath, 'utf-8');
  const steps = [];

  // 提取标记为必需的步骤
  const stepMatches = content.matchAll(/###?\s+(?:Step\s+\d+:|步骤\s*\d+[:：])\s*(.+?)(?:\[必需\]|\[REQUIRED\])?/gi);
  for (const match of stepMatches) {
    const stepTitle = match[1].trim();
    const isRequired = match[0].includes('[必需]') || match[0].includes('[REQUIRED]') || match[0].includes('必须');

    if (isRequired) {
      steps.push({
        title: stepTitle,
        required: true
      });
    }
  }

  return steps;
}

function detectExecutedSteps(toolResult) {
  const executed = [];

  // 检测各种常见步骤
  const stepPatterns = {
    '网络搜索': /WebSearch|网络搜索|web search/i,
    '本地搜索': /Glob|Grep|本地搜索/i,
    '读取指南': /Read.*guide\.md|读取.*指南/i,
    '违禁词检查': /compliance-checker|违禁词/i,
    '生成配图': /generate.*image|生成.*配图|配图生成/i,
    '知识归档': /知识归档|归档|archive/i
  };

  for (const [stepName, pattern] of Object.entries(stepPatterns)) {
    if (pattern.test(toolResult)) {
      executed.push(stepName);
    }
  }

  return executed;
}

// ==================== 2. 输出质量检测 ====================

function detectOutputQuality(skillName, toolResult) {
  const issues = [];

  // 根据 Skill 类型检测不同的输出质量
  if (skillName === 'xiaohongshu-content-generator') {
    issues.push(...checkXiaohongshuOutput(toolResult));
  } else if (skillName === 'wechat-content-generator') {
    issues.push(...checkWechatOutput(toolResult));
  } else if (skillName === 'video-script-generator') {
    issues.push(...checkVideoOutput(toolResult));
  }

  // 通用检查：是否生成了输出文件
  if (!toolResult.includes('saved') && !toolResult.includes('保存') && !toolResult.includes('生成')) {
    issues.push({
      type: 'output_missing',
      message: '未检测到输出文件生成'
    });
  }

  return issues;
}

function checkXiaohongshuOutput(toolResult) {
  const issues = [];

  // 检查配图数量
  const imageCountMatch = toolResult.match(/(\d+)张/);
  if (imageCountMatch) {
    const count = parseInt(imageCountMatch[1]);
    if (count < 12) {
      issues.push({
        type: 'image_count',
        message: `配图数量不足：${count}张（要求12-15张）`,
        severity: 'high'
      });
    }
  }

  // 检查封面命名
  if (toolResult.includes('cover.png') && !toolResult.includes('cover_')) {
    issues.push({
      type: 'cover_naming',
      message: '封面图命名缺少视觉标题，应为 cover_[视觉标题].png',
      severity: 'high'
    });
  }

  // 检查是否读取了配图指南
  if (toolResult.includes('配图') && !toolResult.includes('image-prompt-guide.md')) {
    issues.push({
      type: 'missing_guide',
      message: '生成配图前未读取 knowledge/image-prompt-guide.md',
      severity: 'high'
    });
  }

  // 检查混合风格
  if (toolResult.includes('配图') && !toolResult.includes('infographic') && !toolResult.includes('cozy-sketch')) {
    issues.push({
      type: 'style_mixing',
      message: '可能未使用混合风格策略（对比图、步骤图应使用不同风格）',
      severity: 'medium'
    });
  }

  return issues;
}

function checkWechatOutput(toolResult) {
  const issues = [];

  // 检查配图指南
  if (toolResult.includes('配图') && !toolResult.includes('wechat-image-prompt-guide.md')) {
    issues.push({
      type: 'missing_guide',
      message: '生成配图前未读取 knowledge/wechat-image-prompt-guide.md',
      severity: 'high'
    });
  }

  return issues;
}

function checkVideoOutput(toolResult) {
  const issues = [];

  // 检查视频配图指南
  if (toolResult.includes('配图') && !toolResult.includes('video-image-prompt-guide.md')) {
    issues.push({
      type: 'missing_guide',
      message: '生成配图前未读取 knowledge/video-image-prompt-guide.md',
      severity: 'high'
    });
  }

  return issues;
}

// ==================== 3. 记录到 instincts.json ====================

function loadInstincts() {
  let instincts = {
    last_updated: null,
    skill_issues: [],
    reminders: [],
    learned_patterns: []
  };

  try {
    if (fs.existsSync(instinctsPath)) {
      instincts = JSON.parse(fs.readFileSync(instinctsPath, 'utf-8'));
    }
  } catch (e) {
    console.error('[执行审计] 无法读取 instincts.json');
  }

  return instincts;
}

function saveInstincts(instincts) {
  try {
    const dir = path.dirname(instinctsPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    instincts.last_updated = new Date().toISOString();
    fs.writeFileSync(instinctsPath, JSON.stringify(instincts, null, 2));
  } catch (e) {
    console.error('[执行审计] 无法保存 instincts.json:', e.message);
  }
}

function recordIssue(instincts, skillName, issue) {
  const issueId = `${skillName}-${issue.type}-${Date.now()}`;

  // 检查是否已存在相同类型的问题
  const existingIssue = instincts.skill_issues.find(
    i => i.skill === skillName && i.issue.includes(issue.type)
  );

  if (existingIssue) {
    existingIssue.frequency = (existingIssue.frequency || 1) + 1;
    existingIssue.detected_at = new Date().toISOString();
    existingIssue.issue = issue.message;
  } else {
    instincts.skill_issues.push({
      id: issueId,
      skill: skillName,
      issue: issue.message,
      detected_at: new Date().toISOString(),
      frequency: 1,
      status: 'active',
      severity: issue.severity || 'medium',
      solution: generateSolution(issue)
    });
  }

  // 添加或更新提醒
  const existingReminder = instincts.reminders.find(r => r.skill === skillName && r.message.includes(issue.type));

  if (!existingReminder) {
    instincts.reminders.push({
      skill: skillName,
      message: issue.message,
      priority: issue.severity === 'high' ? 'high' : 'medium'
    });
  }
}

function generateSolution(issue) {
  const solutions = {
    'image_count': '确保生成12-15张配图，包含封面、对比图、步骤图、细节图',
    'cover_naming': '封面图必须命名为 cover_[视觉标题].png，从双标题系统获取视觉标题',
    'missing_guide': '生成配图前必须先读取对应平台的 image-prompt-guide.md',
    'style_mixing': '使用混合风格：对比图用 infographic-sketch，步骤图用 cozy-sketch，场景图用 dreamy-photo',
    'output_missing': '检查 Skill 是否正确生成了所有必需的输出文件'
  };

  return solutions[issue.type] || '参考 SKILL.md 和相关文档';
}

// ==================== 4. 执行审计 ====================

function auditExecution(skillName, toolResult) {
  const audit = {
    skill: skillName,
    timestamp: new Date().toISOString(),
    step_issues: [],
    output_issues: [],
    warnings: []
  };

  // 1. 检查执行步骤
  const expectedSteps = getExpectedSteps(skillName);
  const executedSteps = detectExecutedSteps(toolResult);

  for (const step of expectedSteps) {
    if (step.required) {
      const stepKeywords = step.title.toLowerCase();
      const executed = executedSteps.some(e => {
        const keyword = e.toLowerCase();
        return stepKeywords.includes(keyword) || keyword.includes(stepKeywords.split(/[：:]/)[0].trim().toLowerCase());
      });

      if (!executed) {
        audit.step_issues.push({
          type: 'missing_step',
          message: `缺少必需步骤: ${step.title}`,
          severity: 'high'
        });
      }
    }
  }

  // 2. 检查输出质量
  audit.output_issues = detectOutputQuality(skillName, toolResult);

  // 3. 生成警告
  audit.warnings = [...audit.step_issues, ...audit.output_issues];

  return audit;
}

// ==================== 5. 主流程 ====================

const audit = auditExecution(skillName, toolResult);

if (audit.warnings.length > 0) {
  console.log('\n[执行审计] ⚠️  发现问题:');

  audit.warnings.forEach((w, i) => {
    const icon = w.severity === 'high' ? '🔴' : '🟡';
    console.log(`  ${icon} [${i + 1}] ${w.message}`);
  });

  // 记录所有问题到 instincts.json
  const instincts = loadInstincts();
  audit.warnings.forEach(issue => {
    recordIssue(instincts, skillName, issue);
  });
  saveInstincts(instincts);

  console.log(`\n[执行审计] 问题已自动记录到: ${instinctsPath}`);
  console.log('[执行审计] 下次执行时会自动提醒这些问题\n');
} else {
  console.log('[执行审计] ✅ 执行完整，输出质量良好\n');
}

process.exit(0);
