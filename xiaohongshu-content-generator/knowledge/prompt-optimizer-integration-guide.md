# Prompt Optimizer Integration Guide (Plan 3)

**版本**: v1.0.0
**创建日期**: 2026-02-05
**整合方案**: Plan 3 - 双重保障机制

## 核心理念

Plan 3 采用**三层架构**，确保生成内容的质量和稳定性：

```
用户输入
  ↓
【结构层】Prompt Template Optimization（提供标准化结构）
  ↓
【约束层】Rule Checklists（平台规范和执行规则）
  ↓
【价值层】User Examples（个性化案例和经验）
  ↓
AI 生成
  ↓
质量检查
```

### 三层架构说明

1. **结构层（Prompt Template）**
   - 来源：`_global_config/prompt-templates/`
   - 作用：提供标准化的提示词结构（Role/Profile/Skills/Rules/Workflows）
   - 优势：确保提示词的完整性和专业性

2. **约束层（Rule Checklists）**
   - 来源：`knowledge/step0-init-checklist.md`, `step5-content-checklist.md`, `step9-image-checklist.md`
   - 作用：平台规范、字数限制、格式要求、执行规则
   - 优势：确保生成内容符合平台要求

3. **价值层（User Examples）**
   - 来源：用户积累的正反面案例、个性化风格、独特经验
   - 作用：体现用户的个性化内容和独特价值
   - 优势：保持内容的独特性和用户风格

## 使用方法

### 方法1：在 Python 脚本中使用

```python
from prompt_optimizer_integration import PromptOptimizerIntegration

# 初始化整合器
optimizer = PromptOptimizerIntegration()

# 优化内容生成提示词
content_prompt = "生成一篇关于多肉植物养护的小红书笔记"
optimized_prompt = optimizer.optimize_content_prompt(
    content_prompt,
    include_checklists=['step0', 'step5']  # 包含初始化和内容检查清单
)

# 优化图像生成提示词
image_description = "一盆多肉植物放在窗台上，阳光洒在叶片上"
optimized_image_prompt = optimizer.optimize_image_prompt(
    image_description,
    include_image_checklist=True  # 包含图像检查清单
)

# 使用优化后的提示词调用 LLM
# response = call_llm(optimized_prompt)
```

### 方法2：使用便捷函数

```python
from prompt_optimizer_integration import (
    optimize_xiaohongshu_content_prompt,
    optimize_xiaohongshu_image_prompt
)

# 快速优化内容提示词
optimized_content = optimize_xiaohongshu_content_prompt(
    "生成一篇关于多肉植物养护的小红书笔记"
)

# 快速优化图像提示词
optimized_image = optimize_xiaohongshu_image_prompt(
    "一盆多肉植物放在窗台上"
)
```

### 方法3：在 Skill 中集成

在 `SKILL.md` 中添加步骤：

```markdown
### Step X: 优化提示词（使用 Plan 3 双重保障机制）

使用 Prompt Optimizer Integration 优化生成提示词：

1. 导入整合器：
   ```python
   from scripts.prompt_optimizer_integration import PromptOptimizerIntegration
   optimizer = PromptOptimizerIntegration()
   ```

2. 优化内容提示词：
   ```python
   optimized_prompt = optimizer.optimize_content_prompt(
       original_prompt,
       include_checklists=['step0', 'step5']
   )
   ```

3. 优化图像提示词：
   ```python
   optimized_image_prompt = optimizer.optimize_image_prompt(
       original_description,
       include_image_checklist=True
   )
   ```

4. 使用优化后的提示词生成内容
```

## 在可视化平台中的应用

### 后端 API 设计

```python
from flask import Flask, request, jsonify
from prompt_optimizer_integration import PromptOptimizerIntegration

app = Flask(__name__)
optimizer = PromptOptimizerIntegration()

@app.route('/api/optimize/content', methods=['POST'])
def optimize_content():
    """优化内容生成提示词"""
    data = request.json
    original_prompt = data.get('prompt')
    checklists = data.get('checklists', ['step0', 'step5'])

    optimized = optimizer.optimize_content_prompt(
        original_prompt,
        include_checklists=checklists
    )

    return jsonify({
        'success': True,
        'optimized_prompt': optimized
    })

@app.route('/api/optimize/image', methods=['POST'])
def optimize_image():
    """优化图像生成提示词"""
    data = request.json
    original_description = data.get('description')

    optimized = optimizer.optimize_image_prompt(
        original_description,
        include_image_checklist=True
    )

    return jsonify({
        'success': True,
        'optimized_prompt': optimized
    })

@app.route('/api/generate/xiaohongshu', methods=['POST'])
def generate_xiaohongshu():
    """生成小红书内容（完整工作流）"""
    data = request.json
    task_description = data.get('task')

    # Step 1: 优化提示词（Plan 3）
    optimized_prompt = optimizer.optimize_content_prompt(
        task_description,
        include_checklists=['step0', 'step5']
    )

    # Step 2: 调用 LLM 生成内容
    content = call_llm(optimized_prompt)

    # Step 3: 质量检查
    quality_check_result = perform_quality_check(content)

    return jsonify({
        'success': True,
        'content': content,
        'quality_check': quality_check_result
    })
```

