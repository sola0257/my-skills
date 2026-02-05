# 提示词模板使用指南

**版本**: v1.0
**更新日期**: 2026-02-05

## 📋 目录结构

```
_global_config/prompt-templates/
├── text-optimize/              # 文本提示词优化
│   └── system-prompt-general.md
├── image-optimize/             # 图像提示词优化
│   └── image-prompt-general.md
└── docs/                       # 文档
    ├── README.md              # 本文件
    └── template-selection-guide.md
```

## 🎯 模板选择决策树

### 场景1：内容生成（文本）

**触发条件**：
- 生成小红书文案
- 生成微信公众号文章
- 生成视频脚本

**使用模板**：`text-optimize/system-prompt-general.md`

**使用时机**：
- 在生成内容之前
- 优化系统提示词（System Prompt）

**预期效果**：
- 提示词结构化（Role/Profile/Skills/Rules/Workflows）
- 生成内容更专业、更符合要求

### 场景2：图像生成（配图）

**触发条件**：
- 生成小红书配图
- 生成微信公众号配图
- 生成视频封面/分镜图

**使用模板**：`image-optimize/image-prompt-general.md`

**使用时机**：
- 在调用图像生成 API 之前
- 优化图像描述提示词

**预期效果**：
- 图像描述更详细（主体/动作/环境/光线/色彩/材质/氛围/构图）
- 生成图像更符合预期

### 场景3：知识提取

**触发条件**：
- 使用 knowledge-extractor
- 提取文档中的方法论

**使用模板**：`text-optimize/system-prompt-general.md`

**使用时机**：
- 在提取知识之前
- 优化提取指令

**预期效果**：
- 提取的知识更结构化
- 提取质量更高

## 🔄 集成方式

### 方式1：在 Skill 中集成（推荐）

在 SKILL.md 中添加提示词优化步骤：

```markdown
### Step X: 优化提示词

**目的**：使用经过验证的模板优化提示词，提升生成质量

**执行**：
1. 读取对应的模板文件
2. 将原始提示词插入模板
3. 调用 LLM 获取优化后的提示词
4. 使用优化后的提示词执行后续任务

**模板选择**：
- 文本生成 → `text-optimize/system-prompt-general.md`
- 图像生成 → `image-optimize/image-prompt-general.md`
```

### 方式2：在 Python 脚本中集成

创建统一的优化函数：

```python
# _global_config/prompt-templates/optimizer.py

def optimize_prompt(original_prompt: str, template_type: str) -> str:
    """
    优化提示词

    Args:
        original_prompt: 原始提示词
        template_type: 模板类型 ('system' | 'image')

    Returns:
        优化后的提示词
    """
    template_map = {
        'system': 'text-optimize/system-prompt-general.md',
        'image': 'image-optimize/image-prompt-general.md'
    }

    template_path = f"/Users/dj/Desktop/小静的skills/_global_config/prompt-templates/{template_map[template_type]}"

    with open(template_path, 'r') as f:
        template_content = f.read()

    # 提取模板（去掉说明部分）
    template = extract_template(template_content)

    # 替换占位符
    optimized_request = template.replace("[在这里插入原始提示词]", original_prompt)

    # 调用 LLM
    response = call_llm(optimized_request)

    return response
```

### 方式3：自动化集成（最佳实践）

在 content-generator Skills 中自动调用：

```python
# 在生成内容前自动优化提示词
def generate_content(topic: str):
    # 1. 构建原始提示词
    original_prompt = f"生成关于{topic}的小红书文案"

    # 2. 自动优化提示词
    optimized_prompt = optimize_prompt(original_prompt, 'system')

    # 3. 使用优化后的提示词生成内容
    content = call_llm(optimized_prompt)

    return content
```

## 📊 质量保证机制

### 1. 模板版本管理

每个模板都有版本号，确保可追溯：
- v1.0: 初始版本
- v1.1: 优化XX部分
- v1.2: 修复XX问题

### 2. 使用记录

建议在使用时记录：
- 使用的模板版本
- 原始提示词
- 优化后的提示词
- 生成结果质量评分

### 3. 持续优化

根据使用效果，定期更新模板：
- 收集低质量案例
- 分析问题原因
- 更新模板内容
- 发布新版本

## ⚠️ 注意事项

### 1. 不要过度优化

**问题**：简单的提示词不需要复杂的优化
**解决**：只在需要高质量输出时使用模板

### 2. 保持原始意图

**问题**：优化后的提示词偏离原始意图
**解决**：在模板中明确要求"保持原始创意意图"

### 3. 成本控制

**问题**：每次优化都要调用 LLM，增加成本
**解决**：
- 缓存常用的优化结果
- 只在关键场景使用
- 使用更便宜的模型进行优化

## 📈 效果评估

### 评估指标

1. **结构化程度**：优化后的提示词是否更结构化
2. **完整性**：是否包含所有必要信息
3. **生成质量**：使用优化后的提示词，生成结果是否更好

### 对比测试

建议进行 A/B 测试：
- A组：使用原始提示词
- B组：使用优化后的提示词
- 对比生成结果质量

## 🔗 相关资源

- 原始项目：https://github.com/linshenkx/prompt-optimizer
- 模板来源：prompt-optimizer/packages/core/src/services/template/default-templates/
- 更新日志：见各模板文件的版本说明
