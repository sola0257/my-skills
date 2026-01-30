#!/usr/bin/env node

/**
 * 智能规则一致性检查 Hook v4.0
 *
 * 新特性：
 * - 条件执行：只在修改规则文件时才运行检查
 * - 自动触发：配置为 PostToolUse Hook，自动检测文件修改
 * - 快速跳过：非规则文件修改时几乎不耗时
 *
 * 触发条件：
 * - 修改了 CLAUDE.md
 * - 修改了任何 SKILL.md
 * - 修改了 knowledge/ 目录下的 .md 文件
 *
 * Hook 类型: PostToolUse
 */

const fs = require('fs');
const path = require('path');

// 路径配置
const HOME = process.env.HOME;
const CLAUDE_MD_PATH = path.join(HOME, '.claude/CLAUDE.md');
const SKILLS_PATH = path.join(HOME, 'Desktop/小静的skills');
const GLOBAL_CONFIG_PATH = path.join(HOME, '.claude/skills/_global_config');
const REPORT_PATH = path.join(GLOBAL_CONFIG_PATH, 'rule-consistency-report-v3.json');
const REGISTRY_PATH = path.join(GLOBAL_CONFIG_PATH, 'rule-registry.json');

// ============================================================================
// 条件检查：是否需要运行规则检查
// ============================================================================

function shouldRunCheck() {
  // 从环境变量获取修改的文件路径
  const modifiedFile = process.env.MODIFIED_FILE || '';

  // 如果没有文件信息，从标准输入读取
  if (!modifiedFile) {
    // 尝试从命令行参数获取
    const args = process.argv.slice(2);
    if (args.length > 0) {
      const file = args[0];
      return isRuleFile(file);
    }

    // 如果都没有，默认运行检查（手动调用的情况）
    return true;
  }

  return isRuleFile(modifiedFile);
}

function isRuleFile(filePath) {
  // 检查是否是规则文件
  const normalizedPath = filePath.toLowerCase();

  // CLAUDE.md
  if (normalizedPath.includes('claude.md')) {
    return true;
  }

  // SKILL.md
  if (normalizedPath.includes('skill.md')) {
    return true;
  }

  // knowledge/ 目录下的 .md 文件
  if (normalizedPath.includes('knowledge/') && normalizedPath.endsWith('.md')) {
    return true;
  }

  return false;
}

// ============================================================================
// 快速退出检查
// ============================================================================

if (!shouldRunCheck()) {
  // 非规则文件修改，快速退出
  process.exit(0);
}

console.log('\n[规则检查] 检测到规则文件修改，开始检查规则一致性...\n');

// ============================================================================
// 以下是原有的规则检查逻辑
// ============================================================================

// 规则注册表
let ruleRegistry = {
  registered_rules: [],
  confirmed_syncs: [],
  ignored_patterns: [],
  learned_patterns: []
};

// 加载注册表
function loadRegistry() {
  try {
    if (fs.existsSync(REGISTRY_PATH)) {
      ruleRegistry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf-8'));
    }
  } catch (e) {
    console.log('[规则注册表] 初始化新注册表');
  }
}

// 保存注册表
function saveRegistry() {
  try {
    fs.mkdirSync(GLOBAL_CONFIG_PATH, { recursive: true });
    fs.writeFileSync(REGISTRY_PATH, JSON.stringify(ruleRegistry, null, 2));
  } catch (e) {
    console.error('[保存注册表失败]', e.message);
  }
}

