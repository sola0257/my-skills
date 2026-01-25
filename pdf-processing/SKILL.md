---
name: pdf-processing
description: "PDF处理工具。支持：URL转PDF、PDF质量评估、PDF批量重命名。触发词：'转换URL为PDF'、'评估PDF质量'、'重命名PDF'、'处理PDF文件'"
license: MIT
version: "1.0"
---

# PDF 处理工具 v1.0

## 🚨 静默执行协议

**执行规则：**
- ❌ **禁止** 请求确认
- ✅ **必须** 自动处理并返回结果

---

## 📋 功能概述

### 功能1: URL转PDF

将网页URL转换为PDF文件，用于知识库构建。

**使用场景**：
- 保存学术文章
- 归档网页内容
- 为NotebookLM准备资料

**脚本位置**：
```
/Users/dj/Documents/slowseasons AI工厂/内容生产/content-production-skills/skills/pdf-processing/batch_convert_urls.py
```

---

### 功能2: PDF质量评估

分析PDF内容，评估是否适合用于知识提取。

**评估维度**：
- 文本可提取性
- 内容完整性
- 相关性评分

---

### 功能3: PDF批量重命名

根据PDF内容智能重命名文件。

**脚本位置**：
```
/Users/dj/Documents/slowseasons AI工厂/内容生产/content-production-skills/skills/pdf-processing/rename_pdfs.py
```

---

## 🔧 使用方法

### URL转PDF
```bash
python batch_convert_urls.py <url_list_file> <output_dir>
```

### PDF重命名
```bash
python rename_pdfs.py <pdf_dir>
```

---

## 🔗 关联技能

| 技能 | 关系 |
|------|------|
| web-resource-search | 提供URL列表 → pdf-processing转换 |
| knowledge-extractor | pdf-processing输出 → 知识提取 |
| docs-scraper | 可配合抓取网页转PDF |

---

## 📝 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v1.0 | 2026-01-22 | 初始版本：URL转换、质量评估、重命名 |
