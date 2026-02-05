
## ⚠️ 恢复执行重要提醒

**当用户说"继续Step X"、"继续执行"、"下一步"时**：

本 Skill 的所有步骤都可能需要用户输入或确认。
在恢复执行任何步骤前，请遵循全局"恢复执行强制规则"（~/.claude/CLAUDE.md）：

1. ✅ 先读取该步骤的完整描述
2. ✅ 检查是否需要提问或确认
3. ✅ 确认所有输入参数
4. ✅ 有疑问先问用户

**禁止直接开始执行，禁止假设已知上下文。**

---

# OpenCode Model Manager

为 OpenCode 添加新模型的自动化工具。支持从第三方 API 聚合平台（如 DeepRouter）添加模型，自动配置并验证，确保不影响现有模型。

## 触发条件

当用户请求以下操作时触发：
- "添加 OpenCode 模型"
- "配置 OpenCode 新模型"
- "在 OpenCode 中添加 [模型名]"
- "/opencode-model-manager"

## 核心功能

1. **自动配置管理**
   - 读取并解析当前 OpenCode 配置文件
   - 智能添加新模型配置，避免覆盖现有配置
   - 为每个模型创建独立的 provider 配置

2. **API 验证**
   - 自动测试新模型的 API 连接
   - 验证 API Key 有效性
   - 确认模型 ID 正确性

3. **平台支持**
   - DeepRouter（默认支持）
   - 其他第三方 API 聚合平台（需提供文档）
   - 自动识别平台类型和配置要求

4. **安全保护**
   - 添加前自动备份配置文件
   - 配置验证失败时自动回滚
   - 保持现有模型配置不变

## 使用方法

### 基本用法

```
/opencode-model-manager

平台: DeepRouter
模型名称: claude-sonnet-4-5-thinking
API Key: sk-xxxxx
```

### 添加新平台的模型

```
/opencode-model-manager

平台: NewPlatform
平台文档: [文档路径或URL]
模型名称: model-name
API Key: sk-xxxxx
```

## 输入参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 平台名称 | 是 | API 聚合平台名称 | DeepRouter, OpenRouter |
| 模型名称 | 是 | 模型的 ID | claude-sonnet-4-5-thinking |
| API Key | 是 | 模型的 API 密钥 | sk-xxxxx |
| 平台文档 | 否 | 新平台需提供 API 文档 | 文件路径或 URL |
| 显示名称 | 否 | 模型的显示名称 | Claude Sonnet 4.5 Thinking |

## 工作流程

1. **收集信息**
   - 询问用户平台、模型名称、API Key
   - 如果是新平台，请求 API 文档

2. **读取当前配置**
   - 读取 `/Users/dj/.config/opencode/opencode.json`
   - 解析现有 provider 配置

3. **确定平台配置**
   - DeepRouter: `baseURL: https://deeprouter.top/v1`
   - 其他平台: 从文档中提取 baseURL

4. **验证 API**
   - 调用 `/v1/models` 获取支持的模型列表
   - 确认目标模型存在
   - 测试聊天接口 `/v1/chat/completions`

5. **生成配置**
   - 创建独立的 provider 配置
   - Provider ID 格式: `{platform}-{model-short-name}`
   - 避免与现有 provider 冲突

6. **备份并更新**
   - 备份当前配置到 `opencode.json.backup.{timestamp}`
   - 将新配置合并到配置文件
   - 保持 JSON 格式正确

7. **验证结果**
   - 再次读取配置文件确认
   - 提供重启 OpenCode 的指令
   - 提供验证命令 `/models`

## 配置模板

### DeepRouter 模板

```json
"{platform}-{model-short}": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "{Platform} {Model Display Name}",
  "options": {
    "baseURL": "https://deeprouter.top/v1",
    "apiKey": "{api_key}"
  },
  "models": {
    "{model_id}": {
      "name": "{Model Display Name}"
    }
  }
}
```

## 错误处理

1. **API Key 无效**
   - 提示用户检查 API Key
   - 不修改配置文件

2. **模型不存在**
   - 列出平台支持的模型
   - 让用户选择正确的模型 ID

3. **配置冲突**
   - 检测到同名 provider
   - 自动生成新的 provider ID

4. **JSON 格式错误**
   - 从备份恢复
   - 报告错误位置

## 输出示例

```
✓ 读取当前配置: 5 个 provider
✓ 验证 API 连接: 成功
✓ 确认模型存在: claude-sonnet-4-5-thinking
✓ 测试模型响应: 正常
✓ 备份配置文件: opencode.json.backup.20260128
✓ 添加新配置: deeprouter-sonnet
✓ 保存配置文件: 成功

配置完成！请执行以下步骤：

1. 重启 OpenCode:
   完全退出当前会话，然后运行: opencode

2. 验证模型列表:
   在 OpenCode 中输入: /models

3. 测试新模型:
   选择 "Claude Sonnet 4.5 Thinking" 并发送测试消息

新模型信息:
- Provider: deeprouter-sonnet
- Model ID: claude-sonnet-4-5-thinking
- Display Name: Claude Sonnet 4.5 Thinking
```

## 注意事项

1. **Provider ID 命名规则**
   - 格式: `{platform}-{model-identifier}`
   - 全小写，使用连字符
   - 避免特殊字符

2. **API Key 安全**
   - 直接写入配置文件（OpenCode 标准做法）
   - 不使用环境变量（避免复杂性）

3. **配置文件位置**
   - 主配置: `/Users/dj/.config/opencode/opencode.json`
   - 备份目录: 同目录下

4. **兼容性**
   - 仅支持 OpenAI 兼容的 API
   - 使用 `@ai-sdk/openai-compatible` npm 包

## 支持的平台

### 已知平台配置

| 平台 | Base URL | 文档 |
|------|----------|------|
| DeepRouter | https://deeprouter.top/v1 | 已内置 |
| OpenRouter | https://openrouter.ai/api/v1 | 需提供 |
| Together AI | https://api.together.xyz/v1 | 需提供 |

## 版本历史

- v1.0 (2026-01-28): 初始版本
  - 支持 DeepRouter
  - 自动 API 验证
  - 配置备份和回滚
