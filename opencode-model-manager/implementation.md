# OpenCode Model Manager - 实现指南

本文档为 Claude 提供执行此 Skill 的详细步骤和代码实现。

## 执行流程

### 阶段 1: 信息收集

使用 AskUserQuestion 工具收集必要信息（如果用户未提供）：

```
问题 1: 平台名称
- DeepRouter (推荐)
- OpenRouter
- Together AI
- 其他（需提供文档）

问题 2: 模型名称
提示: 模型的 ID，如 claude-sonnet-4-5-thinking

问题 3: API Key
提示: 以 sk- 开头的密钥

问题 4: 显示名称（可选）
提示: 在 OpenCode 中显示的名称，如 Claude Sonnet 4.5 Thinking
```

### 阶段 2: 平台配置确定

根据平台名称确定配置：

```python
# 已知平台配置
PLATFORM_CONFIGS = {
    "deeprouter": {
        "baseURL": "https://deeprouter.top/v1",
        "npm": "@ai-sdk/openai-compatible"
    },
    "openrouter": {
        "baseURL": "https://openrouter.ai/api/v1",
        "npm": "@ai-sdk/openai-compatible"
    },
    "together": {
        "baseURL": "https://api.together.xyz/v1",
        "npm": "@ai-sdk/openai-compatible"
    }
}
```

如果是新平台，使用 WebFetch 或 Read 工具读取文档，提取 baseURL。

### 阶段 3: API 验证

#### 3.1 获取模型列表

```bash
curl -s -H "Authorization: Bearer {api_key}" \
  {baseURL}/models | python3 -m json.tool
```

检查返回的模型列表中是否包含目标模型 ID。

#### 3.2 测试聊天接口

```bash
curl -s -X POST {baseURL}/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {api_key}" \
  -d '{"model":"{model_id}","messages":[{"role":"user","content":"test"}],"stream":false}' \
  | python3 -m json.tool
```

验证返回状态码为 200 且包含 choices 字段。

### 阶段 4: 读取当前配置

```bash
# 读取配置文件
Read /Users/dj/.config/opencode/opencode.json
```

解析 JSON，提取现有的 provider 列表。

### 阶段 5: 生成 Provider ID

规则：
1. 基础格式: `{platform}-{model-short-name}`
2. 转换为小写
3. 移除特殊字符，保留连字符
4. 检查是否与现有 provider 冲突
5. 如果冲突，添加数字后缀: `-2`, `-3` 等

示例代码逻辑：
```python
def generate_provider_id(platform, model_id, existing_providers):
    # 提取模型简称
    # claude-sonnet-4-5-thinking -> sonnet
    # minimax-m2.1 -> minimax

    model_short = extract_short_name(model_id)
    base_id = f"{platform.lower()}-{model_short}"

    # 检查冲突
    provider_id = base_id
    counter = 2
    while provider_id in existing_providers:
        provider_id = f"{base_id}-{counter}"
        counter += 1

    return provider_id
```

### 阶段 6: 备份配置

```bash
# 创建备份
timestamp=$(date +%Y%m%d_%H%M%S)
cp /Users/dj/.config/opencode/opencode.json \
   /Users/dj/.config/opencode/opencode.json.backup.$timestamp
```

### 阶段 7: 更新配置

使用 Read 读取配置，使用 Edit 工具更新：

1. 找到 `"provider"` 对象的最后一个 provider
2. 在最后一个 provider 后添加新配置
3. 确保 JSON 格式正确（逗号、缩进）

新 provider 配置模板：
```json
"{provider_id}": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "{Platform} {Display Name}",
  "options": {
    "baseURL": "{baseURL}",
    "apiKey": "{api_key}"
  },
  "models": {
    "{model_id}": {
      "name": "{display_name}"
    }
  }
}
```

### 阶段 8: 验证配置

```bash
# 验证 JSON 格式
python3 -m json.tool /Users/dj/.config/opencode/opencode.json > /dev/null
echo $?  # 应该返回 0
```

如果验证失败，从备份恢复：
```bash
cp /Users/dj/.config/opencode/opencode.json.backup.$timestamp \
   /Users/dj/.config/opencode/opencode.json
```

### 阶段 9: 输出结果

生成格式化的成功消息，包括：
1. 配置摘要
2. 重启指令
3. 验证步骤
4. 新模型信息

## 关键实现细节

### 模型简称提取

