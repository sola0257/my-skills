# **Agentic AI开发环境中的不稳定性溯源与架构迁移研究报告：从模型特性到跨平台规则移植**

## **1\. 绪论：Agentic AI 开发范式的演进与挑战**

2026年初，随着大语言模型（LLM）能力的飞跃，软件工程领域正经历一场从“辅助编码”（Copilot）向“自主代理开发”（Agentic Development）的范式转移。这一转变的核心在于将AI的角色从一个被动的代码补全工具，提升为一个能够感知环境、规划任务、执行操作并自我修正的智能主体。在此背景下，Google推出的“Anti-Gravity”（反重力）IDE与Anthropic的Claude Code CLI代表了两种截然不同的技术路线：前者试图构建一个全知全能的图形化集成环境，后者则致力于在终端命令行中通过极简的接口实现深度的工具链整合 1。

然而，随着实践的深入，开发者普遍遭遇了“技能不稳定性”（Skill Instability）的瓶颈。这种不稳定性表现为代理在执行复杂任务时陷入逻辑死循环、忽略显式指令、上下文丢失，甚至产生破坏性操作。本报告旨在从底层模型特性（Claude 3.5/4.5 Sonnet/Opus Thinking 与 Gemini 3 Pro）、信息架构设计（Markdown与Knowledge文件结构），以及规则引擎机制（Anti-Gravity Rules）三个维度，对这一现象进行详尽的病理学分析。同时，报告将重点探讨如何在脱离Google生态的情况下，将“Anti-Gravity”中高效的Rules规则机制，通过Model Context Protocol (MCP) 和系统提示词工程，移植到更加灵活的Terminal Claude CLI环境中，以构建一个既具备高度稳定性又拥有强大约束力的混合开发架构。

## **2\. 模型特性与不稳定性深度分析：Gemini 3 Pro 与 Claude Thinking 的博弈**

Agentic AI的核心在于其“思考”能力，即在执行动作之前进行内部推理（Reasoning）的过程。然而，Google与Anthropic在实现这一能力时采用了根本不同的架构策略，导致了截然不同的故障模式。

### **2.1 Gemini 3 Pro：推理算力的“同类相食”与递归死循环**

Gemini 3 Pro 被Google定位为最强的Agentic模型，具备100万token的上下文窗口和原生的多模态能力 3。然而，在实际的开发场景中，特别是结合Antigravity IDE使用时，该模型表现出了极高的不稳定性，主要体现为“推理循环”和“输出截断”。

#### **2.1.1 共享Token预算的架构缺陷**

Gemini 3 Pro 的一个关键架构特征是其“思考过程”（Thinking Process）与“最终响应”（Final Response）共享同一个输出Token预算（max\_output\_tokens）。这种设计在资源受限的环境下导致了严重的“同类相食”（Cannibalization）效应 5。  
当用户下达一个复杂的重构指令（例如：“重构整个认证模块并更新所有引用”）时，模型需要进行大量的内部推理来规划路径。如果系统设置（或默认）的推理预算较紧（例如“Low” Reasoning Setting），模型会试图压缩其思维链。然而，一旦推理过程超出了预设的隐性阈值，或者模型陷入了对某个依赖项的反复确认中，推理token就会大量挤占原本预留给代码生成的token空间。  
其结果是，用户看到的并不是一个深思熟虑的答案，而是一个在逻辑上看似合理但在执行上突然中断的代码块，或者是一个只有注释没有实现的空函数 5。更严重的是，当Token耗尽导致输出截断时，Agent往往无法正确感知任务已失败，而是在下一轮对话中基于截断的输出来继续推理，从而产生“幻觉链条”。

#### **2.1.2 温度敏感性与死循环机制**

与Gemini 2.5或GPT-4不同，Gemini 3 Pro对温度（Temperature）参数表现出极端的敏感性。Google官方建议将Gemini 3的温度保持在默认的1.0，因为其推理引擎是针对高熵值环境优化的 6。  
在Antigravity环境中，如果开发者为了追求代码的确定性而人为降低温度（例如设为0.2），Gemini 3 Pro的推理模块往往会陷入“确定性陷阱”。模型在面对一个具有多义性的代码路径时，由于缺乏足够的随机性来探索替代方案，会反复生成完全相同的错误推理路径，导致IDE中的Agent陷入无限的“Thinking”状态，直到超时 7。这种现象被社区称为“逻辑死锁”（Reasoning Deadlock），其本质是模型的自我验证机制在低温度下失效，无法跳出局部最优解。

