# 全局 API 配置说明

## 📋 概述

本目录包含所有 skills 共享的 API 配置，确保统一的 API 调用和安全的密钥管理。

## 📁 文件说明

### 1. `api_config.json`（非敏感配置）

包含 API 的基础配置信息：
- API 端点 URL
- 默认模型
- 其他非敏感参数

**示例**：
```json
{
  "yunwu": {
    "base_url": "https://yunwu.ai/v1",
    "chat_endpoint": "/chat/completions",
    "default_model": "gemini-3-pro-image-preview"
  }
}
```

### 2. `.env`（敏感信息）

包含 API 密钥等敏感信息：
- API Key
- 其他认证信息

**⚠️ 安全提示**：
- 此文件应加入 `.gitignore`
- 不要提交到版本控制系统
- 不要分享给他人

**示例**：
```bash
YUNWU_API_KEY=sk-xxx...
```

## 🔧 使用方式

### 在 Python 脚本中使用

```python
from pathlib import Path
import json
import os

# 加载配置
config_dir = Path(__file__).parent.parent / "_global_config"

# 读取 API 配置
with open(config_dir / "api_config.json") as f:
    config = json.load(f)

# 读取 API Key
from dotenv import load_dotenv
load_dotenv(config_dir / ".env")
api_key = os.getenv("YUNWU_API_KEY")
```

### 使用统一 API 客户端（推荐）

```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "_shared_scripts"))
from yunwu_image_api import generate_image, batch_generate

# 单张图片生成
generate_image(prompt, output_path, aspect_ratio="3:4", allow_text=False)

# 批量生成
results = batch_generate(prompts_dict, base_dir, text_config, aspect_ratio="3:4")
```

## 🎯 强制规则

### 所有 skills 必须遵守

1. **统一 API 客户端**：
   - ✅ 必须使用 `_shared_scripts/yunwu_image_api.py`
   - ❌ 禁止创建新的 API 调用脚本
   - ❌ 禁止在 skill 内部硬编码 API 配置

2. **强制使用 Gemini 模型**：
   - ✅ 所有图片生成必须使用 `gemini-3-pro-image-preview`
   - ❌ 禁止随意更改模型
   - ❌ 禁止使用其他模型（如 DALL-E）

3. **Prompt 质量保证**：
   - ✅ 必须参考案例库标准创建 prompt
   - ✅ 封面：`knowledge/image-generation-cases/case-002-xhs-cover.md`
   - ✅ 正文：`knowledge/image-generation-cases/case-003-xhs-scene.md`

## 📊 架构图

```
全域自媒体运营/
└── 小静的skills/
    ├── _global_config/              # 全局配置（本目录）
    │   ├── api_config.json         # API 配置
    │   └── .env                     # 敏感信息
    ├── _shared_scripts/             # 共享脚本
    │   └── yunwu_image_api.py      # 统一 API 客户端
    ├── xiaohongshu-content-generator/
    │   └── SKILL.md                # 调用统一客户端
    ├── wechat-content-generator/
    │   └── SKILL.md                # 调用统一客户端
    └── video-script-generator/
        └── SKILL.md                # 调用统一客户端
```

## 🔄 更新日志

### v1.0 (2026-01-31)
- ✅ 创建全局配置架构
- ✅ 创建统一 API 客户端
- ✅ 强制使用 Gemini 模型
- ✅ 集中管理 API 密钥

---

**维护者**：Claude Code
**最后更新**：2026-01-31
