# OpenCode Model Manager

为 OpenCode 添加新模型的自动化 Skill。

## 快速开始

```
/opencode-model-manager

平台: DeepRouter
模型名称: claude-sonnet-4-5-thinking
API Key: sk-xxxxx
```

## 功能特性

- ✅ 自动验证 API 连接和模型可用性
- ✅ 智能生成 Provider ID，避免冲突
- ✅ 自动备份配置文件
- ✅ 保护现有模型配置不受影响
- ✅ 支持批量添加多个模型
- ✅ 支持多个第三方 API 平台
- ✅ 详细的错误提示和恢复指导

## 支持的平台

- **DeepRouter** (默认支持)
- **OpenRouter** (需提供文档)
- **Together AI** (需提供文档)
- 其他 OpenAI 兼容的 API 平台

## 文档

- [SKILL.md](./SKILL.md) - 完整功能说明
- [implementation.md](./implementation.md) - 实现指南（供 Claude 使用）
- [examples.md](./examples.md) - 使用示例

## 为什么需要这个 Skill？

在手动配置 OpenCode 模型时，常见问题：

1. **配置错误** - JSON 格式错误导致 OpenCode 无法启动
2. **API Key 混淆** - 多个模型使用了错误的 API Key
3. **覆盖现有配置** - 添加新模型时意外修改了旧配置
4. **Provider ID 冲突** - 重复的 Provider ID 导致模型无法加载

这个 Skill 自动处理所有这些问题，确保配置过程安全可靠。

## 工作原理

1. **验证阶段** - 测试 API Key 和模型可用性
2. **备份阶段** - 自动备份当前配置
3. **配置阶段** - 生成并添加新的 Provider 配置
4. **验证阶段** - 确认配置文件格式正确
5. **指导阶段** - 提供重启和测试步骤

## 安全保证

- 配置前自动备份
- API 验证失败时不修改配置
- JSON 格式错误时自动回滚
- 独立的 Provider 配置，互不影响

## 版本

v1.0 (2026-01-28)

## 作者

Created for OpenCode model management automation.