#### **2.1.3 上下文饱和导致的指令漂移**

尽管Gemini 3 Pro宣称拥有1M的上下文窗口，但在实际的Agentic工作流中，信息的“密度”远比“长度”重要。Antigravity IDE倾向于将整个文件树、Git历史和依赖图一次性注入上下文 8。这种策略导致了“上下文饱和”（Context Saturation）。  
在高饱和状态下，Gemini 3 Pro表现出明显的“首因效应”消退，即模型开始遗忘最早设定的全局规则（Global Rules），而过度关注最近的文件变更。这解释了为何在长会话中，Agent会突然开始违反项目编码规范，或者使用已经被废弃的API 9。这种不稳定性并非模型能力不足，而是信息架构设计上的过载导致的注意力分散。

### **2.2 Claude Sonnet/Opus 4.5：确定性状态追踪与“惰性”防御**

相比之下，Anthropic的Claude 4.5系列（尤其是Opus 4.5）展现出了截然不同的行为特征。Claude模型引入了明确的effort参数（Low, Medium, High）来控制思考深度，并且在架构上似乎对推理流进行了更严格的分层管理 10。

#### **2.2.1 状态持久化与长程推理**

Claude 4.5最显著的优势在于其“状态追踪”（State Tracking）能力。在涉及多文件、多步骤的任务中，Claude Opus能够构建并维护一个稳定的项目心理模型（Mental Model）11。这意味着即使在上下文窗口不断滚动的过程中，模型依然能“记住”之前的决策点。  
这种稳定性来源于Claude的“扩展思考”（Extended Thinking）机制。与Gemini的黑盒推理不同，Claude的思考过程往往是显式的，并且可以交织在工具调用之间（Interleaved Thinking）10。例如，模型可以先运行一个grep命令，根据输出进行一轮思考，再决定是修改代码还是继续搜索。这种“想-做-想”的循环大大降低了单次推理错误的累积风险。

#### **2.2.2 “反重力”下的刚性与惰性**

然而，Claude的稳定性也带来了一定的副作用：刚性（Rigidity）。当通过CLAUDE.md或Prompt注入了严格的规则后，Claude 4.5往往表现出一种“过度纠正”的倾向。如果规则稍微过时，或者与当前任务有轻微冲突，模型可能会直接拒绝执行，而不是尝试变通 12。  
此外，Claude模型在处理重复性任务时容易表现出“省流模式”的惰性（Laziness）。为了节省Token（也是为了响应速度），模型可能会跳过详细的解释，直接输出代码差异（Diff）。虽然这对资深开发者是好事，但在需要Agent进行自我审查（Self-Reflection）的场景下，省略中间的思考步骤可能导致潜在的逻辑漏洞被掩盖 11。

#### **2.2.3 性能与延迟的权衡**

从延迟角度看，Claude的“思考”是昂贵的。启用Extended Thinking会导致响应时间显著增加，这在实时交互的IDE（如Antigravity）中可能是不可接受的，但在异步的CLI环境中（如Claude Code）则是可行的。这种延迟与质量的权衡，使得Claude更适合作为“架构师”进行深思熟虑的重构，而Gemini更适合作为“补全者”进行快速的代码生成 13。

### **2.3 数据对比：模型在Agentic任务中的表现特征**

下表总结了两种模型在关键Agentic指标上的对比分析：

