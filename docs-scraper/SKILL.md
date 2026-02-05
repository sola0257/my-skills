---
name: docs-scraper
description: |
  Comprehensive documentation website scraper that extracts content and organizes it into categorized Markdown files. 
  Use when Claude needs to: (1) Scrape/download documentation from a website, (2) Sync docs to local files, 
  (3) Extract and categorize help articles, (4) Archive web documentation for offline use.
  Triggers: "抓取文档", "scrape docs", "下载文档", "download docs", "同步文档", "sync docs", "抓取网页", "archive docs"
license: MIT
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

# Documentation Website Scraper

## 🔇 Quiet Mode Protocol (CRITICAL)

**MANDATORY**: After the initial startup interactions (asking for output directory and login confirmation if needed), execute the ENTIRE workflow silently without interruption.

- **DO NOT** ask "Should I continue?" or "Do you want me to proceed?"
- **DO NOT** ask for confirmation before scraping each page
- **DO NOT** stop to report progress mid-execution
- **GENERATE** the complete output in one go
- **IF** a page fails to load: log it and continue to the next page
- **IF** "Copy Page" button is not found: save as HTML and continue
- **IF** content is empty: log warning and continue

---

## ⚠️ Content Extraction Requirements (CRITICAL)

**MANDATORY**: You must extract the COMPLETE, ORIGINAL content from each page. DO NOT summarize, paraphrase, or abbreviate.

### What to do:

1. **Use `read_url_content`** to get the page structure and available chunks
2. **MUST fetch ALL chunk positions** using `view_content_chunk` for every position (4, 5, 6, 7... until the last position)
3. **Concatenate ALL chunks** to get the complete page content
4. **Preserve original content** exactly as retrieved - do not rewrite or summarize
5. **If a page has 10 chunks, fetch all 10 chunks** - never skip chunks

### What NOT to do:

- ❌ **DO NOT** read only chunk headers/titles and write your own content
- ❌ **DO NOT** summarize the content in your own words
- ❌ **DO NOT** skip chunks that seem redundant
- ❌ **DO NOT** create shortened versions of the documentation
- ❌ **DO NOT** add your own explanations or interpretations

### Example - CORRECT extraction:

```
1. read_url_content("https://docs.example.com/api") 
   → Returns: positions 0-12 available
   
2. FOR position in [4, 5, 6, 7, 8, 9, 10, 11, 12]:  # Skip 0-3 (navigation)
       view_content_chunk(document_id, position)
       → Append to page_content
       
3. Save complete page_content to file
```

### Example - WRONG extraction (DO NOT DO THIS):

```
1. read_url_content("https://docs.example.com/api")
   → See headers: "Overview", "Authentication", "Endpoints"
   
2. Write your own summary based on headers  ← WRONG!
```

### Browser Alternative (Preferred for completeness):

If `read_url_content` doesn't capture complete content:
1. Use browser to navigate to page
2. Look for "Copy Page" or "Copy to Clipboard" button
3. Click to get pre-formatted Markdown
4. If no such button exists, use browser to extract full page text

---

## Overview

This skill scrapes documentation websites with sidebar/navigation structures, extracts content from each page, and organizes them into categorized Markdown files for Claude Code to learn from.

## Workflow Decision Tree

```
START
  │
  ├─► [1] Ask user for OUTPUT DIRECTORY
  │       └─► Wait for user response
  │
  ├─► [2] Check output directory for existing files
  │       │
  │       ├─► Existing .md files found?
  │       │       │
  │       │       ├─► YES: Ask user "检测到已有X个文件，选择模式：
  │       │       │         1️⃣ 增量抓取 - 仅抓取新页面
  │       │       │         2️⃣ 全量抓取 - 重新抓取所有页面
  │       │       │         3️⃣ 续传模式 - 继续上次未完成的抓取"
  │       │       │
  │       │       └─► NO: Proceed with full scrape
  │       │
  │       └─► Wait for user response
  │
  ├─► [3] Open target URL
  │       │
  │       ├─► Login required? ──YES──► Ask user to login
  │       │                            └─► Wait for "已登录" confirmation
  │       │                            └─► Refresh and continue
  │       │
  │       └─► NO ──► Continue
  │
  ├─► [4] Detect navigation structure (sidebar, menu, table of contents)
  │
  ├─► [5] Extract all categories and page links
  │
  ├─► [6] FOR EACH category:
  │       │
  │       ├─► IF incremental mode AND category file exists:
  │       │       └─► SKIP this category (log as "已存在，跳过")
  │       │
  │       ├─► FOR EACH page in category:
  │       │       │
  │       │       ├─► Open page
  │       │       │
  │       │       ├─► Extract complete content (ALL chunks)
  │       │       │
  │       │       └─► Append content to category buffer
  │       │
  │       ├─► Check if content exceeds 8000 tokens (~6000 words)
  │       │       │
  │       │       ├─► YES: Split into Part1, Part2, etc.
  │       │       │
  │       │       └─► NO: Save as single .md file
  │       │
  │       └─► Continue to next category
  │
  ├─► [7] Generate _failed_pages.md (only if there are failures)
  │
  └─► [8] Output completion summary (including skipped count)
END
```


