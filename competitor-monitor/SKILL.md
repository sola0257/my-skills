---
name: competitor-monitor
description: "对标账号监控与自我状态更新。基于 MediaCrawler，监控对标账号的爆文数据，同时监控自己账号的发布状态并自动更新排期表。"
license: MIT
version: "1.0"
---


## ⚠️ 恢复执行重要提醒

**当用户说"继续Step X"、"继续执行"、"下一步"时**：

本 Skill 的所有步骤都可能需要用户输入或确认。
在恢复执行任何步骤前，请遵循全局"恢复执行强制规则"（~/.claude/CLAUDE.md）：

1. ✅ 先读取该步骤的完整描述
2. ✅ 检查是否需要提问或确认
3. ✅ 确认所有输入参数
4. ✅ 有疑问先问用户

**禁止直接开始执行，禁止假设已知上下文。**

---

# 对标账号监控工具 v1.0

## 📋 概述

本工具是全域自媒体运营的"眼睛"。它利用自动化爬虫技术（MediaCrawler），定期巡查指定账号。

**核心功能：**
1.  **竞品监控**：抓取对标账号的最新笔记（标题、封面、点赞、评论），生成分析报告。
2.  **自我监控**：监控自己的主页，发现新发布内容自动更新《内容排期表》。

---

## 🛠️ 安装与配置 (首次必读)

由于涉及浏览器自动化，本 Skill 依赖开源项目 `MediaCrawler`。

**安装步骤：**
1.  下载 MediaCrawler 源码：[GitHub](https://github.com/NanmiCoder/MediaCrawler)
2.  将源码解压至：`/Users/dj/Desktop/全域自媒体运营/工具/MediaCrawler/`
3.  在终端运行安装依赖：
    ```bash
    cd /Users/dj/Desktop/全域自媒体运营/工具/MediaCrawler
    pip install -r requirements.txt
    playwright install
    ```

---

## ⚙️ 监控配置

配置文件位于：`config/monitored_accounts.json`

```json
{
  "self": {
    "xhs_id": "你的小红书号",
    "last_check": "2026-01-24 12:00"
  },
  "competitors": [
    {
      "name": "对标A",
      "xhs_id": "123456789",
      "tags": ["绿植", "阳台"]
    },
    {
      "name": "对标B",
      "xhs_id": "987654321",
      "tags": ["干货", "养护"]
    }
  ]
}
```

---

## 🔄 执行流程

### 1. 竞品分析模式
**命令**：`/competitor-monitor analyze`

**逻辑**：
1.  调用 MediaCrawler 抓取 `competitors` 列表中的账号。
2.  筛选近 7 天点赞 > 500 的笔记。
3.  生成《对标账号分析报告.md》，存入 `全域自媒体运营/选题库/`。

### 3. 发现对标模式 (新增)
**命令**：`/competitor-monitor discover [关键词]`

**逻辑**：
1.  自动搜索指定关键词（如"办公室绿植"）。
2.  抓取前20-50篇笔记。
3.  自动筛选出点赞 > 1000 的潜力账号。
4.  输出候选人列表（含主页链接）。

**示例**：
```bash
/competitor-monitor discover 懒人绿植
```

---

## 📝 输出示例 (竞品分析)

```markdown
# 🕵️‍♀️ 对标账号分析周报 (2026-01-24)

## 📊 爆文概览

| 账号 | 标题 | 互动量 | 爆点分析 | 链接 |
|---|---|---|---|---|
| 对标A | 为什么你的龟背竹不开背？ | 1.2w | 痛点直击 + 对比图 | [查看](...) |
| 对标B | 3块钱自制生根水 | 8k | 低成本 + 实用 | [查看](...) |

## 💡 选题建议
1.  **龟背竹养护**：近期热度回升，建议跟进"开背技巧"。
2.  **自制肥料**：低成本养花话题永远有流量。
```

---

## 📝 依赖

- `MediaCrawler` (需手动安装)
- `playwright`

