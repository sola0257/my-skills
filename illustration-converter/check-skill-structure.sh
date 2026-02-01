#!/bin/bash
# Skill 更新检查工具
# 用于检查是否遵循"渐进式披露"和"Skill 精简"原则

echo "🔍 Skill 更新检查工具"
echo "===================="
echo ""

# 检查 SKILL.md 行数
SKILL_LINES=$(wc -l < SKILL.md)
echo "📄 SKILL.md 行数: $SKILL_LINES"

if [ $SKILL_LINES -gt 500 ]; then
    echo "⚠️  警告: SKILL.md 超过 500 行，建议精简"
    echo "   考虑将详细内容移到 knowledge/ 目录"
else
    echo "✅ SKILL.md 行数合理"
fi

echo ""

# 检查 knowledge/ 目录
if [ -d "knowledge" ]; then
    KNOWLEDGE_FILES=$(ls -1 knowledge/*.md 2>/dev/null | wc -l)
    echo "📚 knowledge/ 文档数量: $KNOWLEDGE_FILES"

    if [ $KNOWLEDGE_FILES -eq 0 ]; then
        echo "⚠️  警告: knowledge/ 目录为空"
    else
        echo "✅ knowledge/ 目录有文档"
    fi
else
    echo "❌ 错误: knowledge/ 目录不存在"
fi

echo ""

# 检查是否有 UPDATE-GUIDELINES.md
if [ -f "UPDATE-GUIDELINES.md" ]; then
    echo "✅ 更新规范文档存在"
else
    echo "⚠️  警告: 缺少 UPDATE-GUIDELINES.md"
fi

echo ""

# 检查 knowledge/README.md
if [ -f "knowledge/README.md" ]; then
    echo "✅ knowledge/README.md 存在"
else
    echo "⚠️  警告: 缺少 knowledge/README.md"
fi

echo ""
echo "===================="
echo "检查完成"
echo ""
echo "💡 提示:"
echo "- SKILL.md 应保持 < 500 行"
echo "- 详细内容应放在 knowledge/ 目录"
echo "- 更新前请阅读 UPDATE-GUIDELINES.md"
