#!/usr/bin/env node

/**
 * Skill 执行指导 Hook v1.0
 *
 * 目的：解决 AI 执行不稳定的问题
 * 原理：在 Skill 被调用时，强制提醒 AI 需要读取哪些文档
 *
 * Hook 类型: PostToolUse (Skill tool)
 */

const fs = require('fs');
const path = require('path');

// 从环境变量或标准输入获取 Skill 调用信息
let skillName = process.env.SKILL_NAME || '';

// 如果没有环境变量，尝试从命令行参数获取
if (!skillName && process.argv.length > 2) {
  skillName = process.argv[2];
}

// 如果还是没有，尝试从标准输入读取
if (!skillName) {
  let input = '';
  process.stdin.on('data', (chunk) => {
    input += chunk;
  });

  process.stdin.on('end', () => {
    // 尝试从输入中提取 Skill 名称
    const skillMatch = input.match(/skill["\s:]+([a-z-]+)/i);
    if (skillMatch) {
      skillName = skillMatch[1];
      processSkill(skillName);
    }
  });
} else {
  processSkill(skillName);
}

function processSkill(skillName) {
  if (!skillName) {
    process.exit(0);
  }

  const skillsPath = path.join(process.env.HOME, 'Desktop/小静的skills');
  const skillPath = path.join(skillsPath, skillName);
  const requiredReadingPath = path.join(skillPath, 'required-reading.json');

  // 检查是否有必读文档清单
  if (!fs.existsSync(requiredReadingPath)) {
    // 没有清单，不输出提醒
    process.exit(0);
  }

  try {
    const requiredReading = JSON.parse(fs.readFileSync(requiredReadingPath, 'utf-8'));

    if (!requiredReading.required_before_execution || requiredReading.required_before_execution.length === 0) {
      process.exit(0);
    }

    // 输出强制提醒
    console.log('\n' + '='.repeat(80));
    console.log(`⚠️  [执行提醒] 调用 ${skillName}`);
    console.log('='.repeat(80));
    console.log('\n执行前必须读取以下文档：\n');

    requiredReading.required_before_execution.forEach((doc, index) => {
      const fullPath = path.join(skillPath, doc.file);
      const exists = fs.existsSync(fullPath);
      const status = exists ? '✓' : '✗';

      console.log(`${index + 1}. ${status} ${doc.file}`);
      console.log(`   原因: ${doc.reason}`);
      console.log(`   路径: ${fullPath}`);
      console.log('');
    });

    console.log('⚠️  请在执行前完成阅读，确保遵循所有规范。');
    console.log('='.repeat(80) + '\n');

  } catch (e) {
    // 解析失败，静默退出
    process.exit(0);
  }
}
