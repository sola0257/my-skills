#!/usr/bin/env node

/**
 * 智能规则一致性检查 Hook v2.0
 *
 * 功能：
 * 1. AI 智能发现潜在规则冲突（方案B）
 * 2. 支持规则注册系统（方案C）
 * 3. 人工确认后批量同步
 *
 * 工作流：
 * AI扫描 → 识别冲突 → 生成报告 → 人工确认 → 批量同步
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
const REGISTRY_PATH = path.join(GLOBAL_CONFIG_PATH, 'rule-registry.json');

// 已注册的规则（方案C：减少误判）
let ruleRegistry = {
  registered_rules: [],
  confirmed_conflicts: [],
  ignored_patterns: []
};

// 加载规则注册表
function loadRegistry() {
  try {
    if (fs.existsSync(REGISTRY_PATH)) {
      ruleRegistry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf-8'));
    }
  } catch (e) {
    console.log('[规则注册表] 初始化新注册表');
  }
}

// 保存规则注册表
function saveRegistry() {
  try {
    fs.mkdirSync(GLOBAL_CONFIG_PATH, { recursive: true });
    fs.writeFileSync(REGISTRY_PATH, JSON.stringify(ruleRegistry, null, 2));
  } catch (e) {
    console.error('[保存注册表失败]', e.message);
  }
}

// 扫描所有相关文档
function scanDocuments() {
  const documents = [];

  // 1. 扫描 CLAUDE.md
  if (fs.existsSync(CLAUDE_MD_PATH)) {
    documents.push({
      path: CLAUDE_MD_PATH,
      type: 'global',
      content: fs.readFileSync(CLAUDE_MD_PATH, 'utf-8')
    });
  }

  // 2. 扫描所有 Skills
  const skillDirs = fs.readdirSync(SKILLS_PATH, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('.'))
    .map(d => d.name);

  for (const skillName of skillDirs) {
    const skillPath = path.join(SKILLS_PATH, skillName);

    // SKILL.md
    const skillMdPath = path.join(skillPath, 'SKILL.md');
    if (fs.existsSync(skillMdPath)) {
      documents.push({
        path: skillMdPath,
        type: 'skill',
        skill: skillName,
        content: fs.readFileSync(skillMdPath, 'utf-8')
      });
    }

    // knowledge/*.md
    const knowledgePath = path.join(skillPath, 'knowledge');
    if (fs.existsSync(knowledgePath)) {
      const knowledgeFiles = fs.readdirSync(knowledgePath)
        .filter(f => f.endsWith('.md'));

      for (const file of knowledgeFiles) {
        const filePath = path.join(knowledgePath, file);
        documents.push({
          path: filePath,
          type: 'knowledge',
          skill: skillName,
          content: fs.readFileSync(filePath, 'utf-8')
        });
      }
    }
  }

  return documents;
}

// 提取规则模式（AI智能识别）
function extractRulePatterns(documents) {
  const patterns = [];

  // 规则识别模式
  const ruleIndicators = [
    // 数量规则
    { pattern: /(\d+[-~]\d+)张/g, type: '数量规则', category: 'image_count' },
    { pattern: /不得少于(\d+)张/g, type: '数量规则', category: 'image_count' },

    // 尺寸规则
    { pattern: /(\d+[x×]\d+)/g, type: '尺寸规则', category: 'image_size' },
    { pattern: /(\d+:\d+)竖版/g, type: '尺寸规则', category: 'image_size' },

    // 风格规则
    { pattern: /(可混用风格|统一风格|同一选题.*风格)/g, type: '风格规则', category: 'style' },
    { pattern: /(dreamy-photo|cozy-sketch|infographic-sketch)/g, type: '风格规则', category: 'style' },

    // 命名规则
    { pattern: /序号[_].*\.png/g, type: '命名规则', category: 'naming' },

    // 色彩规则
    { pattern: /(Morandi|低饱和度|高饱和度)/g, type: '色彩规则', category: 'color' },
    { pattern: /(dusty coral|muted rose|sage green)/g, type: '色彩规则', category: 'color' }
  ];

  for (const doc of documents) {
    for (const indicator of ruleIndicators) {
      const matches = [...doc.content.matchAll(indicator.pattern)];

      for (const match of matches) {
        // 提取上下文
        const index = match.index;
        const start = Math.max(0, index - 100);
        const end = Math.min(doc.content.length, index + match[0].length + 100);
        const context = doc.content.substring(start, end).replace(/\n/g, ' ');

        patterns.push({
          document: path.relative(HOME, doc.path),
          type: indicator.type,
          category: indicator.category,
          value: match[0],
          context: context,
          skill: doc.skill || 'global'
        });
      }
    }
  }

  return patterns;
}

// 分组相似规则
function groupSimilarRules(patterns) {
  const groups = {};

  for (const pattern of patterns) {
    const key = `${pattern.category}_${pattern.value}`;

    if (!groups[key]) {
      groups[key] = {
        category: pattern.category,
        type: pattern.type,
        value: pattern.value,
        occurrences: []
      };
    }

    groups[key].occurrences.push({
      document: pattern.document,
      skill: pattern.skill,
      context: pattern.context
    });
  }

  return Object.values(groups);
}

// 识别潜在冲突
function identifyConflicts(groups) {
  const conflicts = [];

  for (const group of groups) {
    // 如果同一规则出现在多个文档中
    if (group.occurrences.length > 1) {
      // 检查是否跨越不同层级（global, skill, knowledge）
      const documents = group.occurrences.map(o => o.document);
      const hasGlobal = documents.some(d => d.includes('CLAUDE.md'));
      const hasSkill = documents.some(d => d.includes('SKILL.md'));
      const hasKnowledge = documents.some(d => d.includes('knowledge/'));

      // 如果跨越多个层级，可能需要一致性
      if ((hasGlobal && hasSkill) || (hasGlobal && hasKnowledge) || (hasSkill && hasKnowledge)) {
        conflicts.push({
          rule_type: group.type,
          category: group.category,
          value: group.value,
          documents: documents,
          occurrences: group.occurrences,
          confidence: calculateConfidence(group),
          suggestion: generateSuggestion(group)
        });
      }
    }
  }

  return conflicts;
}

// 计算置信度
function calculateConfidence(group) {
  let confidence = 0.5; // 基础置信度

  // 如果在已注册规则中，提高置信度
  const isRegistered = ruleRegistry.registered_rules.some(r =>
    r.category === group.category && r.value === group.value
  );
  if (isRegistered) confidence += 0.3;

  // 如果出现在多个文档中，提高置信度
  if (group.occurrences.length >= 3) confidence += 0.2;

  // 如果包含 CLAUDE.md，提高置信度
  const hasGlobal = group.occurrences.some(o => o.document.includes('CLAUDE.md'));
  if (hasGlobal) confidence += 0.2;

  return Math.min(confidence, 1.0);
}

// 生成同步建议
function generateSuggestion(group) {
  const hasGlobal = group.occurrences.some(o => o.document.includes('CLAUDE.md'));

  if (hasGlobal) {
    return {
      action: 'sync_from_global',
      source: 'CLAUDE.md',
      targets: group.occurrences
        .filter(o => !o.document.includes('CLAUDE.md'))
        .map(o => o.document)
    };
  } else {
    return {
      action: 'needs_review',
      message: '需要人工判断哪个文档作为源'
    };
  }
}

// 过滤已忽略的模式
function filterIgnoredPatterns(conflicts) {
  return conflicts.filter(conflict => {
    return !ruleRegistry.ignored_patterns.some(pattern =>
      pattern.category === conflict.category && pattern.value === conflict.value
    );
  });
}

// 生成人工确认报告
function generateConfirmationReport(conflicts) {
  console.log('\n' + '='.repeat(80));
  console.log('🔍 智能规则冲突检测报告');
  console.log('='.repeat(80));
  console.log(`\n检测到 ${conflicts.length} 个潜在规则冲突，需要人工确认：\n`);

  for (let i = 0; i < conflicts.length; i++) {
    const conflict = conflicts[i];
    console.log(`\n[${i + 1}] ${conflict.rule_type} - ${conflict.value}`);
    console.log(`   类别: ${conflict.category}`);
    console.log(`   置信度: ${(conflict.confidence * 100).toFixed(0)}%`);
    console.log(`   出现位置 (${conflict.documents.length}个):`);

    for (const occ of conflict.occurrences) {
      console.log(`     - ${occ.document}`);
      console.log(`       ${occ.context.substring(0, 80)}...`);
    }

    if (conflict.suggestion.action === 'sync_from_global') {
      console.log(`   建议: 从 ${conflict.suggestion.source} 同步到其他文档`);
    } else {
      console.log(`   建议: ${conflict.suggestion.message}`);
    }
  }

  console.log('\n' + '='.repeat(80));
  console.log('📝 下一步操作：');
  console.log('1. 查看报告文件: ' + REPORT_PATH);
  console.log('2. 确认需要同步的规则');
  console.log('3. 运行同步命令（待实现）');
  console.log('='.repeat(80) + '\n');
}

// 主函数
function main() {
  console.log('\n[智能规则检查 v2.0] 开始扫描...\n');

  // 加载规则注册表
  loadRegistry();

  // 1. 扫描所有文档
  console.log('[步骤1] 扫描文档...');
  const documents = scanDocuments();
  console.log(`  找到 ${documents.length} 个文档`);

  // 2. 提取规则模式
  console.log('[步骤2] 提取规则模式...');
  const patterns = extractRulePatterns(documents);
  console.log(`  识别到 ${patterns.length} 个规则模式`);

  // 3. 分组相似规则
  console.log('[步骤3] 分组相似规则...');
  const groups = groupSimilarRules(patterns);
  console.log(`  分组为 ${groups.length} 个规则组`);

  // 4. 识别潜在冲突
  console.log('[步骤4] 识别潜在冲突...');
  const conflicts = identifyConflicts(groups);
  console.log(`  发现 ${conflicts.length} 个潜在冲突`);

  // 5. 过滤已忽略的模式
  const filteredConflicts = filterIgnoredPatterns(conflicts);
  console.log(`  过滤后剩余 ${filteredConflicts.length} 个需要确认的冲突`);

  // 6. 生成报告
  const report = {
    timestamp: new Date().toISOString(),
    version: '2.0',
    scan_summary: {
      documents_scanned: documents.length,
      patterns_found: patterns.length,
      rule_groups: groups.length,
      conflicts_detected: conflicts.length,
      conflicts_after_filter: filteredConflicts.length
    },
    conflicts: filteredConflicts,
    registry_stats: {
      registered_rules: ruleRegistry.registered_rules.length,
      confirmed_conflicts: ruleRegistry.confirmed_conflicts.length,
      ignored_patterns: ruleRegistry.ignored_patterns.length
    }
  };

  // 保存报告
  try {
    fs.mkdirSync(GLOBAL_CONFIG_PATH, { recursive: true });
    fs.writeFileSync(REPORT_PATH, JSON.stringify(report, null, 2));
    console.log(`\n[报告已保存] ${REPORT_PATH}`);
  } catch (e) {
    console.error('[保存报告失败]', e.message);
  }

  // 7. 生成人工确认报告
  if (filteredConflicts.length > 0) {
    generateConfirmationReport(filteredConflicts);
    process.exit(1); // 有冲突需要确认
  } else {
    console.log('\n✅ 未发现需要确认的规则冲突');
    process.exit(0);
  }
}

// 执行
main();
