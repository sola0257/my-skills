---
name: skill-suitability-evaluator
description: "Skill 适配性评估工具，用于判断用户任务是否适合做成 Claude Skill。当用户询问'判断一下这个任务是否适合做成skill'、'评估任务是否适合Skill'、'这个工作流能做成技能吗'、'能自动化这个任务吗'时触发。生成交互式 HTML 表单收集信息，并输出彩色卡片形式的评估结果。"
license: MIT
---

# Skill Suitability Evaluator / Skill 适配性评估器

## 🔒 静默执行协议 (Quiet Mode Protocol)

**CRITICAL EXECUTION RULES - MUST FOLLOW:**

1. **Do NOT ask for confirmation to proceed.** Execute the full workflow in one response.
2. **Generate the COMPLETE output in one go.** Never stop mid-way to ask "shall I continue?"
3. **If data is missing, use automatic inference.** Do not ask user for clarification.
4. **If output is long, continue anyway.** Do not ask "output is long, should I proceed?"
5. **Never say "I need more information".** Work with what you have.

**禁止行为示例 (Anti-Patterns to NEVER do):**
- ❌ "需要我继续吗？"
- ❌ "请问您想要...还是...？"
- ❌ "我需要更多信息来完成这个任务"
- ❌ "输出较长，是否继续？"

---

## 📋 Overview

This skill evaluates whether a user's task/workflow is suitable for becoming a Claude Skill, based on 5 key dimensions:

1. **重复性 (Repeatability)**: 任务重复做过5次以上？
2. **标准化 (Standardization)**: 输入输出有固定模式？
3. **可描述性 (Describability)**: 能用具体动词描述任务？
4. **独立性 (Independence)**: 任务相对独立，不依赖大量上下文？
5. **简洁性 (Conciseness)**: 指令可以在合理长度内写清楚？

---

## 🔄 Workflow Decision Tree

```
用户描述任务
    ↓
生成 HTML 五维度勾选表单（含补充说明输入框）
    ↓
用户提交表单 OR Claude 自动推断
    ↓
执行五维度评估
    ↓
┌─────────────────────────────────────────┐
│ 全部 YES (5/5)  → ✅ 适合做 Skill        │
│ 3-4项 YES       → ⚠️ 部分适合，需改进     │
│ ≤2项 YES        → ❌ 不适合，提供替代方案  │
└─────────────────────────────────────────┘
    ↓
输出交互式 HTML 评估结果卡片
```

---

## 📥 Step 1: Generate Input Collection Form

When user triggers this skill with a task description, **IMMEDIATELY** generate the following HTML form. Do not ask any questions first.

**Language Detection:**
- Detect user's input language
- If Chinese → Output Chinese HTML
- If English → Output English HTML
- If other/unclear → Default to Chinese

