#!/usr/bin/env node

/**
 * Quality Evaluator Hook for Claude Code
 *
 * 在 Skill 执行后自动评估内容质量
 * Hook 类型: ToolUseResult
 */

const fs = require('fs');
const path = require('path');

// 读取质量标准
const standardsPath = path.join(process.env.HOME, '.claude/skills/_global_config/quality-standards.json');
let qualityStandards = {};

try {
  qualityStandards = JSON.parse(fs.readFileSync(standardsPath, 'utf-8'));
} catch (e) {
  console.error('[质量评估] 无法读取 quality-standards.json');
  process.exit(0);
}

// 从环境变量获取工具调用信息
const toolName = process.env.TOOL_NAME || '';
const toolResult = process.env.TOOL_RESULT || '';

// 检查是否是内容生成 Skill
const contentSkills = [
  'xiaohongshu-content-generator',
  'wechat-content-generator',
  'video-script-generator'
];

const isContentSkill = contentSkills.some(skill => toolName.includes(skill));

if (!isContentSkill) {
  // 不是内容生成 Skill，跳过评估
  process.exit(0);
}

// 评估内容质量
function evaluateQuality(content, platform) {
  const standards = qualityStandards[platform] || {};
  const scores = {};
  let totalScore = 0;
  let totalWeight = 0;

  // 评估维度
  const dimensions = standards.dimensions || {};

  for (const [dimension, config] of Object.entries(dimensions)) {
    const weight = config.weight || 0;
    let score = 0;

    // 简化的评估逻辑（实际应该更复杂）
    switch (dimension) {
      case '结构完整性':
        score = evaluateStructure(content, config.criteria);
        break;
      case '信任型调性符合度':
        score = evaluateTrust(content, config.criteria);
        break;
      case '调性符合度':
        score = evaluateTone(content, config.criteria);
        break;
      case '合规性':
        score = evaluateCompliance(content, config.criteria);
        break;
      case '账号阶段适配':
        score = evaluateStageAdaptation(content, config.criteria);
        break;
      case '标签质量': // 新增
        const tagEval = evaluateTags(content);
        score = tagEval.score;
        if (tagEval.issues.length > 0) {
          scores['标签问题'] = tagEval.issues.join('; ');
        }
        break;
    }

    scores[dimension] = score;
    totalScore += score * weight;
    totalWeight += weight;
  }

  // 如果没有配置标签维度，也要检查标签
  if (!dimensions['标签质量']) {
    const tagEval = evaluateTags(content);
    scores['标签质量'] = tagEval.score;
    if (tagEval.issues.length > 0) {
      scores['标签问题'] = tagEval.issues.join('; ');
    }
    totalScore += tagEval.score * 0.2; // 给标签20%的权重
    totalWeight += 0.2;
  }

  const finalScore = totalWeight > 0 ? totalScore / totalWeight : 0;
  const threshold = standards.threshold || 75;
  const passed = finalScore >= threshold;

  return {
    finalScore: Math.round(finalScore),
    threshold,
    passed,
    scores,
    suggestions: generateSuggestions(scores, dimensions)
  };
}

// 评估结构完整性
function evaluateStructure(content, criteria) {
  let score = 100;

  // 检查必需元素
  if (criteria && criteria.required_elements) {
    for (const element of criteria.required_elements) {
      if (!content.includes(element)) {
        score -= 20;
      }
    }
  }

  return Math.max(0, score);
}

// 评估信任型调性
function evaluateTrust(content, criteria) {
  let score = 100;

  // 检查避免用词
  const avoidWords = ['必买', '绝了', '姐妹们冲', '太爱了', '一定要'];
  for (const word of avoidWords) {
    if (content.includes(word)) {
      score -= 15;
    }
  }

  // 检查推荐用词
  const recommendWords = ['客观来说', '根据我的经验', '建议大家', '比较推荐'];
  let hasRecommendWord = false;
  for (const word of recommendWords) {
    if (content.includes(word)) {
      hasRecommendWord = true;
      break;
    }
  }
  if (!hasRecommendWord) {
    score -= 10;
  }

  return Math.max(0, score);
}

