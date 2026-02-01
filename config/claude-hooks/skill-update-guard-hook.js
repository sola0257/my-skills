#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 检测关键词
const UPDATE_KEYWORDS = [
  '更新 SKILL.md',
  '修改 SKILL.md',
  '优化 Skill',
  '更新 skill',
  '添加到 SKILL.md',
  '编辑 SKILL.md',
  'update SKILL.md',
  'modify SKILL.md',
  'edit SKILL.md'
];

// 从标准输入读取用户输入
let userInput = '';
process.stdin.on('data', (chunk) => {
  userInput += chunk;
});

process.stdin.on('end', () => {
  const lowerInput = userInput.toLowerCase();

  // 检查是否包含更新关键词
  const hasUpdateKeyword = UPDATE_KEYWORDS.some(keyword =>
    lowerInput.includes(keyword.toLowerCase())
  );

  if (hasUpdateKeyword) {
    console.log('\n⚠️ 检测到 Skill 更新操作\n');
    console.log('请遵循以下原则：');
    console.log('1. SKILL.md 保持精简（< 500 行）');
    console.log('2. 详细内容放在 knowledge/');
    console.log('3. 通过引用而非复制关联内容\n');
    console.log('详细规范：UPDATE-GUIDELINES.md\n');
    console.log('请在更新前完成检查清单：');
    console.log('- [ ] 这个内容是核心流程吗？');
    console.log('- [ ] 是否会造成重复？');
    console.log('- [ ] SKILL.md 是否保持精简？\n');
    console.log('更新完成后请运行：./check-skill-structure.sh\n');
  }
});