| 维度 | Gemini 3 Pro (Antigravity环境) | Claude 4.5 Sonnet/Opus (CLI环境) | 稳定性影响分析 |
| :---- | :---- | :---- | :---- |
| **推理架构** | 共享Token预算 (Reasoning/Output) | 独立/参数化思考深度 (effort param) | Gemini易因预算冲突导致截断；Claude更可控。 |
| **温度偏好** | 严格 1.0 | 灵活 (0.5-1.0) | Gemini在低温下易死循环；Claude适应性更强。 |
| **上下文管理** | 激进加载 (全量上下文) | 选择性加载 (基于相关性) | Gemini易患“上下文腐烂”；Claude通过工具检索保持聚焦。 |
| **错误恢复** | 弱 (倾向于坚持错误路径) | 强 (通过Interleaved Thinking自我修正) | Claude能中途纠错；Gemini往往需要重置会话。 |
| **指令遵循** | 概率性 (受最近上下文干扰) | 确定性 (严格遵循System Prompt) | Claude更适合执行严格的Rule/Spec。 |

## **3\. 信息架构的决定性作用：Markdown结构与辅助文件设计**

AI Agent并非魔法，其表现高度依赖于输入信息的结构化程度。研究表明，Markdown文档的层级结构、知识文件的分离设计（Knowledge Separation），以及脚本的黑盒化处理，是决定Skill稳定性的关键变量。

### **3.1 Markdown 的认知可解析性（Cognitive Parsability）**

Markdown之所以成为Agent指令的标准语言，不仅是因为其简洁，更是因为其结构与LLM训练数据的内在一致性。

#### **3.1.1 标题即边界**

在设计SKILL.md时，Markdown标题（Header，如 \#\#, \#\#\#）起到了“注意力锚点”（Attention Anchor）的作用。研究发现，当指令被清晰的H2/H3标题包裹时，模型检索和遵循指令的准确率显著高于扁平的文本段落 15。  
例如，将“错误处理”作为一个独立的 \#\# Error Handling 章节，比将其混杂在 \#\# Description 中更能确保模型在遇到异常时触发相应的逻辑。这是因为Transformer架构的自注意力机制能够更有效地捕捉到层级结构带来的语义边界。

#### **3.1.2 列表的程序化暗示**

使用无序列表（- item）或有序列表（1. step）对模型具有强烈的“程序化暗示”。对于Agent而言，有序列表被隐式编码为“必须按顺序执行的步骤”，而段落文本则更多被处理为“背景信息” 17。因此，在编写Workflow规则时，强制使用有序列表是防止步骤跳跃（Step Skipping）的最有效手段。

### **3.2 SKILL.md 的解剖学：构建稳健技能的标准范式**

一个高稳定性的Skill文件不应仅仅是自然语言的描述，而应具备严格的工程结构。Antigravity与Claude CLI社区已经形成了一套最佳实践标准 18。

#### **3.2.1 元数据（Frontmatter）的路由作用**

SKILL.md 顶部的YAML Frontmatter 是Agent的“路由表”。

YAML

**\---**  
name: database-migration-handler  
description: Handles all database schema changes. Use this skill WHENEVER the user asks to modify tables, columns, or indexes. DO NOT use for simple data selection.  
**\---**

其中的 description 字段至关重要。它必须使用**第三人称**描述，并包含**触发关键词**（Trigger Keywords）18。模糊的描述会导致Agent在不恰当的时候调用技能，或者在需要时忽略技能。必须明确“何时用”以及“何时不用”（Negative Constraints）。

#### **3.2.2 渐进式披露（Progressive Disclosure）**

为了对抗上下文饱和，Skill的设计应遵循“渐进式披露”原则。SKILL.md 本身应保持轻量（建议500行以内），仅包含高层逻辑和决策树。具体的API文档、长篇的规范说明应放入 references/ 子目录，并通过链接引用。  
这种设计迫使Agent在“加载技能”和“深入阅读”之间建立一个决策点。只有当Agent确信需要查阅API细节时，才会读取 references/api-docs.md，从而节省了宝贵的上下文窗口 8。

### **3.3 脚本与知识的分离：黑盒化（Black-Boxing）策略**

将逻辑封装在脚本中，而不是用自然语言描述逻辑，是提升Agent稳定性的终极手段。

#### **3.3.1 确定性执行 vs. 概率性生成**

如果任务是“检查数据库中是否有重复用户”，让LLM编写并执行SQL存在极大的不确定性（幻觉、语法错误）。最佳实践是在 scripts/ 目录下编写一个 check\_duplicates.py 脚本，并在 SKILL.md 中指示Agent调用该脚本.8  
这种策略将“怎么做”（How）的复杂性从LLM的概率空间转移到了代码的确定性空间，Agent只需负责“做什么”（What）。