---

## Allowed Interactions (Startup Phase ONLY)

### Interaction 1: Output Directory

**MUST ask before starting:**
```
请告诉我文档的输出目录路径。
例如: ~/Desktop/Claude Docs 或 /Users/yourname/Documents/docs
```

**Wait for user response, then proceed.**

### Interaction 2: Login Detection

**ONLY if login page/prompt is detected:**
```
检测到该网站需要登录才能访问内容。
请在浏览器中完成登录，然后回复"已登录"继续。
```

**Wait for user to confirm "已登录" or similar, then refresh and proceed.**

### Interaction 3: Incremental Mode (ONLY if existing files detected)

**ONLY if output directory contains .md files:**
```
检测到输出目录已有 X 个 Markdown 文件。请选择抓取模式：

1️⃣ 增量抓取 - 仅抓取新增页面，跳过已有文件
2️⃣ 全量抓取 - 删除现有文件，重新抓取所有
3️⃣ 续传模式 - 继续抓取上次失败/未完成的页面

请回复 1、2 或 3
```

**Behavior for each mode:**

| Mode | Behavior |
|------|----------|
| **1 (增量)** | Check each category file, skip if exists, only scrape new categories |
| **2 (全量)** | Clear directory, scrape everything fresh |
| **3 (续传)** | Read `_failed_pages.md`, re-attempt those pages only |

**Default (if no response after 5 seconds)**: Use mode 1 (incremental)

---

## Incremental Scraping Logic

### How incremental mode works:

```python
# Pseudo-code for incremental scraping
for category in all_categories:
    expected_filename = to_kebab_case(category.name) + ".md"
    
    if incremental_mode:
        if file_exists(output_dir / expected_filename):
            log(f"⏭️ 跳过: {expected_filename} (已存在)")
            skipped_count += 1
            continue
    
    # Scrape this category
    content = scrape_category(category)
    save_file(output_dir / expected_filename, content)
    scraped_count += 1
```

### Resume mode logic:

```python
# Read failed pages from previous run
if resume_mode and file_exists("_failed_pages.md"):
    failed_pages = parse_failed_pages_log()
    
    for page in failed_pages:
        retry_scrape(page)
        if success:
            remove_from_failed_log(page)
```

### Summary output for incremental mode:

```
✅ 抓取完成！

📁 输出目录: /path/to/output

📊 统计:
- 新抓取: 3 个分类
- 已跳过: 5 个分类 (已存在)
- 失败: 1 个页面

📄 新增文件:
- New-Category-1.md
- New-Category-2.md
- New-Category-3.md

⏭️ 跳过的文件:
- Existing-Category-1.md
- Existing-Category-2.md
- ...
```

---

## Navigation Structure Detection

The skill intelligently detects various navigation patterns:

| Pattern | Detection Method |
|---------|-----------------|
| **Sidebar list** | `nav`, `aside`, `.sidebar`, `#sidebar` elements |
| **Nested menu** | `ul > li > a` with parent-child relationships |
| **Table of contents** | `.toc`, `#toc`, `.table-of-contents` elements |
| **Tab navigation** | `.tabs`, `[role="tablist"]` elements |
| **Accordion** | `.accordion`, `details > summary` elements |
| **Breadcrumb-based** | Follow category hierarchy from breadcrumbs |

**Fallback**: If no clear navigation structure is found, extract all internal links from the page and group by URL path segments.

---

## Output Structure

