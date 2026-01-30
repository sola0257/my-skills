#!/usr/bin/env node

/**
 * 通用规则一致性检查 Hook v3.0
 *
 * 设计理念：
 * - 不限定规则类型（配图、商品、知识提取等）
 * - 基于语义模式识别，而非硬编码关键词
 * - 支持规则注册系统（方案C）
 * - AI智能发现 + 人工确认（方案B）
 *
 * 适用范围：所有 Skills
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

// 规则注册表
let ruleRegistry = {
  registered_rules: [],      // 已确认需要一致的规则
  confirmed_syncs: [],        // 已确认的同步操作
  ignored_patterns: [],       // 已确认忽略的模式
  learned_patterns: []        // 从用户确认中学习的模式
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
  // 强制性规则
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

  // 建议性规则
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

  // 数量/格式规则
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

  // 格式规则
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

  // 流程规则
  process: {
    patterns: [
      /步骤\d+[：:][^。\n]{1,100}/g,
      /第[一二三四五六七八九十]\步[：:][^。\n]{1,100}/g,
      /执行流程[：:][^。\n]{1,200}/g
    ],
    weight: 0.8,
    category: 'process'
  },

  // 技术参数
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

          // 提取更大的上下文
          const contextStart = Math.max(0, index - 200);
          const contextEnd = Math.min(doc.content.length, index + ruleText.length + 200);
          const context = doc.content.substring(contextStart, contextEnd);

          // 提取所在章节标题
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

  // 从后往前找最近的标题
  for (let i = lines.length - 1; i >= 0; i--) {
    const line = lines[i].trim();
    if (line.match(/^#{1,6}\s+/)) {
      return line.replace(/^#{1,6}\s+/, '').trim();
    }
  }

  return 'Unknown Section';
}

// 计算文本相似度（简化版）
function calculateSimilarity(text1, text2) {
  // 移除标点和空格，转小写
  const normalize = (text) => text.toLowerCase()
    .replace(/[，。！？、；：""''（）【】《》\s]/g, '')
    .replace(/[,\.!\?;:"'\(\)\[\]<>\s]/g, '');

  const norm1 = normalize(text1);
  const norm2 = normalize(text2);

  // 计算最长公共子序列长度
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

    // 尝试加入现有组
    for (const group of groups) {
      const representative = group.segments[0];

      // 检查相似度
      const similarity = calculateSimilarity(seg1.ruleText, representative.ruleText);

      // 如果相似度高，且类别相同，加入该组
      if (similarity > 0.6 && seg1.category === representative.category) {
        group.segments.push(seg1);
        group.similarity_scores.push(similarity);
        foundGroup = true;
        break;
      }
    }

    // 如果没有找到合适的组，创建新组
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
    // 只有当规则出现在多个文档中时才可能有冲突
    if (group.segments.length < 2) continue;

    const documents = [...new Set(group.segments.map(s => s.document))];

    // 只有当跨越不同层级时才需要检查一致性
    const hasGlobal = documents.some(d => d.includes('CLAUDE.md'));
    const hasSkill = documents.some(d => d.includes('SKILL.md'));
    const hasKnowledge = documents.some(d => d.includes('knowledge/'));

    if ((hasGlobal && hasSkill) || (hasGlobal && hasKnowledge) || (hasSkill && hasKnowledge)) {
      // 计算平均相似度
      const avgSimilarity = group.similarity_scores.reduce((a, b) => a + b, 0) / group.similarity_scores.length;

      // 计算置信度
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

  // 按置信度排序
  conflicts.sort((a, b) => b.confidence - a.confidence);

  return conflicts;
}

// 计算冲突置信度
function calculateConflictConfidence(group, hasGlobal) {
  let confidence = 0.5;

  // 基于类别权重
  const categoryWeight = group.segments[0].weight;
  confidence += categoryWeight * 0.2;

  // 如果包含全局规则，提高置信度
  if (hasGlobal) confidence += 0.2;

  // 如果出现次数多，提高置信度
  if (group.segments.length >= 3) confidence += 0.1;
  if (group.segments.length >= 5) confidence += 0.1;

  // 如果在注册表中，大幅提高置信度
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
  console.log('🔍 通用规则冲突检测报告 v3.0');
  console.log('='.repeat(80));
  console.log(`\n检测到 ${conflicts.length} 个潜在规则冲突，需要人工确认：\n`);

  for (let i = 0; i < Math.min(conflicts.length, 20); i++) {
    const conflict = conflicts[i];
    console.log(`\n[${i + 1}] ${conflict.category} 规则`);
    console.log(`   代表性文本: ${conflict.representative_text.substring(0, 80)}...`);
    console.log(`   置信度: ${(conflict.confidence * 100).toFixed(0)}%`);
    console.log(`   平均相似度: ${(conflict.avg_similarity * 100).toFixed(0)}%`);
    console.log(`   出现位置 (${conflict.documents.length}个):`);

    for (const seg of conflict.segments.slice(0, 5)) {
      console.log(`     - ${seg.document}`);
      console.log(`       章节: ${seg.sectionTitle}`);
      console.log(`       内容: ${seg.ruleText.substring(0, 60)}...`);
    }

    if (conflict.segments.length > 5) {
      console.log(`     ... 还有 ${conflict.segments.length - 5} 个位置`);
    }

    if (conflict.suggestion.action === 'sync_from_global') {
      console.log(`   建议: 从 ${conflict.suggestion.source} 同步到 ${conflict.suggestion.targets.length} 个文档`);
    } else {
      console.log(`   建议: ${conflict.suggestion.message}`);
    }
  }

  if (conflicts.length > 20) {
    console.log(`\n... 还有 ${conflicts.length - 20} 个冲突，详见报告文件`);
  }

  console.log('\n' + '='.repeat(80));
  console.log('📝 下一步操作：');
  console.log('1. 查看完整报告: ' + REPORT_PATH);
  console.log('2. 确认需要同步的规则（编辑 rule-registry.json）');
  console.log('3. 运行同步命令: node rule-sync.js');
  console.log('='.repeat(80) + '\n');
}

// 主函数
function main() {
  console.log('\n[通用规则检查 v3.0] 开始扫描...\n');

  loadRegistry();

  // 1. 扫描文档
  console.log('[步骤1] 扫描所有文档...');
  const documents = scanDocuments();
  console.log(`  找到 ${documents.length} 个文档`);

  // 2. 提取规则片段
  console.log('[步骤2] 提取规则片段...');
  const segments = extractRuleSegments(documents);
  console.log(`  提取到 ${segments.length} 个规则片段`);

  // 3. 分组相似规则
  console.log('[步骤3] 分组相似规则...');
  const groups = groupSimilarRules(segments);
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
    version: '3.0',
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

  // 保存报告
  try {
    fs.mkdirSync(GLOBAL_CONFIG_PATH, { recursive: true});
    fs.writeFileSync(REPORT_PATH, JSON.stringify(report, null, 2));
    console.log(`\n[报告已保存] ${REPORT_PATH}`);
  } catch (e) {
    console.error('[保存报告失败]', e.message);
  }

  // 7. 生成人工确认报告
  if (filteredConflicts.length > 0) {
    generateConfirmationReport(filteredConflicts);
    process.exit(1);
  } else {
    console.log('\n✅ 未发现需要确认的规则冲突');
    process.exit(0);
  }
}

// 执行
main();