#### **3.3.2 接口标准化**

脚本应具备清晰的 \--help 接口。Agent被训练为优先阅读工具的帮助文档。通过让Agent调用 python scripts/tool.py \--help，模型可以快速获得准确的使用方法，而无需阅读脚本源码，从而进一步降低Token消耗 20。

## **4\. “Anti-Gravity” Rules 机制解析：IDE层面的上下文注入**

Google Antigravity 的核心竞争力之一在于其强大的 Rules 系统。这不仅仅是一组文档，而是一个动态的上下文注入引擎。

### **4.1 .agent/rules 的文件系统架构**

Antigravity 的规则存储在 .agent/rules 目录中。这些规则文件（Markdown格式）并非全部同时生效，而是由IDE根据当前上下文动态筛选 22。

#### **4.1.1 触发机制分类**

* **Always On（常驻）：** 这些规则的内容会被无条件地追加到System Prompt中。通常用于最高优先级的安全策略（如“严禁硬编码密码”）22。  
* **Manual（手动）：** 类似于宏命令，只有当用户在对话中显式 @mention 时才加载。  
* **Model Decision（模型决策）：** 这是最智能的部分。IDE会先使用一个小模型（如Gemini Flash）扫描用户的Prompt和规则的 description，判断相关性。如果相关，则将规则全文注入上下文。  
* **Glob Pattern（文件路径匹配）：** 基于文件扩展名或路径触发。例如，当用户打开一个 .ts 文件时，typescript-rules.md 会自动生效 22。

#### **4.1.2 引用与组合**

规则文件支持 @file 引用语法。例如，一个规则文件可以包含 @/docs/coding-style.md。Antigravity 引擎会在注入Prompt之前解析这些引用，将目标文件的内容内联进来 22。这种组合能力允许规则复用现有的项目文档。

### **4.2 生效机制：Prompt 组装流水线**

当用户在Antigravity中发送消息时，后台发生的过程如下：

1. **Context Analysis:** IDE分析当前打开的文件列表（Active Set）。  
2. **Rule Resolution:**  
   * 匹配 Glob 模式 \-\> 加载相关规则。  
   * 运行相关性分类器 \-\> 加载 Model Decision 规则。  
   * 加载 Always On 规则。  
3. **Prompt Construction:** 将所有选中的规则按照优先级顺序拼接，形成一个巨大的 System Prompt 前缀。  
4. **Inference:** 将拼接后的Prompt发送给 Gemini 3 Pro。

这种机制的优点是上下文利用率极高，缺点是极其依赖IDE本身的逻辑。一旦离开Antigravity环境（例如进入纯终端），这套复杂的注入机制就会失效。这正是移植工作的难点所在。

## **5\. 跨平台移植研究：在 Terminal Claude CLI 中重构 Rules 系统**

Terminal Claude CLI（即 claude-code）是一个轻量级的、以终端为中心的工具，它没有Antigravity那样复杂的后台守护进程来管理规则的动态注入。然而，通过巧妙利用 MCP 协议和 System Prompt 配置，我们可以在 CLI 环境中复刻甚至超越 Antigravity 的规则体验。

### **5.1 CLAUDE.md：静态规则的基石**

Antigravity 的 “Always On” 规则可以直接映射到 Claude CLI 的 CLAUDE.md 文件。

#### **5.1.1 移植策略**

* **位置：** 将规则文件放置在项目根目录或 \~/.claude/CLAUDE.md（全局）23。  
* **结构化合并：** 由于 Claude CLI 默认只读取一个 CLAUDE.md，我们需要将 Antigravity 中分散的 “Always On” 规则合并。建议使用 Markdown 的一级标题将不同领域的规则隔开，例如 \# Coding Standards，\# Architecture Guidelines。  
* **局限性：** CLAUDE.md 无法根据文件类型动态加载。如果将所有规则都塞进去，会迅速消耗 Token 并稀释模型的注意力。因此，必须仅保留最核心的原则。

