# OpenCode Model Manager - 使用示例

## 示例 1: 添加 DeepRouter 的 Claude 模型

### 用户输入

```
/opencode-model-manager

平台: DeepRouter
模型名称: claude-sonnet-4-5-thinking
API Key: sk-t7cTRhpPNEYw06nD7yI5UgUeocXRiz2RMxZ1B3xboBXAFRSr
显示名称: Claude Sonnet 4.5 Thinking
```

### Claude 执行步骤

1. **验证 API**
```bash
# 获取模型列表
curl -s -H "Authorization: Bearer sk-t7cTRhpPNEYw06nD7yI5UgUeocXRiz2RMxZ1B3xboBXAFRSr" \
  https://deeprouter.top/v1/models | python3 -m json.tool | grep -i "claude-sonnet-4-5-thinking"

# 测试聊天
curl -s -X POST https://deeprouter.top/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-t7cTRhpPNEYw06nD7yI5UgUeocXRiz2RMxZ1B3xboBXAFRSr" \
  -d '{"model":"claude-sonnet-4-5-thinking","messages":[{"role":"user","content":"test"}],"stream":false}'
```

2. **读取配置**
```bash
Read /Users/dj/.config/opencode/opencode.json
```

3. **生成 Provider ID**
```
平台: deeprouter
模型: claude-sonnet-4-5-thinking
简称: sonnet
Provider ID: deeprouter-sonnet
```

4. **备份配置**
```bash
cp /Users/dj/.config/opencode/opencode.json \
   /Users/dj/.config/opencode/opencode.json.backup.20260128_230000
```

5. **添加配置**
```json
"deeprouter-sonnet": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "DeepRouter Sonnet",
  "options": {
    "baseURL": "https://deeprouter.top/v1",
    "apiKey": "sk-t7cTRhpPNEYw06nD7yI5UgUeocXRiz2RMxZ1B3xboBXAFRSr"
  },
  "models": {
    "claude-sonnet-4-5-thinking": {
      "name": "Claude Sonnet 4.5 Thinking"
    }
  }
}
```

### 输出结果

```
✓ 读取当前配置: 5 个 provider
✓ 验证 API 连接: 成功
✓ 确认模型存在: claude-sonnet-4-5-thinking
✓ 测试模型响应: 正常
✓ 备份配置文件: opencode.json.backup.20260128_230000
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
- Platform: DeepRouter
```

---

## 示例 2: 添加多个模型（批量）

### 用户输入

```
/opencode-model-manager

我要添加三个 DeepRouter 模型：

1. claude-sonnet-4-5-thinking, key: sk-t7cTRhpPNEYw06nD7yI5UgUeocXRiz2RMxZ1B3xboBXAFRSr
2. claude-opus-4-5-20251101-thinking, key: sk-ZZx8CL3InOIKFR7WkYb1aThtqbqTGdhjlKXMnzeqJlNnKayt
3. minimax-m2.1, key: sk-88TFJqHh03vtYkkIIOQY9XUmikXoAxJncUynztFlC5Dr0nuh
```

### Claude 执行步骤

对每个模型重复以下步骤：

1. 验证 API
2. 生成 Provider ID
3. 添加配置

生成的 Provider IDs:
- `deeprouter-sonnet`
- `deeprouter-opus`
- `deeprouter-minimax`

### 输出结果

```
批量添加完成！

已添加 3 个模型:

1. ✓ deeprouter-sonnet
   - Model: claude-sonnet-4-5-thinking
   - Name: Claude Sonnet 4.5 Thinking

2. ✓ deeprouter-opus
   - Model: claude-opus-4-5-20251101-thinking
   - Name: Claude Opus 4.5 Thinking

3. ✓ deeprouter-minimax
   - Model: minimax-m2.1
   - Name: MiniMax M2.1

备份文件: opencode.json.backup.20260128_230000

请重启 OpenCode 并运行 /models 验证。
```

---

## 示例 3: 添加新平台的模型

### 用户输入

```
/opencode-model-manager

平台: OpenRouter
平台文档: https://openrouter.ai/docs
模型名称: anthropic/claude-3.5-sonnet
API Key: sk-or-v1-xxxxx
```

### Claude 执行步骤

1. **读取平台文档**
```
WebFetch https://openrouter.ai/docs
提取: baseURL = https://openrouter.ai/api/v1
```

2. **验证 API**
```bash
curl -s -H "Authorization: Bearer sk-or-v1-xxxxx" \
  https://openrouter.ai/api/v1/models
```

