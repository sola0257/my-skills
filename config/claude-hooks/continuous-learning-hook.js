#!/usr/bin/env node

/**
 * Continuous Learning Hook for Claude Code
 *
 * 在会话结束时收集学习数据
 * Hook 类型: SessionEnd
 */

const fs = require('fs');
const path = require('path');

// 配置路径
const instinctsPath = path.join(process.env.HOME, '.claude/skills/_global_config/instincts.json');
const skillRulesPath = path.join(process.env.HOME, '.claude/skills/_global_config/skill-rules.json');

// 读取现有数据
let instincts = {
  last_updated: null,
  learned_patterns: [],
  successful_cases: [],
  failed_cases: [],
  optimization_suggestions: []
};

try {
  if (fs.existsSync(instinctsPath)) {
    instincts = JSON.parse(fs.readFileSync(instinctsPath, 'utf-8'));
  }
} catch (e) {
  console.error('[持续学习] 无法读取 instincts.json');
}

// 从环境变量获取会话信息
const sessionData = process.env.SESSION_DATA || '{}';
let session = {};

try {
  session = JSON.parse(sessionData);
} catch (e) {
  // 无法解析会话数据
}

// 分析会话中的 Skill 使用情况
function analyzeSkillUsage(session) {
  const skillUsage = [];

  // 这里应该从会话数据中提取 Skill 调用信息
  // 简化实现：检查是否有特定的 Skill 调用模式

  return skillUsage;
}

// 提取成功模式
function extractSuccessPatterns(session) {
  const patterns = [];

  // 分析用户输入和 Skill 调用的关联
  // 识别高频成功模式

  return patterns;
}

// 提取失败案例
function extractFailureCases(session) {
  const failures = [];

  // 识别导致错误或不满意结果的模式

  return failures;
}

// 生成优化建议
function generateOptimizationSuggestions(patterns, failures) {
  const suggestions = [];

  // 基于成功模式和失败案例生成建议
  if (patterns.length > 0) {
    suggestions.push({
      type: 'trigger_rule',
      description: '发现新的高频使用模式，建议添加到 skill-rules.json',
      patterns: patterns
    });
  }

  if (failures.length > 0) {
    suggestions.push({
      type: 'error_handling',
      description: '发现常见错误模式，建议改进错误处理',
      failures: failures
    });
  }

  return suggestions;
}

// 更新学习数据
function updateLearningData() {
  const skillUsage = analyzeSkillUsage(session);
  const successPatterns = extractSuccessPatterns(session);
  const failureCases = extractFailureCases(session);
  const suggestions = generateOptimizationSuggestions(successPatterns, failureCases);

  // 更新 instincts
  instincts.last_updated = new Date().toISOString();

  // 添加新的学习数据
  if (successPatterns.length > 0) {
    instincts.learned_patterns.push(...successPatterns);
    // 保留最近100条
    instincts.learned_patterns = instincts.learned_patterns.slice(-100);
  }

  if (failureCases.length > 0) {
    instincts.failed_cases.push(...failureCases);
    instincts.failed_cases = instincts.failed_cases.slice(-50);
  }

  if (suggestions.length > 0) {
    instincts.optimization_suggestions.push(...suggestions);
    instincts.optimization_suggestions = instincts.optimization_suggestions.slice(-20);
  }

  // 保存更新后的数据
  try {
    fs.writeFileSync(instinctsPath, JSON.stringify(instincts, null, 2));

    if (suggestions.length > 0) {
      console.log('\n[持续学习] 发现优化建议:');
      for (const suggestion of suggestions) {
        console.log(`  - ${suggestion.description}`);
      }
      console.log(`\n详细信息已保存到: ${instinctsPath}`);
    }
  } catch (e) {
    console.error('[持续学习] 无法保存学习数据:', e.message);
  }
}

// 执行学习
updateLearningData();

process.exit(0);