### **5.2 动态规则注入：基于 Shell Alias 与 Prompt Files 的工作流**

对于 Antigravity 中的 “Model Decision” 或 “Manual” 规则，我们可以利用 Claude CLI 的 \--system-prompt-file 参数来实现“按需加载” 24。

#### **5.2.1 模拟 Workflow**

假设 Antigravity 中有一个 “Refactor” Workflow，它加载了严格的代码质量规则。在 CLI 中，我们可以创建对应的 Prompt 文件：  
文件路径： .claude/prompts/refactor\_mode.md  
内容：

# **REFACTOR MODE**

You are now in strict refactoring mode.

1. You MUST NOT change logical behavior.  
2. You MUST add unit tests for every changed function.  
   ... (详细规则)

Shell Alias（移植关键）：  
在 .zshrc 或 .bashrc 中定义别名：

Bash

alias claude-refactor='claude \-p \--system-prompt-file.claude/prompts/refactor\_mode.md'

当开发者需要执行重构任务时，只需运行 claude-refactor "Refactor auth module"。这不仅完美复刻了 Antigravity 的任务隔离特性，甚至因为显式的模式切换而更加稳定 24。

### **5.3 从 Skill 到 MCP：可执行规则的架构升维**

这是移植工作中最具深度的部分。Antigravity 的 Skill（脚本+文档）在 Claude 生态中对应的最佳实践是 **Model Context Protocol (MCP)** Server。MCP 不仅能提供工具，还能提供**可编程的上下文**。

#### **5.3.1 移植路径：Skill \-\> MCP Server**

Antigravity Skill 通常是一个 Python 脚本。要将其转为 MCP，我们需要将其封装在一个符合 MCP 标准的接口中。

* **Antigravity:** Agent 读取 SKILL.md，决定运行 python scripts/db\_tool.py。  
* **Claude CLI:** Agent 连接到一个常驻的 MCP Server，该 Server 暴露 db\_tool 函数。

**优势：** MCP Server 是长连接的，可以维护状态（例如数据库连接池），而 Antigravity 的脚本每次调用都是独立的进程。这意味着 MCP 在执行数据库操作时延迟更低，且更安全 26。

#### **5.3.2 案例研究：SQL 安全规则的硬约束实现**

在 Antigravity 中，我们可能会写一条规则：“严禁执行 DELETE 语句”。这依赖于 Gemini 3 Pro 的自律，极易失效。  
在 Claude CLI \+ MCP 架构中，我们可以将这条规则代码化。  
**MCP Server 实现逻辑 (TypeScript 伪代码):**

TypeScript

server.tool("execute\_query", **async** ({ query }) \=\> {  
  *// 规则硬编码：程序级拦截*  
  **if** (query.trim().toUpperCase().startsWith("DELETE")) {  
    **throw** **new** Error("Security Rule Violation: DELETE operations are prohibited by MCP policy.");  
  }  
  **return** db.run(query);  
});

配置映射：  
在 claude.json 中配置该 Server 28：

JSON

{  
  "mcpServers": {  
    "secure-db": {  
      "command": "node",  
      "args": \["./mcp-servers/secure-db.js"\]  
    }  
  }  
}

此时，安全规则不再是 Prompt 中的一句话，而是编译在工具链中的代码。无论模型多么想执行删除操作，MCP 层都会无情拦截。这是从“概率性安全”向“确定性安全”的质的飞跃。

### **5.4 混合架构：Antigravity Terminal 中的 Claude CLI**

一种新兴的高级用法是在 Antigravity 的内置终端中直接运行 Claude CLI 30。这种架构结合了两者的优势：

* **宏观规划：** 使用 Antigravity 的 GUI 和 Gemini 模型进行项目概览、文件浏览和简单的代码补全。  
* **微观执行：** 当需要执行复杂的、高风险的重构或系统操作时，在 IDE 终端中呼出 Claude CLI。

规则同步脚本：  
为了让两者共享规则，可以编写一个简单的 Hook 脚本，在 Claude CLI 启动前，将 Antigravity 的 .agent/rules 聚合生成为临时的 CLAUDE.md：

Bash

*\# sync\_rules.sh*  
cat.agent/rules/\*.md \>.claude/CLAUDE.md  
claude "$@"

