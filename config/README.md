# Claude Code Hook 和工具管理

## 目录结构

```
/Users/dj/Desktop/小静的skills/config/
├── claude-hooks/              # 自动触发的 Hook（必须在 settings.json 中配置）
│   ├── skill-activation-hook.js
│   ├── response-quality-hook.js
│   ├── quality-evaluator-hook.js
│   ├── skill-execution-auditor-hook-v2.js
│   ├── skill-change-detector.js
│   └── continuous-learning-hook.js
│
└── claude-tools/              # 手动运行的工具（不需要在 settings.json 中配置）
    ├── rule-consistency-checker-v3.js
    └── skill-execution-auditor-hook-v1-deprecated.js
```

## 自动触发的 Hook

这些 Hook 已在 `/Users/dj/.claude/settings.json` 中配置，会自动触发：

| Hook 文件 | 触发类型 | 触发时机 | 用途 |
|----------|---------|---------|------|
| skill-activation-hook.js | UserPromptSubmit | 用户提交输入时 | 根据关键词建议使用相关 Skill |
| response-quality-hook.js | UserPromptSubmit | 用户提交输入时 | 提醒 Claude 执行3步检查（共情、创新点、接地气） |
| quality-evaluator-hook.js | PostToolUse | 工具使用后 | 评估工具使用质量 |
| skill-execution-auditor-hook-v2.js | PostToolUse | 工具使用后 | 审计 Skill 执行流程 |
| skill-change-detector.js | SessionStart | 会话开始时 | 检测 Skills 更新 |
| continuous-learning-hook.js | SessionEnd | 会话结束时 | 保存学习数据 |

## 手动运行的工具

这些工具不会自动触发，需要手动运行：

### rule-consistency-checker-v3.js

**用途**：扫描所有文档，识别潜在的规则冲突

**运行方式**：
```bash
node /Users/dj/Desktop/小静的skills/config/claude-tools/rule-consistency-checker-v3.js
```

**何时运行**：
- 修改了 CLAUDE.md 或 SKILL.md 后
- 怀疑规则不一致时
- 定期检查（如每周一次）

**输出**：
- 报告文件：`~/.claude/skills/_global_config/rule-consistency-report-v3.json`
- 控制台输出：潜在冲突列表

### skill-execution-auditor-hook-v1-deprecated.js

**状态**：已废弃，被 v2 版本替代

**建议**：可以删除此文件

## 如何添加新的 Hook

### 1. 创建 Hook 文件

```bash
# 在 claude-hooks/ 目录创建
touch /Users/dj/Desktop/小静的skills/config/claude-hooks/your-hook.js
chmod +x /Users/dj/Desktop/小静的skills/config/claude-hooks/your-hook.js
```

### 2. 创建符号链接

```bash
ln -s /Users/dj/Desktop/小静的skills/config/claude-hooks/your-hook.js \
      /Users/dj/.claude/hooks/your-hook.js
```

### 3. 在 settings.json 中配置

编辑 `/Users/dj/.claude/settings.json`，在对应的触发类型下添加：

```json
"UserPromptSubmit": [
  {
    "hooks": [
      {
        "command": "node ~/.claude/hooks/your-hook.js",
        "statusMessage": "描述",
        "type": "command"
      }
    ]
  }
]
```

### 4. 重启 Claude Code

配置修改后需要重启 Claude Code 才能生效。

## 可用的触发类型

| 触发类型 | 触发时机 | 适用场景 |
|---------|---------|---------|
| UserPromptSubmit | 用户提交输入后 | 输入分析、Skill 建议、质量检查 |
| PreToolUse | 工具使用前 | 权限检查、参数验证 |
| PostToolUse | 工具使用后 | 质量评估、自动格式化、测试运行 |
| SessionStart | 会话开始时 | 初始化、环境检查 |
| SessionEnd | 会话结束时 | 数据保存、清理工作 |
| Notification | 通知时 | 权限提示、空闲提醒 |

## 管理原则

1. **自动触发的 Hook 必须在 settings.json 中配置**
2. **手动运行的工具放在 claude-tools/ 目录**
3. **废弃的文件标记为 deprecated 或直接删除**
4. **每个 Hook 文件开头必须注明触发类型和用途**
5. **定期检查和清理不再使用的 Hook**

## 常见问题

### Q: 为什么我的 Hook 没有触发？

A: 检查以下几点：
1. Hook 文件是否有执行权限（`chmod +x`）
2. 符号链接是否正确创建（`ls -la ~/.claude/hooks/`）
3. settings.json 中是否正确配置
4. 是否重启了 Claude Code

### Q: 如何调试 Hook？

A: 在 Hook 文件中添加 console.log，输出会显示在 Claude Code 的控制台中。

### Q: Hook 执行失败会影响 Claude 的正常工作吗？

A: 不会。Hook 执行失败只会显示错误信息，不会阻止 Claude 的正常工作。

---

**最后更新**：2026-01-31
**维护者**：小静