**HTML Form Template (Generate this first):**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skill 适配性评估表单</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        .header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        .card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }
        .dimension {
            background: linear-gradient(145deg, #f8f9ff 0%, #f0f4ff 100%);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .dimension:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .dimension:nth-child(1) { border-left-color: #667eea; }
        .dimension:nth-child(2) { border-left-color: #f093fb; }
        .dimension:nth-child(3) { border-left-color: #f5576c; }
        .dimension:nth-child(4) { border-left-color: #4facfe; }
        .dimension:nth-child(5) { border-left-color: #43e97b; }
        .dimension-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }
        .dimension-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            color: white;
        }
        .dimension:nth-child(1) .dimension-icon { background: linear-gradient(135deg, #667eea, #764ba2); }
        .dimension:nth-child(2) .dimension-icon { background: linear-gradient(135deg, #f093fb, #f5576c); }
        .dimension:nth-child(3) .dimension-icon { background: linear-gradient(135deg, #f5576c, #ff8a5c); }
        .dimension:nth-child(4) .dimension-icon { background: linear-gradient(135deg, #4facfe, #00f2fe); }
        .dimension:nth-child(5) .dimension-icon { background: linear-gradient(135deg, #43e97b, #38f9d7); }
        .dimension-title {
            font-weight: 600;
            font-size: 1.1rem;
            color: #2d3748;
        }
        .dimension-question {
            color: #4a5568;
            margin-bottom: 15px;
            font-size: 0.95rem;
        }
        .options {
            display: flex;
            gap: 15px;
        }
        .option {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
        }
        .option:hover {
            border-color: #667eea;
            background: #f8f9ff;
        }
        .option.yes:hover, .option.yes.selected {
            border-color: #48bb78;
            background: #f0fff4;
            color: #22543d;
        }
        .option.no:hover, .option.no.selected {
            border-color: #fc8181;
            background: #fff5f5;
            color: #742a2a;
        }
        .supplement {
            margin-top: 25px;
        }
        .supplement label {
            display: block;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 10px;
        }
        .supplement textarea {
            width: 100%;
            min-height: 100px;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1rem;
            resize: vertical;
            transition: border-color 0.2s;
        }
        .supplement textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .submit-btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            margin-top: 25px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        .task-display {
            background: #f7fafc;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            border-left: 4px solid #667eea;
        }
        .task-display strong {
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Skill 适配性评估</h1>
            <p>请根据您的任务情况，选择以下各维度的答案</p>
        </div>
        <div class="card">
            <div class="task-display">
                <strong>待评估任务：</strong>[用户描述的任务内容]
            </div>
            
            <div class="dimension">
                <div class="dimension-header">
                    <div class="dimension-icon">🔄</div>
                    <div class="dimension-title">维度一：重复性</div>
                </div>
                <div class="dimension-question">这个任务您已经重复做过 5 次以上吗？</div>
                <div class="options">
                    <div class="option yes" onclick="this.classList.toggle('selected'); this.parentElement.querySelector('.no').classList.remove('selected')">✓ 是 (Yes)</div>
                    <div class="option no" onclick="this.classList.toggle('selected'); this.parentElement.querySelector('.yes').classList.remove('selected')">✗ 否 (No)</div>
                </div>
            </div>

            <div class="dimension">
                <div class="dimension-header">
                    <div class="dimension-icon">📐</div>
                    <div class="dimension-title">维度二：标准化</div>
                </div>
                <div class="dimension-question">任务的输入和输出有固定的模式/格式吗？</div>
                <div class="options">
                    <div class="option yes" onclick="this.classList.toggle('selected'); this.parentElement.querySelector('.no').classList.remove('selected')">✓ 是 (Yes)</div>
                    <div class="option no" onclick="this.classList.toggle('selected'); this.parentElement.querySelector('.yes').classList.remove('selected')">✗ 否 (No)</div>
                </div>
            </div>

            <div class="dimension">
                <div class="dimension-header">
                    <div class="dimension-icon">📝</div>
                    <div class="dimension-title">维度三：可描述性</div>
                </div>
                <div class="dimension-question">能用具体的动词来描述这个任务吗？（如：提取、生成、转换、分析）</div>
                <div class="options">
                    <div class="option yes" onclick="this.classList.toggle('selected'); this.parentElement.querySelector('.no').classList.remove('selected')">✓ 是 (Yes)</div>
                    <div class="option no" onclick="this.classList.toggle('selected'); this.parentElement.querySelector('.yes').classList.remove('selected')">✗ 否 (No)</div>
                </div>
            </div>

            <div class="dimension">
                <div class="dimension-header">
                    <div class="dimension-icon">🧩</div>
                    <div class="dimension-title">维度四：独立性</div>
                </div>
                <div class="dimension-question">任务相对独立，不需要依赖大量外部上下文信息？</div>
                <div class="options">
                    <div class="option yes" onclick="this.classList.toggle('selected'); this.parentElement.querySelector('.no').classList.remove('selected')">✓ 是 (Yes)</div>
                    <div class="option no" onclick="this.classList.toggle('selected'); this.parentElement.querySelector('.yes').classList.remove('selected')">✗ 否 (No)</div>
                </div>
            </div>

            <div class="dimension">
                <div class="dimension-header">
                    <div class="dimension-icon">📏</div>
                    <div class="dimension-title">维度五：简洁性</div>
                </div>
                <div class="dimension-question">任务的指令可以在合理长度内写清楚吗？（不需要超长文档）</div>
                <div class="options">
                    <div class="option yes" onclick="this.classList.toggle('selected'); this.parentElement.querySelector('.no').classList.remove('selected')">✓ 是 (Yes)</div>
                    <div class="option no" onclick="this.classList.toggle('selected'); this.parentElement.querySelector('.yes').classList.remove('selected')">✗ 否 (No)</div>
                </div>
            </div>

            <div class="supplement">
                <label>📎 补充说明（可选）</label>
                <textarea placeholder="如果有任何需要补充的信息，请在此填写..."></textarea>
            </div>

            <button class="submit-btn">🚀 提交评估</button>
        </div>
    </div>
</body>
</html>
```

---

## 📤 Step 2: Process Input & Generate Result

After user provides their selections (or if they skip, use auto-inference based on task description):

### Inference Rules (When User Doesn't Select)

| Dimension | Auto-Inference Logic |
|-----------|---------------------|
| 重复性 | If task sounds routine/common → YES; If sounds novel/one-time → NO |
| 标准化 | If mentions specific formats (JSON, CSV, template) → YES |
| 可描述性 | If contains action verbs (提取/生成/转换/分析/create/extract) → YES |
| 独立性 | If self-contained logic described → YES; If mentions "depends on context" → NO |
| 简洁性 | If describable in < 50 words → YES |

### Evaluation Logic

```
score = count of YES answers

if score == 5:
    result = "✅ 适合做 Skill"
    color_theme = "green"
elif score >= 3:
    result = "⚠️ 部分适合"
    color_theme = "orange"
else:
    result = "❌ 不适合"
    color_theme = "red"
```

---

## 📊 Step 3: Output Result HTML

**Generate the complete result HTML based on evaluation. Include:**

1. **Overall Result Card** - Large header with result status
2. **Five Dimension Cards** - Color-coded (green=YES, red=NO)
3. **Recommendations Section** - Based on result type
4. **Alternative Solutions** - If NOT suitable, provide detailed guides

### Result HTML Template Structure:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skill 适配性评估结果</title>
    <style>
        /* [Include comprehensive CSS for colorful card design] */
        /* Success: Green gradients */
        /* Partial: Orange/Yellow gradients */  
        /* Not Suitable: Red gradients */
        /* Each dimension card with pass/fail indicator */
        /* Collapsible sections for alternative guides */
    </style>
</head>
<body>
    <!-- RESULT HEADER -->
    <div class="result-header [success/partial/fail]">
        <div class="result-icon">[✅/⚠️/❌]</div>
        <h1>[评估结果标题]</h1>
        <p class="score">综合得分：[X]/5</p>
    </div>

    <!-- DIMENSION BREAKDOWN -->
    <div class="dimensions-grid">
        <!-- 5 dimension cards with YES/NO status -->
    </div>

    <!-- RECOMMENDATIONS -->
    <div class="recommendations">
        <!-- Contextual advice based on result -->
    </div>

    <!-- ALTERNATIVE SOLUTIONS (if not suitable) -->
    <div class="alternatives">
        <!-- Detailed operation guides -->
    </div>
</body>
</html>
```

---

## 📋 Alternative Solutions Guide (When NOT Suitable)

When a dimension is NO, include the corresponding solution:

| NO Dimension | Solution Title | Detailed Operation Guide |
|--------------|---------------|--------------------------|
| 重复性不足 | 暂时不需要 Skill | 1. 记录每次执行任务的情况<br>2. 等待任务出现5次以上<br>3. 识别重复模式后再考虑创建 Skill |
| 标准化不足 | 先梳理输入输出规范 | 1. 列出所有可能的输入类型<br>2. 定义统一的输出模板<br>3. 创建示例输入→输出映射表<br>4. 验证模板覆盖80%以上场景 |
| 描述不清晰 | 重新定义任务边界 | 1. 使用格式："[动词] + [对象] + [结果]"<br>2. 例如："提取PDF中的表格并转为CSV"<br>3. 避免模糊词如"处理"、"优化" |
| 上下文依赖 | 考虑拆分任务 | 1. 识别任务中的独立子模块<br>2. 每个子模块应能独立执行<br>3. 为每个子模块创建单独的 Skill<br>4. 用菜单式结构串联多个 Skill |
| 指令过长 | 使用 Menu Approach | 1. 主文件只包含概述和导航<br>2. 详细指令拆分到子文件<br>3. 使用相对路径引用<br>4. Claude 按需读取相关文件 |

---

## ✅ Few-Shot Examples

### ✅ GOOD Example (One-Shot Completion)

**User Input:**
> 判断一下这个任务是否适合做成skill：每天从Slack频道提取客户反馈，整理成表格

**Claude Output:**
```
[直接输出完整的HTML表单界面，无任何询问]

...完整HTML代码...
```

**After User Submits Form (or Auto-Inference):**
```
[直接输出完整的评估结果HTML，无任何询问]

...完整HTML结果代码...
```

### ❌ ANTI-PATTERN (NEVER Do This)

**User Input:**
> 判断一下这个任务是否适合做成skill：数据分析

**Wrong Response (FORBIDDEN):**
```
❌ "我需要更多信息。请问：
1. 您具体是做什么类型的数据分析？
2. 输入是什么格式？
3. 预期输出是什么？

请提供更多细节，我才能进行评估。"
```

**Correct Response:**
```
[即使信息不足，也直接生成表单HTML]
[在表单中标注"信息待补充"，让用户通过表单选择来提供信息]
[绝不停下来询问]
```

---

## 🎯 Triggering Conditions

**ACTIVATE when user says:**
- "判断一下这个任务是否适合做成skill"
- "评估任务是否适合Skill"
- "这个工作流能做成技能吗"
- "能自动化这个任务吗"
- "帮我看看这个适不适合做Skill"
- "Evaluate if this task is suitable for a Skill"

**DO NOT ACTIVATE when:**
- User asks "什么是Skill？" (definition question, not evaluation)
- User asks "怎么创建Skill？" (creation guide, not evaluation)
- User is already creating a Skill (use other skills)

---

## 🔧 Error Handling

| Scenario | Silent Handling |
|----------|----------------|
| Task description < 10 chars | Generate form anyway, mark as "低置信度评估" |
| User provides no selections | Auto-infer all 5 dimensions from description |
| Language unclear | Default to Chinese |
| Conflicting info | Prioritize explicit user selections over inference |

---

## 📄 Output Format Rules

1. **Always output valid, complete HTML** - Never partial code
2. **Inline all CSS** - No external stylesheets
3. **Include all interactive JS** - No external scripts
4. **Self-contained** - HTML should work when saved as .html file
5. **Mobile responsive** - Include viewport meta and responsive CSS