```python
def extract_short_name(model_id):
    """
    从模型 ID 提取简短标识符

    示例:
    - claude-sonnet-4-5-thinking -> sonnet
    - claude-opus-4-5-20251101-thinking -> opus
    - minimax-m2.1 -> minimax
    - gpt-4-turbo -> gpt4turbo
    - deepseek-v3.1 -> deepseek
    """

    # 移除版本号和日期
    name = re.sub(r'-\d+\.?\d*', '', model_id)
    name = re.sub(r'-\d{8}', '', name)
    name = re.sub(r'-thinking$', '', name)

    # 提取关键词
    parts = name.split('-')
    if 'sonnet' in parts:
        return 'sonnet'
    elif 'opus' in parts:
        return 'opus'
    elif 'minimax' in parts:
        return 'minimax'
    else:
        return parts[0]
```

### JSON 安全编辑

使用 Edit 工具时的注意事项：

1. **找到插入点**: 定位到最后一个 provider 的闭合大括号
2. **添加逗号**: 确保在最后一个 provider 后添加逗号
3. **保持缩进**: 使用 2 个空格缩进
4. **完整性检查**: 确保所有括号匹配

示例 old_string（假设 minimax-conch 是最后一个）：
```json
    "minimax-conch": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "MiniMax (海螺)",
      "options": {
        "baseURL": "https://api.minimaxi.com/v1",
        "apiKey": "sk-api-..."
      },
      "models": {
        "MiniMax-M2.1": {
          "name": "MiniMax M2.1 (Reasoning)"
        }
      }
    }
  }
}
```

示例 new_string：
```json
    "minimax-conch": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "MiniMax (海螺)",
      "options": {
        "baseURL": "https://api.minimaxi.com/v1",
        "apiKey": "sk-api-..."
      },
      "models": {
        "MiniMax-M2.1": {
          "name": "MiniMax M2.1 (Reasoning)"
        }
      }
    },
    "deeprouter-newmodel": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "DeepRouter New Model",
      "options": {
        "baseURL": "https://deeprouter.top/v1",
        "apiKey": "sk-xxxxx"
      },
      "models": {
        "new-model-id": {
          "name": "New Model Display Name"
        }
      }
    }
  }
}
```

## 错误处理

### API 验证失败

```
错误: API Key 验证失败

可能原因:
1. API Key 不正确
2. API Key 已过期
3. 模型 ID 不存在于该 Key 的权限中

建议:
- 检查 API Key 是否正确复制
- 访问平台控制台确认 Key 状态
- 确认该 Key 是否有权限访问此模型
```

### 模型不存在

```
错误: 模型 '{model_id}' 不存在

该平台支持的模型:
- model-1
- model-2
- model-3

请选择正确的模型 ID 或访问平台文档确认。
```

### JSON 格式错误

```
错误: 配置文件格式错误

已自动从备份恢复: opencode.json.backup.{timestamp}

错误详情: {error_message}

请检查配置文件格式，或手动编辑修复。
```

## 测试检查清单

执行完成后，提供以下检查清单：

```
配置完成检查清单:

□ 配置文件已更新
□ JSON 格式验证通过
□ 备份文件已创建
□ 新 provider 已添加
□ 现有配置未改变

下一步操作:

1. □ 完全退出 OpenCode
2. □ 重新启动 OpenCode
3. □ 运行 /models 查看模型列表
4. □ 选择新模型发送测试消息
5. □ 确认旧模型仍然可用

如遇问题:
- 查看备份: /Users/dj/.config/opencode/opencode.json.backup.{timestamp}
- 恢复命令: cp [备份文件] /Users/dj/.config/opencode/opencode.json
```

## 常见问题

### Q: 为什么每个模型需要独立的 provider？

A: 因为每个模型使用不同的 API Key。OpenCode 的 provider 配置中，apiKey 是 provider 级别的，不是 model 级别的。

### Q: 可以在一个 provider 下配置多个模型吗？

A: 可以，但前提是这些模型使用相同的 API Key。如果 API Key 不同，必须创建独立的 provider。

### Q: 如何处理模型名称冲突？

A: Provider ID 会自动添加数字后缀（-2, -3 等）来避免冲突。模型的显示名称可以相同，因为它们属于不同的 provider。

### Q: 配置后需要重启 OpenCode 吗？

A: 是的，OpenCode 在启动时读取配置文件。修改配置后必须完全退出并重新启动才能生效。