// 扫描所有文档
function scanDocuments() {
  const documents = [];

  // 1. CLAUDE.md (全局规则)
  if (fs.existsSync(CLAUDE_MD_PATH)) {
    documents.push({
      path: CLAUDE_MD_PATH,
      relativePath: '.claude/CLAUDE.md',
      type: 'global',
      content: fs.readFileSync(CLAUDE_MD_PATH, 'utf-8')
    });
  }

  // 2. 所有 Skills
  const skillDirs = fs.readdirSync(SKILLS_PATH, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('.') && !d.name.startsWith('_'))
    .map(d => d.name);

  for (const skillName of skillDirs) {
    const skillPath = path.join(SKILLS_PATH, skillName);

    // SKILL.md
    const skillMdPath = path.join(skillPath, 'SKILL.md');
    if (fs.existsSync(skillMdPath)) {
      documents.push({
        path: skillMdPath,
        relativePath: `${skillName}/SKILL.md`,
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
          relativePath: `${skillName}/knowledge/${file}`,
          type: 'knowledge',
          skill: skillName,
          content: fs.readFileSync(filePath, 'utf-8')
        });
      }
    }
  }

  return documents;
}

// 通用规则识别模式
const RULE_PATTERNS = {
  mandatory: {
    patterns: [
      /必须[^。\n]{1,100}/g,
      /禁止[^。\n]{1,100}/g,
      /不得[^。\n]{1,100}/g,
      /强制[^。\n]{1,100}/g,
      /MUST[^。\n]{1,100}/gi,
      /NEVER[^。\n]{1,100}/gi
    ],
    weight: 1.0,
    category: 'mandatory'
  },
  recommended: {
    patterns: [
      /应该[^。\n]{1,100}/g,
      /建议[^。\n]{1,100}/g,
      /推荐[^。\n]{1,100}/g,
      /最好[^。\n]{1,100}/g,
      /SHOULD[^。\n]{1,100}/gi,
      /RECOMMENDED[^。\n]{1,100}/gi
    ],
    weight: 0.7,
    category: 'recommended'
  },
  quantitative: {
    patterns: [
      /\d+[-~]\d+[张个件条篇]/g,
      /不[得少]于\d+/g,
      /至[少多]\d+/g,
      /\d+[x×]\d+/g,
      /\d+:\d+/g
    ],
    weight: 0.9,
    category: 'quantitative'
  },
  format: {
    patterns: [
      /格式[：:][^。\n]{1,100}/g,
      /命名[：:][^。\n]{1,100}/g,
      /尺寸[：:][^。\n]{1,100}/g,
      /比例[：:][^。\n]{1,100}/g
    ],
    weight: 0.8,
    category: 'format'
  },
  process: {
    patterns: [
      /步骤\d+[：:][^。\n]{1,100}/g,
      /第[一二三四五六七八九十]\步[：:][^。\n]{1,100}/g,
      /执行流程[：:][^。\n]{1,200}/g
    ],
    weight: 0.8,
    category: 'process'
  },
  technical: {
    patterns: [
      /API[：:][^。\n]{1,100}/gi,
      /端点[：:][^。\n]{1,100}/g,
      /模型[：:][^。\n]{1,100}/g,
      /参数[：:][^。\n]{1,100}/g
    ],
    weight: 0.9,
    category: 'technical'
  }
};

// 提取规则片段
function extractRuleSegments(documents) {
  const segments = [];

  for (const doc of documents) {
    for (const [patternType, config] of Object.entries(RULE_PATTERNS)) {
      for (const pattern of config.patterns) {
        const matches = [...doc.content.matchAll(pattern)];

        for (const match of matches) {
          const ruleText = match[0];
          const index = match.index;

          const contextStart = Math.max(0, index - 200);
          const contextEnd = Math.min(doc.content.length, index + ruleText.length + 200);
          const context = doc.content.substring(contextStart, contextEnd);

          const sectionTitle = extractSectionTitle(doc.content, index);

          segments.push({
            document: doc.relativePath,
            skill: doc.skill || 'global',
            type: doc.type,
            ruleText: ruleText.trim(),
            category: config.category,
            weight: config.weight,
            context: context.replace(/\n/g, ' ').trim(),
            sectionTitle: sectionTitle,
            patternType: patternType
          });
        }
      }
    }
  }

  return segments;
}