### 前端调用示例

```javascript
// 优化内容提示词
async function optimizeContentPrompt(prompt) {
  const response = await fetch('/api/optimize/content', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt: prompt,
      checklists: ['step0', 'step5']
    })
  });

  const data = await response.json();
  return data.optimized_prompt;
}

// 生成小红书内容
async function generateXiaohongshu(taskDescription) {
  const response = await fetch('/api/generate/xiaohongshu', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      task: taskDescription
    })
  });

  const data = await response.json();
  return data;
}
```

## 优势分析

### 相比原方案的改进

| 维度 | 原方案 | Plan 3 |
|------|--------|--------|
| **结构化** | 依赖 AI 记忆 | 模板提供标准结构 |
| **规范性** | 14个文档分散 | 3个检查清单集中 |
| **稳定性** | 执行不稳定 | 三层保障机制 |
| **个性化** | 容易丢失 | 明确保留价值层 |
| **可维护性** | 难以更新 | 模块化易维护 |

### 解决的核心问题

1. **执行不稳定** → 三层架构确保每次执行都遵循相同流程
2. **规范分散** → 检查清单集中管理，易于查阅和更新
3. **个性化丢失** → 明确的价值层保留用户独特内容
4. **难以扩展** → 模块化设计，易于添加新平台

## 测试与验证

### 运行测试

```bash
cd /Users/dj/Desktop/小静的skills/xiaohongshu-content-generator/scripts
python3 prompt_optimizer_integration.py
```

### 预期输出

```
================================================================================
测试内容提示词优化
================================================================================
你是一个专业的AI提示词优化专家。请帮我优化以下prompt，并按照以下格式返回：

# Role: [角色名称]

## Profile
- language: [语言]
- description: [详细的角色描述]
...

## 执行规则与检查清单

**重要**: 以下规则和检查清单必须严格遵守...

### STEP0 检查清单
...

### STEP5 检查清单
...

## 个性化要求

**保留用户的个性化内容**：
- 平台规范和限制（如字数限制、格式要求）
- 正面案例参考（成功的内容示例）
...

================================================================================
测试图像提示词优化
================================================================================
请将以下描述优化为通用的自然语言图像提示词：
...
```

## 下一步计划

### 短期（本周）
- [ ] 在 xiaohongshu-content-generator 的 SKILL.md 中集成此模块
- [ ] 更新 required-reading.json，减少必读文档数量
- [ ] 测试生成内容的质量和稳定性

### 中期（本月）
- [ ] 在可视化平台中实现后端 API
- [ ] 创建前端界面调用 API
- [ ] 收集用户反馈，优化三层架构

### 长期（下季度）
- [ ] 扩展到其他平台（微信、视频号等）
- [ ] 建立质量评估体系
- [ ] 自动化学习和改进机制

## 常见问题

### Q1: 为什么要用三层架构？
A: 单一的模板或检查清单都无法同时保证结构化、规范性和个性化。三层架构分工明确，各司其职。

### Q2: 如何更新检查清单？
A: 直接编辑 `knowledge/step0-init-checklist.md` 等文件，模块会自动加载最新内容。

### Q3: 可以只用部分层吗？
A: 可以，但不推荐。三层架构是为了确保质量，缺少任何一层都会降低稳定性。

### Q4: 如何添加新的检查清单？
A: 在 `knowledge/` 目录创建新的检查清单文件，然后在 `PromptOptimizerIntegration` 类中添加对应的路径和方法。

### Q5: 这个方案适用于其他平台吗？
A: 是的。只需要为其他平台创建对应的检查清单，就可以使用相同的三层架构。

## 参考资料

- Prompt Template 来源：`_global_config/prompt-templates/QUICK-START.md`
- 检查清单：`knowledge/step0-init-checklist.md`, `step5-content-checklist.md`, `step9-image-checklist.md`
- 整合模块：`scripts/prompt_optimizer_integration.py`

---

**维护者**: Claude Code
**最后更新**: 2026-02-05