这样，Claude CLI 就能继承 Antigravity 定义的所有项目规则，实现了真正的跨环境一致性 31。

## **6\. 结论与建议**

通过对不稳定性根源的分析和跨平台移植的研究，本报告得出以下核心结论：

1. **不稳定性是架构性的：** Gemini 3 Pro 的不稳定性源于其 Reasoning/Output 共享的 Token 经济模型和对上下文过载的敏感性。Claude 4.5 的“Thinking”模型虽然更昂贵，但通过分离的 effort 参数和状态追踪机制，提供了更高的工程可靠性。  
2. **Markdown 即代码：** Agent 的指令文档应被视为源代码进行管理。结构化的 Markdown（标题、列表）和分层的信息架构（渐进式披露）是提升模型指令遵循率的关键。  
3. **规则的终极形态是代码：** “Anti-Gravity” 的文本规则虽然灵活，但在高风险操作中不够可靠。通过 MCP 协议将规则转化为服务器端的逻辑判断，是实现“反重力”（即对抗熵增和混乱）的最有效途径。

实施建议：  
对于追求极致稳定性的开发团队，建议采用“双模态”工作流：

* 利用 **Claude CLI \+ MCP** 作为核心执行引擎，处理数据库迁移、大规模重构等任务，并利用 MCP 将安全规则硬编码。  
* 利用 **Antigravity** 作为可视化前端和轻量级辅助，利用其 Rules 系统进行日常的代码风格提示。  
* 通过脚本同步机制，确保两个环境共享同一套“宪法”（System Prompts/Rules），从而在享受 IDE 便利的同时，不失 CLI 的精准与严谨。

## **7\. 附录：关键配置对照表**

| 功能特性 | Google Antigravity | Terminal Claude CLI (迁移后) | 移植方法论 |
| :---- | :---- | :---- | :---- |
| **规则定义** | .agent/rules/\*.md | CLAUDE.md (全局) / Prompt Files (局部) | 使用 Shell Alias 动态加载特定 Prompt 文件。 |
| **触发机制** | 自动 (Glob/Model Decision) | 被动 (System Prompt) / 主动 (Tool Call) | 依赖用户显式选择模式 (Alias) 或模型调用 MCP 工具。 |
| **技能实现** | SKILL.md \+ Scripts | MCP Servers | 将脚本封装为 MCP Server，配置 JSON。 |
| **安全约束** | Prompt 文本警告 | MCP 代码拦截 | **安全性大幅提升**，从劝导变为强制拦截。 |
| **模型引擎** | Gemini 3 Pro (固定) | Claude 3.5/4.5 (原生) / 任意模型 (Via Proxy) | Claude CLI 提供了模型选择的灵活性。 |

#### **引用的著作**

