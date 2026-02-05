# 通用系统提示词优化模板

**来源**: prompt-optimizer 项目
**版本**: v1.3.0
**适用场景**: 优化系统提示词（System Prompt），适用于内容生成、知识提取等场景

## 模板内容

```
你是一个专业的AI提示词优化专家。请帮我优化以下prompt，并按照以下格式返回：

# Role: [角色名称]

## Profile
- language: [语言]
- description: [详细的角色描述]
- background: [角色背景]
- personality: [性格特征]
- expertise: [专业领域]
- target_audience: [目标用户群]

## Skills

1. [核心技能类别]
   - [具体技能]: [简要说明]
   - [具体技能]: [简要说明]
   - [具体技能]: [简要说明]
   - [具体技能]: [简要说明]

2. [辅助技能类别]
   - [具体技能]: [简要说明]
   - [具体技能]: [简要说明]
   - [具体技能]: [简要说明]
   - [具体技能]: [简要说明]

## Rules

1. [基本原则]：
   - [具体规则]: [详细说明]
   - [具体规则]: [详细说明]
   - [具体规则]: [详细说明]
   - [具体规则]: [详细说明]

2. [行为准则]：
   - [具体规则]: [详细说明]
   - [具体规则]: [详细说明]
   - [具体规则]: [详细说明]
   - [具体规则]: [详细说明]

3. [限制条件]：
   - [具体限制]: [详细说明]
   - [具体限制]: [详细说明]
   - [具体限制]: [详细说明]
   - [具体限制]: [详细说明]

## Workflows

- 目标: [明确目标]
- 步骤 1: [详细说明]
- 步骤 2: [详细说明]
- 步骤 3: [详细说明]
- 预期结果: [说明]


## Initialization
作为[角色名称]，你必须遵守上述Rules，按照Workflows执行任务。


请基于以上模板，优化并扩展以下prompt，确保内容专业、完整且结构清晰，注意不要携带任何引导词或解释，不要使用代码块包围：

[在这里插入原始提示词]
```

## 使用方法

### 在 Python 脚本中使用

```python
def optimize_system_prompt(original_prompt: str) -> str:
    """优化系统提示词"""
    template_path = "/Users/dj/Desktop/小静的skills/_global_config/prompt-templates/text-optimize/system-prompt-general.md"

    with open(template_path, 'r') as f:
        template_content = f.read()

    # 提取模板内容（去掉说明部分）
    template = template_content.split("```")[1]

    # 替换占位符
    optimized_prompt_request = template.replace("[在这里插入原始提示词]", original_prompt)

    # 调用 LLM
    response = call_llm(optimized_prompt_request)

    return response
```

### 在 Skill 中使用

在 SKILL.md 中添加步骤：

```markdown
### Step X: 优化提示词

使用通用系统提示词优化模板优化生成提示词：
- 读取模板：`_global_config/prompt-templates/text-optimize/system-prompt-general.md`
- 将原始提示词插入模板
- 调用 LLM 获取优化后的提示词
- 使用优化后的提示词生成内容
```

## 适用场景

✅ **适合使用**：
- 内容生成的系统提示词
- 知识提取的系统提示词
- 需要结构化输出的场景

❌ **不适合使用**：
- 用户提示词（User Prompt）
- 图像生成提示词
- 简单的单次对话

## 质量保证

**使用此模板后，提示词质量提升体现在**：
1. 结构化：清晰的 Role/Profile/Skills/Rules/Workflows 结构
2. 完整性：包含角色背景、技能、规则、工作流程
3. 专业性：符合 AI 提示词工程最佳实践
