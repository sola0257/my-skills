# Validation Matrix: docs-scraper

## Test Scenarios

### 1️⃣ Normal Operations (正常触发)

| Test Case | Input | Expected Behavior | Pass Criteria |
|-----------|-------|-------------------|---------------|
| Basic trigger (中文) | "帮我抓取 https://docs.example.com 的文档" | Skill activates, asks for output directory | Prompt appears |
| Basic trigger (English) | "Scrape docs from https://docs.example.com" | Skill activates, asks for output directory | Prompt appears |
| With directory | User provides "~/Desktop/Test" | Creates directory if not exists, proceeds | Directory created |
| Full execution | Complete scrape of 5+ pages | All pages scraped, files generated | Markdown files exist |

### 2️⃣ Edge Cases (边缘情况)

| Test Case | Scenario | Expected Behavior | Pass Criteria |
|-----------|----------|-------------------|---------------|
| Login required | Site shows login page | Asks user to login, waits for "已登录" | Workflow resumes after confirmation |
| No "Copy Page" button | Button not found on page | Saves HTML to `_raw_html/` folder | HTML file exists |
| Page load failure | Network timeout | Retries 2x, logs to `_failed_pages.md`, continues | Error logged, other pages scraped |
| Empty content | Page has no text content | Logs warning, continues | Warning in log |
| Very long category | >8000 tokens in one category | Splits into Part1, Part2, etc. | Multiple part files created |
| Non-standard navigation | No sidebar, only links | Extracts all internal links, groups by URL path | Files still generated |

### 2.5️⃣ Incremental Mode Tests (增量模式测试)

| Test Case | Scenario | Expected Behavior | Pass Criteria |
|-----------|----------|-------------------|---------------|
| Detect existing files | Output dir has .md files | Prompts user for mode selection (1/2/3) | Mode selection prompt appears |
| Mode 1 - Skip existing | Choose incremental, file exists | Skips category, logs "跳过" | No duplicate content, skip logged |
| Mode 2 - Full rescrape | Choose full scrape | Clears existing, scrapes all | All files recreated |
| Mode 3 - Resume | _failed_pages.md exists | Re-attempts failed pages only | Failed pages retried |
| Empty directory | No existing .md files | Proceeds with full scrape, no mode prompt | Direct full scrape |
| Default mode | No response to mode prompt | Uses mode 1 (incremental) | Incremental behavior applied |

### 3️⃣ Interference Rejection (干扰排除)

| Test Case | Input | Expected Behavior | Pass Criteria |
|-----------|-------|-------------------|---------------|
| Single article URL | "帮我抓取 https://blog.example.com/single-post" | May scrape but should handle gracefully | Single file or appropriate message |
| Non-doc website | "抓取 https://amazon.com" | Should attempt but handle unusual structure | Graceful handling |
| Vague request | "帮我处理这个网站" | Should NOT trigger (too vague) | Skill stays dormant |
| Image/file URL | "下载 https://example.com/file.pdf" | Should NOT trigger (not a doc site) | Skill stays dormant |

### 4️⃣ Quiet Mode Verification (静默执行验证)

| Test Case | Scenario | MUST NOT Happen |
|-----------|----------|-----------------|
| Mid-execution pause | During scraping | "是否继续?" or "Should I proceed?" |
| Per-category confirmation | After each category | "已完成X分类，继续吗?" |
| Error confirmation | On page failure | "页面失败，是否跳过?" |
| Progress updates | During execution | "已完成 30%..." (unless requested) |

---

## How to Run Tests

### Manual Testing

1. **Trigger test**: Say "帮我抓取 [URL] 的文档"
2. **Verify startup interaction**: Should ask for output directory
3. **Provide directory**: Give a test path
4. **Observe execution**: Should complete without mid-execution questions
5. **Check outputs**: Verify Markdown files, HTML backups, failure logs

### Automated Verification Checklist

After each test run, verify:

- [ ] Output directory was created
- [ ] At least one .md file was generated
- [ ] Files are named in kebab-case
- [ ] Long files are split into parts
- [ ] `_failed_pages.md` only exists if failures occurred
- [ ] `_raw_html/` only contains pages without "Copy Page" button
- [ ] No mid-execution confirmations were requested

### 5️⃣ Content Completeness Verification (内容完整性验证) ⚠️ CRITICAL

| Test Case | Verification Method | Pass Criteria |
|-----------|---------------------|---------------|
| No summarization | Compare scraped content length to original page | Scraped content ≥ 80% of original length |
| All chunks extracted | Count chunks from `read_url_content`, verify all fetched | Every chunk position was retrieved |
| Code blocks preserved | Check for ```code``` blocks in output | Code blocks match original formatting |
| Links preserved | Check for markdown links `[text](url)` | Links are present and correct |
| Tables preserved | Check for markdown tables | Tables maintain structure |
| Headers preserved | Check for # ## ### headers | Header hierarchy matches original |

#### Content Comparison Test

```
1. Manually copy content from ONE page on the target website
2. Run scraper on same website  
3. Find the corresponding section in scraped output
4. Compare:
   - Word count: Should be within 80-100% of original
   - All major sections present
   - Code examples not truncated
   - No "..." or "[summary]" placeholders
```

#### Anti-Pattern Detection

These patterns indicate FAILED content extraction:

| Pattern Found | Problem |
|---------------|---------|
| Content is noticeably shorter | Summarization occurred |
| Generic descriptions instead of specifics | Content was paraphrased |
| Missing code examples | Chunks were skipped |
| "Based on the documentation..." | Agent wrote own interpretation |
| Missing tables/diagrams references | Incomplete extraction |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-13 | v1.1 | Added Content Completeness Verification section |
| 2026-01-13 | v1.0 | Initial validation matrix |
