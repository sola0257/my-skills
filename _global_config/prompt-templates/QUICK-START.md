# Prompt 优化模板系统 - 快速开始指南

> **来源**: 基于 [prompt-optimizer](https://github.com/linshenkx/prompt-optimizer) 开源项目提取
> **更新**: 2026-02-05
> **核心原理**: 模板驱动的 Prompt 优化（非算法）

---

## 📁 目录结构

```
_global_config/prompt-templates/
├── QUICK-START.md              # 本文件 - 快速开始指南
├── text-optimize/              # 文本 Prompt 优化
│   └── system-prompt-general.md
├── image-optimize/             # 图片 Prompt 优化
│   └── image-prompt-general.md
└── docs/                       # 详细文档
    ├── README.md               # 完整使用指南
    └── template-selection-guide.md  # 模板选择指南
```

---

## 🚀 30秒快速使用

### 场景1: 优化文本内容生成 Prompt

**原始 Prompt**:
```
生成一篇关于多肉植物养护的小红书笔记
```

**使用模板优化**:
```python
# 读取模板
template_path = "_global_config/prompt-templates/text-optimize/system-prompt-general.md"
template = read_file(template_path)

# 替换变量
optimized_prompt = template.replace("{{originalPrompt}}", "生成一篇关于多肉植物养护的小红书笔记")

# 使用优化后的 Prompt
result = call_llm(optimized_prompt)
```

**优化效果**:
- ✅ 结构化输出（标题、正文、标签）
- ✅ 符合平台规范（字数、格式）
- ✅ 包含必要元素（痛点、解决方案、行动建议）

---

### 场景2: 优化图片生成 Prompt

**原始 Prompt**:
```
一只熊猫在竹林里
```

**使用模板优化**:
```python
# 读取模板
template_path = "_global_config/prompt-templates/image-optimize/image-prompt-general.md"
template = read_file(template_path)

# 替换变量
optimized_prompt = template.replace("[在这里插入原始提示词]", "一只熊猫在竹林里")

# 使用优化后的 Prompt
image = generate_image(optimized_prompt)
```

**优化效果**:
```
主体与动作：一只成年大熊猫，正坐在竹林中，双手抱着新鲜的竹子，专注地啃食着
环境与空间：茂密的竹林，阳光透过竹叶洒下斑驳的光影
光线与时间：清晨的柔和阳光，营造出宁静祥和的氛围
色彩与材质：熊猫黑白分明的毛发，翠绿的竹叶，温暖的阳光色调
氛围与风格：自然纪实摄影风格，真实生动，充满生命力
构图与视角：中景，平视角度，突出熊猫与竹林的和谐共处
```

---

## 📊 模板选择决策表

| 任务类型 | 使用模板 | 适用场景 |
|---------|---------|---------|
| **文本内容生成** | `text-optimize/system-prompt-general.md` | 小红书笔记、公众号文章、视频脚本 |
| **图片生成** | `image-optimize/image-prompt-general.md` | 配图生成、封面设计、插画创作 |
| **知识提取** | `text-optimize/system-prompt-general.md` | 文档整理、方法论提取、知识汇总 |

---

## 🔧 三种集成方式

### 方式1: 直接在 Skill 中使用（推荐）

**适用场景**: 内容生成类 Skills（xiaohongshu-content-generator, wechat-content-generator）

**实现方式**:
```markdown
# 在 SKILL.md 的 Step 3: 生成文案 中添加

## Step 3.1: 优化 System Prompt（新增）

读取模板：
`/Users/dj/Desktop/小静的skills/_global_config/prompt-templates/text-optimize/system-prompt-general.md`

替换变量：
- {{originalPrompt}} → 当前任务的原始 Prompt
- {{platform}} → 目标平台（小红书/公众号/视频号）
- {{contentType}} → 内容类型（养护指南/产品推荐/知识科普）

使用优化后的 Prompt 调用 LLM
```

---

### 方式2: Python 脚本集成

**适用场景**: 批量内容生成、自动化工作流

**示例代码**:
```python
import os
from pathlib import Path

def optimize_prompt(original_prompt: str, template_type: str = "text") -> str:
    """
    使用模板优化 Prompt

    Args:
        original_prompt: 原始 Prompt
        template_type: 模板类型 ("text" 或 "image")

    Returns:
        优化后的 Prompt
    """
    # 读取模板
    base_path = Path("/Users/dj/Desktop/小静的skills/_global_config/prompt-templates")

    if template_type == "text":
        template_path = base_path / "text-optimize/system-prompt-general.md"
    elif template_type == "image":
        template_path = base_path / "image-optimize/image-prompt-general.md"
    else:
        raise ValueError(f"Unknown template type: {template_type}")

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # 替换变量
    optimized = template.replace("{{originalPrompt}}", original_prompt)
    optimized = optimized.replace("[在这里插入原始提示词]", original_prompt)

    return optimized

# 使用示例
original = "生成一篇关于多肉植物养护的小红书笔记"
optimized = optimize_prompt(original, template_type="text")
print(optimized)
```

---

### 方式3: 自动化集成（Hook 触发）

**适用场景**: 全局自动优化所有 Prompt

**实现方式**:
1. 在 `~/.claude/hooks/` 创建 `prompt-optimizer.sh`
2. 检测到内容生成任务时自动应用模板
3. 无需手动调用，完全自动化

**Hook 示例**:
```bash
#!/bin/bash
# 检测到内容生成关键词时自动优化 Prompt
if echo "$PROMPT" | grep -E "(生成|创建|写一篇)" > /dev/null; then
    python3 /path/to/optimize_prompt.py "$PROMPT"
fi
```

---

## ✅ 质量保证机制

### 1. 模板验证清单

使用模板前，确保：
- [ ] 已读取正确的模板文件
- [ ] 已替换所有变量占位符
- [ ] 优化后的 Prompt 结构完整
- [ ] 包含必要的约束条件

### 2. 输出质量检查

生成内容后，检查：
- [ ] 是否符合平台规范（字数、格式）
- [ ] 是否包含必要元素（标题、正文、标签）
- [ ] 是否有明确的价值输出
- [ ] 是否通过违禁词检查

### 3. 持续优化

- 记录优化效果（生成质量、用户反馈）
- 定期更新模板（基于实际使用效果）
- 扩展模板库（新增平台、新增场景）

---

## 📚 进阶阅读

- **完整使用指南**: `docs/README.md`
- **模板选择指南**: `docs/template-selection-guide.md`
- **文本优化模板**: `text-optimize/system-prompt-general.md`
- **图片优化模板**: `image-optimize/image-prompt-general.md`

---

## 🎯 实战案例

### 案例1: 小红书笔记生成

**任务**: 生成一篇关于"多肉植物夏季养护"的小红书笔记

**执行流程**:
1. 读取 `text-optimize/system-prompt-general.md`
2. 替换变量:
   - `{{originalPrompt}}` → "生成一篇关于多肉植物夏季养护的小红书笔记"
   - `{{platform}}` → "小红书"
   - `{{contentType}}` → "养护指南"
3. 使用优化后的 Prompt 调用 LLM
4. 生成结构化内容（标题、正文、标签）
5. 应用违禁词检查
6. 生成配图（使用 `image-optimize/image-prompt-general.md`）

**结果**:
- ✅ 标题吸引人（"多肉夏季养护3大误区，90%的人都踩坑了！"）
- ✅ 正文结构清晰（痛点 → 解决方案 → 行动建议）
- ✅ 配图真实自然（使用优化后的图片 Prompt）
- ✅ 通过违禁词检查

---

### 案例2: 公众号文章生成

**任务**: 生成一篇关于"室内绿植选择"的公众号文章

**执行流程**:
1. 读取 `text-optimize/system-prompt-general.md`
2. 替换变量:
   - `{{originalPrompt}}` → "生成一篇关于室内绿植选择的公众号文章"
   - `{{platform}}` → "微信公众号"
   - `{{contentType}}` → "选购指南"
3. 使用优化后的 Prompt 调用 LLM
4. 生成深度内容（2000-3000字）
5. 生成配图（封面 + 正文配图）

**结果**:
- ✅ 内容深度足够（2500字）
- ✅ 结构完整（引言 → 正文 → 总结）
- ✅ 配图专业（封面 2.35:1，正文 16:9）
- ✅ 可读性强（分段清晰，小标题明确）

---

## 🔄 版本历史

- **v1.0** (2026-02-05): 初始版本
  - 提取 prompt-optimizer 核心模板
  - 创建文本优化和图片优化模板
  - 建立模板选择决策系统
  - 提供三种集成方式

---

## 💡 常见问题

### Q1: 模板和算法有什么区别？

**A**:
- **模板**: 预定义的结构化 Prompt，通过变量替换实现定制化
- **算法**: 基于规则或机器学习的动态优化逻辑

本系统使用**模板驱动**的方式，优势是：
- ✅ 可控性强（输出结果可预测）
- ✅ 易于维护（直接修改模板文件）
- ✅ 无需训练（即改即用）

### Q2: 如何选择合适的模板？

**A**: 参考 `docs/template-selection-guide.md` 中的决策树：
- 文本内容生成 → `text-optimize/system-prompt-general.md`
- 图片生成 → `image-optimize/image-prompt-general.md`
- 知识提取 → `text-optimize/system-prompt-general.md`

### Q3: 可以自定义模板吗？

**A**: 可以！
1. 复制现有模板作为基础
2. 根据具体需求修改结构和约束
3. 保存到对应目录（`text-optimize/` 或 `image-optimize/`）
4. 更新 `docs/template-selection-guide.md` 添加新模板的使用说明

### Q4: 模板优化效果如何验证？

**A**: 建议使用 A/B 测试：
1. 生成两组内容（使用模板 vs 不使用模板）
2. 对比质量指标（结构完整性、内容深度、平台规范符合度）
3. 记录用户反馈（阅读量、互动率）
4. 持续优化模板

---

## 📞 支持与反馈

如有问题或建议，请：
1. 查阅 `docs/README.md` 获取详细文档
2. 检查 `docs/template-selection-guide.md` 确认模板选择
3. 查看实战案例了解最佳实践

---

**最后更新**: 2026-02-05
**维护者**: Claude Code
**来源项目**: [prompt-optimizer](https://github.com/linshenkx/prompt-optimizer)
```