// 提取章节标题
function extractSectionTitle(content, position) {
  const beforeText = content.substring(0, position);
  const lines = beforeText.split('\n');

  for (let i = lines.length - 1; i >= 0; i--) {
    const line = lines[i].trim();
    if (line.match(/^#{1,6}\s+/)) {
      return line.replace(/^#{1,6}\s+/, '').trim();
    }
  }

  return 'Unknown Section';
}

// 计算文本相似度
function calculateSimilarity(text1, text2) {
  const normalize = (text) => text.toLowerCase()
    .replace(/[，。！？、；："\"''（）【】《》\s]/g, '')
    .replace(/[,\.!\?;:\"'\(\)\[\]<>\s]/g, '');

  const norm1 = normalize(text1);
  const norm2 = normalize(text2);

  const lcs = longestCommonSubsequence(norm1, norm2);
  const maxLen = Math.max(norm1.length, norm2.length);

  return maxLen > 0 ? lcs / maxLen : 0;
}

// 最长公共子序列
function longestCommonSubsequence(str1, str2) {
  const m = str1.length;
  const n = str2.length;
  const dp = Array(m + 1).fill(0).map(() => Array(n + 1).fill(0));

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (str1[i - 1] === str2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  return dp[m][n];
}

// 分组相似规则
function groupSimilarRules(segments) {
  const groups = [];

  for (let i = 0; i < segments.length; i++) {
    const seg1 = segments[i];
    let foundGroup = false;

    for (const group of groups) {
      const representative = group.segments[0];
      const similarity = calculateSimilarity(seg1.ruleText, representative.ruleText);

      if (similarity > 0.6 && seg1.category === representative.category) {
        group.segments.push(seg1);
        group.similarity_scores.push(similarity);
        foundGroup = true;
        break;
      }
    }

    if (!foundGroup) {
      groups.push({
        id: groups.length + 1,
        category: seg1.category,
        representative_text: seg1.ruleText,
        segments: [seg1],
        similarity_scores: [1.0]
      });
    }
  }

  return groups;
}

// 识别潜在冲突
function identifyConflicts(groups) {
  const conflicts = [];

  for (const group of groups) {
    if (group.segments.length < 2) continue;

    const documents = [...new Set(group.segments.map(s => s.document))];

    const hasGlobal = documents.some(d => d.includes('CLAUDE.md'));
    const hasSkill = documents.some(d => d.includes('SKILL.md'));
    const hasKnowledge = documents.some(d => d.includes('knowledge/'));

    if ((hasGlobal && hasSkill) || (hasGlobal && hasKnowledge) || (hasSkill && hasKnowledge)) {
      const avgSimilarity = group.similarity_scores.reduce((a, b) => a + b, 0) / group.similarity_scores.length;
      const confidence = calculateConflictConfidence(group, hasGlobal);

      conflicts.push({
        id: group.id,
        category: group.category,
        representative_text: group.representative_text,
        documents: documents,
        segments: group.segments,
        avg_similarity: avgSimilarity,
        confidence: confidence,
        suggestion: generateSyncSuggestion(group, hasGlobal)
      });
    }
  }

  conflicts.sort((a, b) => b.confidence - a.confidence);

  return conflicts;
}

// 计算冲突置信度
function calculateConflictConfidence(group, hasGlobal) {
  let confidence = 0.5;

  const categoryWeight = group.segments[0].weight;
  confidence += categoryWeight * 0.2;

  if (hasGlobal) confidence += 0.2;

  if (group.segments.length >= 3) confidence += 0.1;
  if (group.segments.length >= 5) confidence += 0.1;

  const isRegistered = ruleRegistry.registered_rules.some(r =>
    r.representative_text === group.representative_text
  );
  if (isRegistered) confidence += 0.3;

  return Math.min(confidence, 1.0);
}

// 生成同步建议
function generateSyncSuggestion(group, hasGlobal) {
  if (hasGlobal) {
    const globalSegment = group.segments.find(s => s.document.includes('CLAUDE.md'));
    return {
      action: 'sync_from_global',
      source: 'CLAUDE.md',
      source_text: globalSegment.ruleText,
      targets: group.segments
        .filter(s => !s.document.includes('CLAUDE.md'))
        .map(s => ({ document: s.document, current_text: s.ruleText }))
    };
  } else {
    return {
      action: 'needs_review',
      message: '需要人工判断哪个文档作为同步源',
      options: group.segments.map(s => ({
        document: s.document,
        text: s.ruleText
      }))
    };
  }
}

// 过滤已忽略的模式
function filterIgnoredPatterns(conflicts) {
  return conflicts.filter(conflict => {
    return !ruleRegistry.ignored_patterns.some(pattern =>
      pattern.representative_text === conflict.representative_text
    );
  });
}

// 生成人工确认报告
function generateConfirmationReport(conflicts) {
  console.log('\n' + '='.repeat(80));
  console.log('🔍 规则冲突检测报告');
  console.log('='.repeat(80));
  console.log(`\n检测到 ${conflicts.length} 个潜在规则冲突：\n`);

  for (let i = 0; i < Math.min(conflicts.length, 10); i++) {
    const conflict = conflicts[i];
    console.log(`\n[${i + 1}] ${conflict.category} 规则`);
    console.log(`   代表性文本: ${conflict.representative_text.substring(0, 80)}...`);
    console.log(`   置信度: ${(conflict.confidence * 100).toFixed(0)}%`);
    console.log(`   出现位置 (${conflict.documents.length}个):`);

    for (const seg of conflict.segments.slice(0, 3)) {
      console.log(`     - ${seg.document}`);
    }

    if (conflict.segments.length > 3) {
      console.log(`     ... 还有 ${conflict.segments.length - 3} 个位置`);
    }
  }

  if (conflicts.length > 10) {
    console.log(`\n... 还有 ${conflicts.length - 10} 个冲突，详见报告文件`);
  }

  console.log('\n' + '='.repeat(80));
  console.log('📝 完整报告: ' + REPORT_PATH);
  console.log('='.repeat(80) + '\n');
}

// 主函数
function main() {
  loadRegistry();

  console.log('[步骤1] 扫描所有文档...');
  const documents = scanDocuments();
  console.log(`  找到 ${documents.length} 个文档`);

  console.log('[步骤2] 提取规则片段...');
  const segments = extractRuleSegments(documents);
  console.log(`  提取到 ${segments.length} 个规则片段`);

  console.log('[步骤3] 分组相似规则...');
  const groups = groupSimilarRules(segments);
  console.log(`  分组为 ${groups.length} 个规则组`);

  console.log('[步骤4] 识别潜在冲突...');
  const conflicts = identifyConflicts(groups);
  console.log(`  发现 ${conflicts.length} 个潜在冲突`);

  const filteredConflicts = filterIgnoredPatterns(conflicts);
  console.log(`  过滤后剩余 ${filteredConflicts.length} 个需要确认的冲突`);

  const report = {
    timestamp: new Date().toISOString(),
    version: '4.0',
    scan_summary: {
      documents_scanned: documents.length,
      segments_extracted: segments.length,
      rule_groups: groups.length,
      conflicts_detected: conflicts.length,
      conflicts_after_filter: filteredConflicts.length
    },
    conflicts: filteredConflicts,
    registry_stats: {
      registered_rules: ruleRegistry.registered_rules.length,
      confirmed_syncs: ruleRegistry.confirmed_syncs.length,
      ignored_patterns: ruleRegistry.ignored_patterns.length
    }
  };

  try {
    fs.mkdirSync(GLOBAL_CONFIG_PATH, { recursive: true});
    fs.writeFileSync(REPORT_PATH, JSON.stringify(report, null, 2));
    console.log(`\n[报告已保存] ${REPORT_PATH}`);
  } catch (e) {
    console.error('[保存报告失败]', e.message);
  }

  if (filteredConflicts.length > 0) {
    generateConfirmationReport(filteredConflicts);
    // 不返回错误码，因为发现冲突是正常的检查结果，不是错误
    process.exit(0);
  } else {
    console.log('\n✅ 未发现需要确认的规则冲突\n');
    process.exit(0);
  }
}

// 执行
main();
