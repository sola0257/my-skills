# Skill Output Format Validation

## 概述

当你修改 `xiaohongshu-content-generator` skill 时，这个验证系统会帮助你确保输出格式与平台兼容。

## 🔒 三层保护机制

### 1. Skill 文件内嵌提醒（最直接）

打开 `xiaohongshu-content-generator/SKILL.md`，你会在顶部看到：

```
## 🔒 OUTPUT FORMAT CONTRACT (v1)

**⚠️ CRITICAL: This skill is integrated with xiaohongshu-visual-platform**

Required Output Format:
{
    "title": "string",
    "content": "string",
    "images": []
}
```

**作用**：每次打开 skill 文件时，立即看到输出格式要求。

### 2. 验证脚本（手动检查）

修改 skill 后，运行验证脚本测试输出格式：

```bash
cd /Users/dj/Desktop/小静的skills/xiaohongshu-visual-platform

# 测试 skill 输出
python validate_skill_output.py "多肉植物养护"
```

**输出示例（成功）**：
```
======================================================================
📋 VALIDATION RESULT
======================================================================

✅ OUTPUT FORMAT IS VALID

Output structure:
  - title: str (15 chars)
  - content: str (856 chars)
  - images: list (12 items)

✅ This output is compatible with xiaohongshu-visual-platform
```

**输出示例（失败）**：
```
======================================================================
📋 VALIDATION RESULT
======================================================================

❌ OUTPUT FORMAT IS INVALID

Errors found:
  ❌ Missing required field: 'images'
  ❌ Field 'title' must be string, got int

⚠️  This output will cause errors in xiaohongshu-visual-platform

Action required:
  1. Fix the skill output format
  2. OR update platform code to handle new format
  3. Read: xiaohongshu-visual-platform/docs/skill-output-format.md
```

### 3. 平台运行时验证（自动检查）

平台在运行时会自动验证 skill 输出：

```python
# backend/skill_caller.py
validate_skill_output(content_data, version='v1')
```

如果格式不对，会抛出清晰的错误信息。

## 📋 使用流程

### 修改 Skill 前

1. **打开 SKILL.md**，查看顶部的输出格式要求
2. **阅读文档**：`docs/skill-output-format.md`
3. **确认修改范围**：
   - ✅ 修改生成逻辑、提示词 → 安全
   - ⚠️ 修改输出字段名/类型 → 需要更新平台代码

### 修改 Skill 后

1. **运行验证脚本**：
   ```bash
   python validate_skill_output.py "测试主题"
   ```

2. **检查输出**：
   - ✅ 如果显示 "OUTPUT FORMAT IS VALID" → 可以提交
   - ❌ 如果显示错误 → 修复后再提交

3. **提交修改**：
   ```bash
   git add .
   git commit -m "update: skill logic optimization"
   ```

## 🎯 常见场景

### 场景 1：修改生成逻辑

```
你的修改：调整了内容生成的提示词
是否需要验证：✅ 建议验证（确保输出格式没变）
是否需要更新平台：❌ 不需要
```

### 场景 2：添加新字段

```
你的修改：在输出中添加了 "tags": [] 字段
是否需要验证：✅ 必须验证
是否需要更新平台：⚠️ 如果是可选字段，不需要；如果是必需字段，需要更新
```

### 场景 3：修改字段名

```
你的修改：将 "title" 改为 "main_title"
是否需要验证：✅ 必须验证（会失败）
是否需要更新平台：✅ 必须更新 skill_caller.py 和 app.py
```

## 📚 相关文档

- **输出格式规范**：`docs/skill-output-format.md`
- **Skill 源文件**：`/Users/dj/Desktop/小静的skills/xiaohongshu-content-generator/SKILL.md`
- **平台验证代码**：`backend/skill_caller.py`

## 💡 最佳实践

1. **修改前先看文档**：打开 SKILL.md 查看输出格式要求
2. **修改后立即验证**：运行 `validate_skill_output.py`
3. **保持格式稳定**：只修改内部逻辑，不修改输出结构
4. **如需改格式**：先更新平台代码，再修改 skill

## ❓ 常见问题

**Q: 我只是修改了提示词，需要验证吗？**
A: 建议验证一下，确保输出格式没有意外改变。

**Q: 验证脚本报错怎么办？**
A: 检查错误信息，修复 skill 输出格式，或者更新平台代码。

**Q: 我想添加新字段，怎么做？**
A: 如果是可选字段，直接添加即可；如果是必需字段，需要先更新平台的 `REQUIRED_FIELDS_V1`。

**Q: 验证脚本运行很慢？**
A: 正常，因为它会实际调用 skill 生成内容（可能需要 1-2 分钟）。

---

**最后更新**：2026-02-06