1. Build with Google Antigravity, our new agentic development platform, 访问时间为 一月 16, 2026， [https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)  
2. Guide to AI Coding Agents & Assistants: How to Choose the Right One \- Habr, 访问时间为 一月 16, 2026， [https://habr.com/en/articles/979402/](https://habr.com/en/articles/979402/)  
3. Gemini 3 Pro Preview – Vertex AI \- Google Cloud Console, 访问时间为 一月 16, 2026， [https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/gemini-3-pro-preview](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/gemini-3-pro-preview)  
4. Gemini 3 Pro | Generative AI on Vertex AI \- Google Cloud Documentation, 访问时间为 一月 16, 2026， [https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro)  
5. "Low" Reasoning Instability & Output Budget Cannibalization (Gemini 3.0 Pro), 访问时间为 一月 16, 2026， [https://discuss.ai.google.dev/t/low-reasoning-instability-output-budget-cannibalization-gemini-3-0-pro/109840](https://discuss.ai.google.dev/t/low-reasoning-instability-output-budget-cannibalization-gemini-3-0-pro/109840)  
6. Gemini 3 Developer Guide | Gemini API \- Google AI for Developers, 访问时间为 一月 16, 2026， [https://ai.google.dev/gemini-api/docs/gemini-3](https://ai.google.dev/gemini-api/docs/gemini-3)  
7. Gemini 3 Pro (High) is literally broken : r/google\_antigravity \- Reddit, 访问时间为 一月 16, 2026， [https://www.reddit.com/r/google\_antigravity/comments/1q5rf1a/gemini\_3\_pro\_high\_is\_literally\_broken/](https://www.reddit.com/r/google_antigravity/comments/1q5rf1a/gemini_3_pro_high_is_literally_broken/)  
8. Tutorial : Getting Started with Google Antigravity Skills \- Medium, 访问时间为 一月 16, 2026， [https://medium.com/google-cloud/tutorial-getting-started-with-antigravity-skills-864041811e0d](https://medium.com/google-cloud/tutorial-getting-started-with-antigravity-skills-864041811e0d)  
9. Gemini 3.0 Pro is absolutely unusable right now, whats going on? \- Reddit, 访问时间为 一月 16, 2026， [https://www.reddit.com/r/GoogleGeminiAI/comments/1peddtu/gemini\_30\_pro\_is\_absolutely\_unusable\_right\_now/](https://www.reddit.com/r/GoogleGeminiAI/comments/1peddtu/gemini_30_pro_is_absolutely_unusable_right_now/)  
10. What's new in Claude 4.5, 访问时间为 一月 16, 2026， [https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-5](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-5)  
11. Prompting best practices \- Claude Docs, 访问时间为 一月 16, 2026， [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)  
12. Introducing Claude Opus 4.5: our strongest model to date : r/ClaudeAI \- Reddit, 访问时间为 一月 16, 2026， [https://www.reddit.com/r/ClaudeAI/comments/1p5pmu5/introducing\_claude\_opus\_45\_our\_strongest\_model\_to/](https://www.reddit.com/r/ClaudeAI/comments/1p5pmu5/introducing_claude_opus_45_our_strongest_model_to/)  
13. GPT-5.1 Codex vs. Claude 4.5 Sonnet vs. Kimi K2 Thinking : Tested the best models for agentic coding \- Composio, 访问时间为 一月 16, 2026， [https://composio.dev/blog/kimi-k2-thinking-vs-claude-4-5-sonnet-vs-gpt-5-codex-tested-the-best-models-for-agentic-coding](https://composio.dev/blog/kimi-k2-thinking-vs-claude-4-5-sonnet-vs-gpt-5-codex-tested-the-best-models-for-agentic-coding)  
14. Claude 4.5\! (30 Hours of Thinking\!) \- YouTube, 访问时间为 一月 16, 2026， [https://www.youtube.com/watch?v=8\_wzjlWBcM4](https://www.youtube.com/watch?v=8_wzjlWBcM4)  
15. Boosting AI Performance: The Power of LLM-Friendly Content in Markdown, 访问时间为 一月 16, 2026， [https://developer.webex.com/blog/boosting-ai-performance-the-power-of-llm-friendly-content-in-markdown](https://developer.webex.com/blog/boosting-ai-performance-the-power-of-llm-friendly-content-in-markdown)  
16. MDEval: Evaluating and Enhancing Markdown Awareness in Large Language Models, 访问时间为 一月 16, 2026， [https://arxiv.org/html/2501.15000v2](https://arxiv.org/html/2501.15000v2)  
17. Effective Prompt Engineering with the Markdown Prompts Framework | CodeSignal Learn, 访问时间为 一月 16, 2026， [https://codesignal.com/learn/courses/understanding-llms-and-basic-prompting-techniques-1/lessons/effective-prompt-engineering-with-the-markdown-prompts-framework](https://codesignal.com/learn/courses/understanding-llms-and-basic-prompting-techniques-1/lessons/effective-prompt-engineering-with-the-markdown-prompts-framework)  
18. Skill authoring best practices \- Claude Docs, 访问时间为 一月 16, 2026， [https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)  
19. Introducing agent skills to Google Antigravity : r/google\_antigravity \- Reddit, 访问时间为 一月 16, 2026， [https://www.reddit.com/r/google\_antigravity/comments/1qce66h/introducing\_agent\_skills\_to\_google\_antigravity/](https://www.reddit.com/r/google_antigravity/comments/1qce66h/introducing_agent_skills_to_google_antigravity/)  
20. Agent Skills \- Google Antigravity Documentation, 访问时间为 一月 16, 2026， [https://antigravity.google/docs/skills](https://antigravity.google/docs/skills)  
21. Antigraviy Rules and Workflows \- YouTube, 访问时间为 一月 16, 2026， [https://www.youtube.com/watch?v=7tzgiTAxjjI](https://www.youtube.com/watch?v=7tzgiTAxjjI)  
22. Google Antigravity Documentation, 访问时间为 一月 16, 2026， [https://antigravity.google/docs/rules-workflows](https://antigravity.google/docs/rules-workflows)  
23. The Complete Guide to Setting Global Instructions for Claude Code CLI \- Naqeeb ali Shamsi, 访问时间为 一月 16, 2026， [https://naqeebali-shamsi.medium.com/the-complete-guide-to-setting-global-instructions-for-claude-code-cli-cec8407c99a0](https://naqeebali-shamsi.medium.com/the-complete-guide-to-setting-global-instructions-for-claude-code-cli-cec8407c99a0)  
24. CLI reference \- Claude Code Docs, 访问时间为 一月 16, 2026， [https://code.claude.com/docs/en/cli-reference](https://code.claude.com/docs/en/cli-reference)  
25. From md prompt files to one of the strongest CLI coding tools on the market \- Reddit, 访问时间为 一月 16, 2026， [https://www.reddit.com/r/ClaudeCode/comments/1oecd7g/from\_md\_prompt\_files\_to\_one\_of\_the\_strongest\_cli/](https://www.reddit.com/r/ClaudeCode/comments/1oecd7g/from_md_prompt_files_to_one_of_the_strongest_cli/)  
26. AWS Labs Aurora DSQL MCP Server, 访问时间为 一月 16, 2026， [https://docs.aws.amazon.com/aurora-dsql/latest/userguide/SECTION\_aurora-dsql-mcp-server.html](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/SECTION_aurora-dsql-mcp-server.html)  
27. benborla/mcp-server-mysql: A Model Context Protocol server that provides read-only access to MySQL databases. This server enables LLMs to inspect database schemas and execute read-only queries. \- GitHub, 访问时间为 一月 16, 2026， [https://github.com/benborla/mcp-server-mysql](https://github.com/benborla/mcp-server-mysql)  
28. Example Servers \- Model Context Protocol, 访问时间为 一月 16, 2026， [https://modelcontextprotocol.io/examples](https://modelcontextprotocol.io/examples)  
29. Build Your First MCP Server: Give Claude Superpowers It Didn't Ship With \- Medium, 访问时间为 一月 16, 2026， [https://medium.com/@ivmarcos/build-your-first-mcp-server-give-claude-superpowers-it-didnt-ship-with-7f46be888c96](https://medium.com/@ivmarcos/build-your-first-mcp-server-give-claude-superpowers-it-didnt-ship-with-7f46be888c96)  
30. Using Claude Code with Google Vertex AI | by Narish Samplay \- Medium, 访问时间为 一月 16, 2026， [https://medium.com/google-cloud/claude-code-on-google-vertex-ai-25e13b1b643d](https://medium.com/google-cloud/claude-code-on-google-vertex-ai-25e13b1b643d)  
31. How are you providing rules / system instructions to agents in Antigravity? (AGENTS.md, CLAUDE.md, etc.) : r/google\_antigravity \- Reddit, 访问时间为 一月 16, 2026， [https://www.reddit.com/r/google\_antigravity/comments/1poybmm/how\_are\_you\_providing\_rules\_system\_instructions/](https://www.reddit.com/r/google_antigravity/comments/1poybmm/how_are_you_providing_rules_system_instructions/)  
32. CLAUDE.md and Skills Experiment: What's the Best Way to Organize Instructions for Claude? : r/ClaudeAI \- Reddit, 访问时间为 一月 16, 2026， [https://www.reddit.com/r/ClaudeAI/comments/1pe37e3/claudemd\_and\_skills\_experiment\_whats\_the\_best\_way/](https://www.reddit.com/r/ClaudeAI/comments/1pe37e3/claudemd_and_skills_experiment_whats_the_best_way/)