// 评估调性符合度
function evaluateTone(content, criteria) {
  // 简化评估
  return 80;
}

// 评估合规性
function evaluateCompliance(content, criteria) {
  let score = 100;

  // 检查违禁词
  const bannedWords = ['最好', '第一', '顶级', '极致'];
  for (const word of bannedWords) {
    if (content.includes(word)) {
      score -= 20;
    }
  }

  return Math.max(0, score);
}

// 评估账号阶段适配
function evaluateStageAdaptation(content, criteria) {
  // 简化评估
  return 85;
}

// 评估标签质量（新增）
function evaluateTags(content) {
  let score = 100;
  const issues = [];

  // 提取标签
  const tagMatch = content.match(/#[\u4e00-\u9fa5a-zA-Z0-9]+/g);
  if (!tagMatch || tagMatch.length === 0) {
    return { score: 0, issues: ['未找到标签'] };
  }

  const tags = tagMatch.map(tag => tag.substring(1)); // 去掉 #
  const tagCount = tags.length;

  // 检查标签数量
  if (tagCount < 8) {
    score -= 20;
    issues.push(`标签数量不足（${tagCount}/10）`);
  } else if (tagCount > 12) {
    score -= 10;
    issues.push(`标签数量过多（${tagCount}/10）`);
  }

  // 检查是否有核心关键词和长尾关键词的组合
  const coreKeywords = ['养花', '绿植', '阳台', '种植', '植物', '花园', '园艺', '养护'];
  const hasCoreKeyword = tags.some(tag =>
    coreKeywords.some(keyword => tag.includes(keyword) && tag.length <= 4)
  );

  const hasLongTailKeyword = tags.some(tag => tag.length > 4);

  if (!hasCoreKeyword) {
    score -= 30;
    issues.push('缺少核心关键词（大标签）');
  }

  if (!hasLongTailKeyword) {
    score -= 30;
    issues.push('缺少长尾关键词（精准标签）');
  }

  // 检查是否全是长尾词或全是大标签
  const longTailCount = tags.filter(tag => tag.length > 4).length;
  const coreCount = tagCount - longTailCount;

  if (longTailCount > tagCount * 0.8) {
    score -= 20;
    issues.push('标签过于精准，缺少大流量标签');
  }

  if (coreCount > tagCount * 0.8) {
    score -= 20;
    issues.push('标签过于宽泛，缺少精准长尾词');
  }

  return { score: Math.max(0, score), issues };
}

// 生成改进建议
function generateSuggestions(scores, dimensions) {
  const suggestions = [];

  for (const [dimension, score] of Object.entries(scores)) {
    if (score < 70) {
      const config = dimensions[dimension];
      if (config && config.improvement_tips) {
        suggestions.push(`${dimension}: ${config.improvement_tips[0]}`);
      }
    }
  }

  return suggestions;
}

// 确定平台
function detectPlatform(toolName) {
  if (toolName.includes('xiaohongshu')) return '小红书';
  if (toolName.includes('wechat')) return '微信公众号';
  if (toolName.includes('video')) return '视频号';
  return '小红书'; // 默认
}

// 执行评估
const platform = detectPlatform(toolName);
const evaluation = evaluateQuality(toolResult, platform);

// 输出评估结果
console.log('\n[质量评估] 内容质量评分');
console.log(`平台: ${platform}`);
console.log(`总分: ${evaluation.finalScore}/${evaluation.threshold}`);
console.log(`状态: ${evaluation.passed ? '✅ 通过' : '❌ 未通过'}`);

if (Object.keys(evaluation.scores).length > 0) {
  console.log('\n各维度得分:');
  for (const [dimension, score] of Object.entries(evaluation.scores)) {
    console.log(`  ${dimension}: ${Math.round(score)}分`);
  }
}

if (evaluation.suggestions.length > 0) {
  console.log('\n改进建议:');
  for (const suggestion of evaluation.suggestions) {
    console.log(`  - ${suggestion}`);
  }
}

if (!evaluation.passed) {
  console.log('\n建议重新生成内容以达到质量标准。');
}

process.exit(0);
