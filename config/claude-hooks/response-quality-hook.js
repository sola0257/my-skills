#!/usr/bin/env node

/**
 * Response Quality Hook for Claude Code
 *
 * 当用户询问建议、方案、策略时，自动提醒 Claude 执行3步检查：
 * 1. 共情检查（第一段必须回应用户的情绪/困境）
 * 2. 创新点检查（必须有至少1个用户没想到的点子）
 * 3. 接地气检查（必须给出本周可做的3件事）
 *
 * Hook 类型: UserPromptSubmit
 */

const fs = require('fs');
const path = require('path');

// 从标准输入读取用户输入
let userInput = '';
process.stdin.on('data', (chunk) => {
  userInput += chunk;
});

process.stdin.on('end', () => {
  const lowerInput = userInput.toLowerCase();

  // 检测是否是询问建议/方案/策略的场景
  const advicePatterns = [
    // 直接询问
    /如何|怎么|怎样|怎么办/,
    /建议|方案|策略|思路|办法/,
    /帮我|帮助我|给我/,

    // 描述困境
    /困惑|迷茫|不知道|不清楚|混乱/,
    /问题|困难|挑战|瓶颈/,

    // 请求分析
    /分析|评估|判断|看看/,
    /应该|需要|想要|打算/,

    // 对比/选择
    /还是|或者|vs|pk|对比/,
    /哪个|哪种|选择/
  ];

  // 检查是否匹配任何模式
  const needsAdvice = advicePatterns.some(pattern => pattern.test(lowerInput));

  // 检测是否是描述困境的长文本（超过100字）
  const isLongDescription = userInput.length > 100;

  // 检测是否包含情绪词汇
  const emotionWords = [
    '焦虑', '担心', '害怕', '困惑', '迷茫', '无助',
    '不知道', '不清楚', '混乱', '纠结', '犹豫'
  ];
  const hasEmotion = emotionWords.some(word => lowerInput.includes(word));

  if (needsAdvice || (isLongDescription && hasEmotion)) {
    console.log('\n' + '='.repeat(80));
    console.log('🎯 [回复质量提醒] 检测到用户需要建议/方案/策略');
    console.log('='.repeat(80));
    console.log('\n请在回复前完成以下3步检查：\n');

    console.log('✅ 1. 共情检查（第一段必须做到）');
    console.log('   - 第一段必须先回应用户的情绪/困境/焦虑');
    console.log('   - 用具体的语言描述用户的处境');
    console.log('   - 让用户感受到"你理解我"\n');

    console.log('✅ 2. 创新点检查（必须有至少1个）');
    console.log('   - 必须提出至少1个"用户没想到的"创新点');
    console.log('   - 创新点必须是可执行的，不是空想');
    console.log('   - 创新点必须结合用户的具体资源和优势\n');

    console.log('✅ 3. 接地气检查（必须有具体行动）');
    console.log('   - 必须给出"本周/今天可以做的3件事"');
    console.log('   - 每件事必须具体到"做什么、怎么做、预期结果"');
    console.log('   - 不能只有理论，必须有可执行的步骤\n');

    console.log('📋 回复结构模板：');
    console.log('   1. 开头：共情（回应情绪）');
    console.log('   2. 核心分析（系统性分析）');
    console.log('   3. 创新点（至少1个）');
    console.log('   4. 本周可做的3件事（具体到每一步）');
    console.log('   5. 结尾：行动号召\n');

    console.log('='.repeat(80));
    console.log('');
  }
});
