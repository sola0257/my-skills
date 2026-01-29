#!/usr/bin/env node

/**
 * 规则一致性检查 Hook
 *
 * 功能：自动检测跨文档的规则冲突
 * 触发：当 CLAUDE.md、SKILL.md 或 knowledge/*.md 被修改时
 * 输出：规则冲突报告和同步建议
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 路径配置
const HOME = process.env.HOME;
const CLAUDE_MD_PATH = path.join(HOME, '.claude/CLAUDE.md');
const SKILLS_PATH = path.join(HOME, 'Desktop/小静的skills');
const GLOBAL_CONFIG_PATH = path.join(HOME, '.claude/skills/_global_config');
const REPORT_PATH = path.join(GLOBAL_CONFIG_PATH, 'rule-consistency-report.json');

// 规则定义：需要跨文档一致的规则
const RULE_DEFINITIONS = {
  '配图风格规则': {
    keywords: ['混用风格', '统一风格', '同一选题', '可混用'],
    locations: [
      { file: 'CLAUDE.md', section: '规则2：全平台配图强制要求' },
      { file: 'xiaohongshu-content-generator/SKILL.md', section: '5. 信任型配图策略' },
      { file: 'xiaohongshu-content-generator/knowledge/image-prompt-guide.md', section: '核心原则' }
    ],
    expected_value: '可混用风格'
  },
  '小红书配图数量': {
    keywords: ['12-15张', '配图数量', '不得少于'],
    locations: [
      { file: 'CLAUDE.md', section: '小红书' },
      { file: 'xiaohongshu-content-generator/SKILL.md', section: '配图基本要求' }
    ],
    expected_value: '12-15张'
  },
  '小红书配图尺寸': {
    keywords: ['3:4', '1080×1440', '1080x1440'],
    locations: [
      { file: 'CLAUDE.md', section: '小红书' },
      { file: 'xiaohongshu-content-generator/SKILL.md', section: '配图基本要求' },
      { file: 'xiaohongshu-content-generator/knowledge/image-prompt-guide.md', section: '技术参数' }
    ],
    expected_value: '3:4竖版（1080×1440）'
  }
};

// 读取文件内容
function readFile(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      return fs.readFileSync(filePath, 'utf-8');
    }
  } catch (e) {
    console.error(`[规则检查] 读取文件失败: ${filePath}`);
  }
  return null;
}

// 检查规则是否存在于文本中
function checkRuleInText(text, rule) {
  if (!text) return { found: false, context: null };

  const keywords = rule.keywords;
  let foundKeywords = [];
  let context = '';

  // 查找关键词
  for (const keyword of keywords) {
    if (text.includes(keyword)) {
      foundKeywords.push(keyword);

      // 提取上下文（关键词前后50个字符）
      const index = text.indexOf(keyword);
      const start = Math.max(0, index - 50);
      const end = Math.min(text.length, index + keyword.length + 50);
      context = text.substring(start, end).replace(/\n/g, ' ');
    }
  }

  return {
    found: foundKeywords.length > 0,
    keywords: foundKeywords,
    context: context
  };
}

// 检查单个规则的一致性
function checkRuleConsistency(ruleName, ruleConfig) {
  const results = [];

  for (const location of ruleConfig.locations) {
    let filePath;

    if (location.file === 'CLAUDE.md') {
      filePath = CLAUDE_MD_PATH;
    } else {
      filePath = path.join(SKILLS_PATH, location.file);
    }

    const content = readFile(filePath);
    const check = checkRuleInText(content, ruleConfig);

    results.push({
      file: location.file,
      section: location.section,
      found: check.found,
      keywords: check.keywords || [],
      context: check.context
    });
  }

  return results;
}

// 分析规则一致性
function analyzeConsistency(results, expectedValue) {
  const foundFiles = results.filter(r => r.found);
  const notFoundFiles = results.filter(r => !r.found);

  if (notFoundFiles.length === 0) {
    return {
      status: 'consistent',
      message: '所有文档规则一致'
    };
  }

  if (foundFiles.length === 0) {
    return {
      status: 'missing',
      message: '所有文档都缺少此规则'
    };
  }

  return {
    status: 'inconsistent',
    message: `规则不一致：${foundFiles.length}个文档有规则，${notFoundFiles.length}个文档缺少规则`,
    foundFiles: foundFiles.map(f => f.file),
    notFoundFiles: notFoundFiles.map(f => f.file)
  };
}

// 生成同步建议
function generateSyncSuggestions(inconsistencies) {
  const suggestions = [];

  for (const [ruleName, data] of Object.entries(inconsistencies)) {
    if (data.analysis.status === 'inconsistent') {
      suggestions.push({
        rule: ruleName,
        action: 'sync_required',
        source: data.analysis.foundFiles[0], // 使用第一个有规则的文件作为源
        targets: data.analysis.notFoundFiles,
        expected_value: data.expected_value,
        priority: 'high'
      });
    }
  }

  return suggestions;
}

// 主函数
function main() {
  console.log('\n[规则一致性检查] 开始检查...\n');

  const report = {
    timestamp: new Date().toISOString(),
    rules_checked: Object.keys(RULE_DEFINITIONS).length,
    inconsistencies: {},
    suggestions: []
  };

  // 检查每个规则
  for (const [ruleName, ruleConfig] of Object.entries(RULE_DEFINITIONS)) {
    console.log(`[规则检查] ${ruleName}...`);

    const results = checkRuleConsistency(ruleName, ruleConfig);
    const analysis = analyzeConsistency(results, ruleConfig.expected_value);

    if (analysis.status !== 'consistent') {
      report.inconsistencies[ruleName] = {
        expected_value: ruleConfig.expected_value,
        results: results,
        analysis: analysis
      };

      console.log(`  ⚠️  ${analysis.message}`);
      if (analysis.notFoundFiles) {
        console.log(`  缺少规则的文档: ${analysis.notFoundFiles.join(', ')}`);
      }
    } else {
      console.log(`  ✅ ${analysis.message}`);
    }
  }

  // 生成同步建议
  if (Object.keys(report.inconsistencies).length > 0) {
    report.suggestions = generateSyncSuggestions(report.inconsistencies);

    console.log('\n[同步建议]');
    for (const suggestion of report.suggestions) {
      console.log(`\n规则: ${suggestion.rule}`);
      console.log(`  源文档: ${suggestion.source}`);
      console.log(`  需要同步到: ${suggestion.targets.join(', ')}`);
      console.log(`  期望值: ${suggestion.expected_value}`);
    }
  } else {
    console.log('\n✅ 所有规则一致，无需同步');
  }

  // 保存报告
  try {
    fs.mkdirSync(GLOBAL_CONFIG_PATH, { recursive: true });
    fs.writeFileSync(REPORT_PATH, JSON.stringify(report, null, 2));
    console.log(`\n[报告已保存] ${REPORT_PATH}`);
  } catch (e) {
    console.error('[保存报告失败]', e.message);
  }

  // 如果有不一致，返回非零退出码
  if (Object.keys(report.inconsistencies).length > 0) {
    console.log('\n⚠️  检测到规则不一致，建议同步更新');
    process.exit(1);
  }

  process.exit(0);
}

// 执行
main();