3. **生成配置**
```json
"openrouter-claude35": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "OpenRouter Claude 3.5",
  "options": {
    "baseURL": "https://openrouter.ai/api/v1",
    "apiKey": "sk-or-v1-xxxxx"
  },
  "models": {
    "anthropic/claude-3.5-sonnet": {
      "name": "Claude 3.5 Sonnet"
    }
  }
}
```

---

## 示例 4: 处理错误 - API Key 无效

### 用户输入

```
/opencode-model-manager

平台: DeepRouter
模型名称: claude-sonnet-4-5-thinking
API Key: sk-invalid-key
```

### Claude 执行步骤

1. **验证 API**
```bash
curl -s -H "Authorization: Bearer sk-invalid-key" \
  https://deeprouter.top/v1/models
```

返回错误: `{"error": {"message": "Invalid API key"}}`

### 输出结果

```
❌ 配置失败

错误: API Key 验证失败

返回信息: Invalid API key

可能原因:
1. API Key 不正确或已过期
2. API Key 格式错误
3. 该 Key 没有访问权限

建议:
- 检查 API Key 是否正确复制（注意空格）
- 访问 DeepRouter 控制台确认 Key 状态
- 确认该 Key 是否有权限访问此模型

配置文件未修改，请修正后重试。
```

---

## 示例 5: 处理错误 - 模型不存在

### 用户输入

```
/opencode-model-manager

平台: DeepRouter
模型名称: gpt-5-ultra
API Key: sk-valid-key
```

### Claude 执行步骤

1. **获取模型列表**
```bash
curl -s -H "Authorization: Bearer sk-valid-key" \
  https://deeprouter.top/v1/models | python3 -m json.tool
```

2. **搜索模型**
```bash
# 在返回的模型列表中搜索 gpt-5-ultra
# 结果: 未找到
```

### 输出结果

```
❌ 配置失败

错误: 模型 'gpt-5-ultra' 不存在

该 API Key 支持的模型（部分）:
- claude-sonnet-4-5-thinking
- claude-opus-4-5-20251101-thinking
- minimax-m2.1
- deepseek-v3.1
- gpt-4-turbo
- gemini-2.0-flash

建议:
- 检查模型名称拼写
- 访问 DeepRouter 文档查看完整模型列表
- 确认该模型是否需要特殊权限

配置文件未修改，请使用正确的模型名称重试。
```

---

## 示例 6: 处理冲突 - Provider ID 已存在

### 场景

配置文件中已存在 `deeprouter-sonnet`，用户尝试添加另一个 Sonnet 模型。

### 用户输入

```
/opencode-model-manager

平台: DeepRouter
模型名称: claude-sonnet-4-5-thinking
API Key: sk-another-key
```

### Claude 执行步骤

1. **检测冲突**
```
生成的 Provider ID: deeprouter-sonnet
检查现有配置: deeprouter-sonnet 已存在
```

2. **自动解决**
```
尝试: deeprouter-sonnet-2
检查: 不存在
使用: deeprouter-sonnet-2
```

### 输出结果

```
⚠️  Provider ID 冲突已自动解决

原 Provider ID: deeprouter-sonnet (已存在)
新 Provider ID: deeprouter-sonnet-2

✓ 配置完成

新模型信息:
- Provider: deeprouter-sonnet-2
- Model ID: claude-sonnet-4-5-thinking
- Display Name: Claude Sonnet 4.5 Thinking

注意: 这是第二个 Sonnet 配置，使用不同的 API Key。
```

---

## 快速参考

### 最简单的调用方式

```
/opencode-model-manager

DeepRouter
claude-sonnet-4-5-thinking
sk-xxxxx
```

### 完整参数调用

```
/opencode-model-manager

平台: DeepRouter
模型名称: claude-sonnet-4-5-thinking
API Key: sk-xxxxx
显示名称: Claude Sonnet 4.5 Thinking
```

### 验证配置

```bash
# 查看配置文件
cat /Users/dj/.config/opencode/opencode.json

# 验证 JSON 格式
python3 -m json.tool /Users/dj/.config/opencode/opencode.json

# 查看备份
ls -lt /Users/dj/.config/opencode/*.backup.*
```

### 恢复配置

```bash
# 从最新备份恢复
cp /Users/dj/.config/opencode/opencode.json.backup.20260128_230000 \
   /Users/dj/.config/opencode/opencode.json
```
