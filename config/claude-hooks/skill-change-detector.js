#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const skillsPath = path.join(process.env.HOME, 'Desktop/小静的skills');
const globalConfigPath = path.join(process.env.HOME, '.claude/skills/_global_config');
const changeLogPath = path.join(globalConfigPath, 'skill-changes.json');

// 读取上次检查记录
let changeLog = {
  last_check: null,
  detected_changes: [],
  sync_suggestions: []
};

try {
  if (fs.existsSync(changeLogPath)) {
    changeLog = JSON.parse(fs.readFileSync(changeLogPath, 'utf-8'));
  }
} catch (e) {
  console.log('[Skill 变更检测] 初始化变更日志');
}

console.log('\n[Skill 变更检测] 正在检查 Skills 更新...');

try {
  // 检查 git 状态
  const gitStatus = execSync('git status --porcelain', {
    cwd: skillsPath,
    encoding: 'utf-8'
  }).trim();

  if (!gitStatus) {
    console.log('[Skill 变更检测] 未检测到变更');
    process.exit(0);
  }

  // 检测变更的 Skills
  const changedSkills = [];
  const lines = gitStatus.split('\n');

  for (const line of lines) {
    const match = line.match(/^\s*M\s+(.+?)\/SKILL\.md$/);
    if (match) {
      const skillName = match[1];
      changedSkills.push(skillName);
    }
  }

  if (changedSkills.length === 0) {
    console.log('[Skill 变更检测] 未检测到 SKILL.md 变更');
    process.exit(0);
  }

  console.log(`[Skill 变更检测] 检测到 ${changedSkills.length} 个 Skill 更新:`);
  changedSkills.forEach(skill => console.log(`  - ${skill}`));

  // 分析每个变更的 Skill
  const suggestions = [];

  for (const skillName of changedSkills) {
    try {
      // 获取 git diff
      const diff = execSync(`git diff ${skillName}/SKILL.md`, {
        cwd: skillsPath,
        encoding: 'utf-8'
      });

      // 提取版本号变化
      const versionMatch = diff.match(/^-version:\s*"(.+?)"\n\+version:\s*"(.+?)"/m);
      if (versionMatch) {
        const [, oldVersion, newVersion] = versionMatch;
        console.log(`  ${skillName}: v${oldVersion} → v${newVersion}`);

        // 分析变更类型
        const changeTypes = analyzeChanges(diff);

        suggestions.push({
          skill: skillName,
          old_version: oldVersion,
          new_version: newVersion,
          change_types: changeTypes,
          sync_needed: generateSyncSuggestions(skillName, changeTypes)
        });
      }
    } catch (e) {
      console.log(`  ${skillName}: 无法分析变更`);
    }
  }

  // 保存检测结果
  changeLog.last_check = new Date().toISOString();
  changeLog.detected_changes = suggestions;
  fs.writeFileSync(changeLogPath, JSON.stringify(changeLog, null, 2));

  // 输出同步建议
  if (suggestions.length > 0) {
    console.log('\n[Skill 变更检测] 同步建议:');
    suggestions.forEach(s => {
      console.log(`\n  ${s.skill} (v${s.old_version} → v${s.new_version}):`);
      s.sync_needed.forEach(suggestion => {
        console.log(`    - ${suggestion}`);
      });
    });
    console.log('\n  详细信息已保存到: ~/.claude/skills/_global_config/skill-changes.json');
  }

} catch (e) {
  if (e.message && e.message.includes('not a git repository')) {
    console.log('[Skill 变更检测] Skills 目录不是 git 仓库,跳过检测');
  } else {
    console.log('[Skill 变更检测] 检测失败:', e.message);
  }
}

// 分析变更类型
function analyzeChanges(diff) {
  const types = [];

  if (diff.includes('信任型') || diff.includes('trust')) {
    types.push('策略变更');
  }
  if (diff.match(/账号阶段|粉丝数|account.*stage/i)) {
    types.push('账号阶段标准变更');
  }
  if (diff.match(/标题|title/i)) {
    types.push('标题策略变更');
  }
  if (diff.match(/调性|tone|语气/i)) {
    types.push('调性变更');
  }
  if (diff.match(/新增|new.*feature/i)) {
    types.push('新增功能');
  }

  return types.length > 0 ? types : ['其他变更'];
}

// 生成同步建议
function generateSyncSuggestions(skillName, changeTypes) {
  const suggestions = [];

  if (changeTypes.includes('策略变更')) {
    suggestions.push('更新 分阶段调性配置.md');
    suggestions.push('更新 quality-standards.json');
  }

  if (changeTypes.includes('账号阶段标准变更')) {
    suggestions.push('统一 CLAUDE.md 中的账号阶段标准');
    suggestions.push('更新 quality-standards.json 的阶段适配标准');
  }

  if (changeTypes.includes('标题策略变更')) {
    suggestions.push('更新 quality-standards.json 的标题评估标准');
  }

  if (changeTypes.includes('调性变更')) {
    suggestions.push('检查 brand-tonality.md 是否需要更新');
    suggestions.push('检查其他内容生成 Skills 是否需要同步');
  }

  if (changeTypes.includes('新增功能')) {
    suggestions.push('更新 skill-rules.json 添加新功能的触发规则');
  }

  // 如果是内容生成类 Skill,建议同步到其他平台
  if (skillName.includes('content-generator')) {
    suggestions.push('检查其他平台的内容生成 Skills 是否需要同步更新');
  }

  return suggestions;
}
