#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 读取 skill-rules.json
const rulesPath = path.join(process.env.HOME, '.claude/skills/_global_config/skill-rules.json');
let skillRules = { skills: {} };

try {
  skillRules = JSON.parse(fs.readFileSync(rulesPath, 'utf-8'));
} catch (e) {
  console.log('skill-rules.json not found');
  process.exit(0);
}

// 从标准输入读取用户输入
let userInput = '';
process.stdin.on('data', (chunk) => {
  userInput += chunk;
});

process.stdin.on('end', () => {
  const suggestions = [];
  const lowerInput = userInput.toLowerCase();

  // 遍历所有 skill 规则
  for (const [skillName, config] of Object.entries(skillRules.skills)) {
    if (!config.auto_suggest) continue;

    // 检查关键词匹配
    for (const trigger of config.triggers || []) {
      if (trigger.type === 'keyword') {
        for (const keyword of trigger.keywords || []) {
          if (lowerInput.includes(keyword.toLowerCase())) {
            suggestions.push(skillName);
            break;
          }
        }
      }
    }
  }

  // 输出建议
  if (suggestions.length > 0) {
    const uniqueSuggestions = [...new Set(suggestions)].slice(0, 3);
    console.log(`\n[系统提示] 检测到可能需要使用以下 Skill: ${uniqueSuggestions.join(', ')}`);
  }
});
