---
name: xiaohongshu-content-generator
description: "Generate Xiaohongshu (Little Red Book) content. 支持双标题系统、违禁词检查、自动封面排版、账号阶段感知。自动生成文案和配图，支持商品软植入。"
license: MIT
version: "6.0"
---

# 小红书图文内容一键生成器 v6.0

## 🚨 静默执行协议

**执行规则：**
- ❌ **禁止** 请求确认以继续
- ✅ **必须** 一次性生成完整输出（文案 + 自动排版封面 + 配图）
- ✅ **必须** 自动进行违禁词检查
- ✅ **必须** 根据粉丝数自动判断内容策略

---

## 📋 核心功能更新 (v6.0)

1.  **双标题系统**：
    *   **视觉标题 (Visual Title)**：用于封面大字，痛点/情绪向，吸引点击。
    *   **搜索标题 (Search Title)**：用于笔记正文，长尾关键词，优化SEO。
2.  **封面排版自动化**：
    *   自动生成底图。
    *   自动叠加文字（基于 Python Pillow）。
    *   支持 8 种高转化排版（左右对分、杂志风等）。
3.  **违禁词自动检查**：
    *   调用 `compliance-checker` skill。
    *   自动修正高风险词汇。
4.  **账号阶段感知**：
    *   **起号期 (0-500粉)**：纯干货，不挂车，建立信任。
    *   **成长期 (500-2000粉)**：软植入，评论区引导。
    *   **成熟期 (2000+粉)**：正常带货。

---

## ⚙️ 账号阶段配置

**判断逻辑（满足任一条件即可进阶）：**

| 阶段 | 粉丝数 | 互动特征 | 内容策略 |
|---|---|---|---|
| **起号期** | 0-500 | 评论区无购买询问 | 纯干货，商品仅作为道具 |
| **成长期** | 500-2000 | 评论区出现"在哪买" | 软植入，1-2个要点提及 |
| **成熟期** | 2000+ | 评论区大量购买询问 | 挂链接，强种草 |

---

## 🔄 执行流程

1.  **解析输入**：获取主题、粉丝数、互动情况。
2.  **生成文案**：
    *   生成双标题。
    *   生成正文（黄金3秒开头）。
    *   生成 Tags。
3.  **违禁词检查**：调用 `compliance-checker`。
4.  **生成图片 Prompts**：
    *   封面 Prompt (Dreamy style, no text)。
    *   正文配图 Prompts。
5.  **调用生成脚本** (`scripts/generate_xhs_post.py`)：
    *   生成底图。
    *   **合成封面**：将视觉标题叠加到底图上。
    *   生成其他配图。
6.  **保存结果**：
    *   Markdown 文档。
    *   所有图片文件。

---

## 🛠️ 调用方式

```bash
# 完整调用
/xiaohongshu-content-generator 主题="绿萝养护" 粉丝数=200

# 强制指定商品
/xiaohongshu-content-generator 主题="绿萝养护" 商品ID="12345"
```

---

## 📦 输出结构

```
/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/小红书/
└── 2026-01-24_绿萝养护_双标题/
    ├── 2026-01-24_绿萝养护.md       # 含双标题、正文、违禁词检查报告
    ├── cover_final.png             # 最终合成封面（带文字）
    ├── cover_base.png              # 封面底图（无文字，留底）
    ├── 01.png, 02.png...           # 正文配图
    └── data.json                   # 元数据
```

---

## 📝 依赖

- `compliance-checker` (Skill)
- `yunwu-api` (Image Generation)
- `python-pillow` (Image Composition)
- `scripts/cover_generator.py` (Layout Engine)