```
[Output Directory]/
├── Category-Name-1.md           # One file per category
├── Category-Name-2.md
├── Long-Category-Part1.md       # Split if > 8000 tokens
├── Long-Category-Part2.md
├── _raw_html/                   # Fallback HTML saves
│   ├── page-without-copy-button.html
│   └── ...
└── _failed_pages.md             # Only created if failures exist
```

### File Naming Convention

- Category names converted to kebab-case
- Spaces → hyphens, special chars removed
- Example: "Build with Claude" → `Build-with-Claude.md`

### _failed_pages.md Format

```markdown
# Failed Pages Log

## [Category Name]
- [ ] Page Title - URL - Error: [error description]
- [ ] Another Page - URL - Error: timeout after 3 retries

Generated: [timestamp]
```

---

## Error Handling (Silent)

| Error Type | Action | Log |
|------------|--------|-----|
| Page load timeout | Retry 2x, then skip | ✅ Log to _failed_pages.md |
| "Copy Page" not found | Save as HTML | ❌ Not logged (expected fallback) |
| Empty content | Skip page | ✅ Log to _failed_pages.md |
| Network error | Retry 2x, then skip | ✅ Log to _failed_pages.md |
| Element not found | Use fallback selectors | ❌ Not logged |

---

## Token Estimation

To determine if a file needs splitting:

- **Target**: ~8000 tokens per file (optimal for Claude Code processing)
- **Estimation**: 1 token ≈ 4 characters (English) or 1.5 characters (Chinese)
- **Split threshold**: ~32,000 characters (English) or ~12,000 characters (Chinese)

When splitting:
1. Split at natural boundaries (headings, sections)
2. Maintain document structure in each part
3. Add "[Continued in Part N]" markers

---

## Few-Shot Examples

### ✅ Good Case: Uninterrupted Execution

**User**: 帮我抓取 https://docs.example.com 的文档

**Claude (Correct Behavior)**:
```
请告诉我文档的输出目录路径。
例如: ~/Desktop/Claude Docs
```

**User**: ~/Desktop/Example Docs

**Claude (Correct Behavior)**:
```
[Opens browser, navigates to URL]
[Detects sidebar navigation with 5 categories]
[Scrapes all 23 pages across 5 categories]
[Saves 5 Markdown files]

✅ 抓取完成！

📁 输出目录: ~/Desktop/Example Docs

📄 生成文件:
- Getting-Started.md (3 pages, 4,521 tokens)
- API-Reference.md (8 pages, 7,892 tokens)
- Tutorials-Part1.md (6 pages, 7,456 tokens)
- Tutorials-Part2.md (4 pages, 5,234 tokens)
- FAQ.md (2 pages, 1,203 tokens)

⚠️ 失败页面: 0

总计: 23 页 → 5 文件
```

### ❌ Anti-Pattern: DO NOT DO THIS

**User**: 帮我抓取 https://docs.example.com 的文档

**Claude (WRONG - Interrupting mid-workflow)**:
```
我已经找到了 5 个分类，共 23 个页面。是否继续抓取？
```
☝️ **NEVER do this. Execute silently after startup interactions.**

**Claude (WRONG - Asking for confirmation per category)**:
```
已完成 "Getting Started" 分类（3 页）。是否继续抓取下一个分类？
```
☝️ **NEVER do this. Complete ALL categories in one execution.**

**Claude (WRONG - Stopping on error)**:
```
页面 "Advanced Setup" 加载失败。是否跳过并继续？
```
☝️ **NEVER do this. Log the error and continue automatically.**

---

## Complete Example Workflow

```
User: 抓取 https://platform.claude.com/docs/en/home 的文档

Claude: 请告诉我文档的输出目录路径。
        例如: ~/Desktop/Claude Docs

User: ~/Desktop/Claude Docs

Claude: [Silently executes entire workflow...]
        
        ✅ 抓取完成！
        
        📁 输出目录: /Users/xxx/Desktop/Claude Docs
        
        📄 生成文件:
        - Build-with-Claude.md (4 pages)
        - Capabilities.md (6 pages)
        - Tools.md (5 pages)
        - Best-Practices.md (3 pages)
        - API-Reference-Part1.md (10 pages)
        - API-Reference-Part2.md (8 pages)
        
        📂 HTML 备份: 2 files in _raw_html/
        
        ⚠️ 失败页面: 查看 _failed_pages.md (1 条记录)
```
