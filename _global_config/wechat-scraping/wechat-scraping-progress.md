# 微信公众号文章抓取项目 - 工作进度

**更新时间**: 2026-02-05
**项目状态**: 全局 MCP 配置已更新，需要重启 Claude Code

---

## 📋 项目目标

抓取微信公众号后台的已发表文章数据，并同步到飞书表格。

**最终目标**:
- 抓取所有已发表文章（标题、URL、发布时间、合集、曝光量、互动量等）
- 保存为 JSON 格式
- 同步到飞书表格

---

## ✅ 已完成的工作

### Phase 1: 探索阶段（已完成）
1. ✅ 使用 Playwright Codegen 录制了完整的操作流程
   - 文件: `recorded_full_workflow.py`
   - 录制内容: 登录 → 内容管理 → 发表记录 → 浏览文章 → 翻页 → 筛选（原创、合集）

2. ✅ 创建了多个版本的 Python RPA 脚本
   - `scrape_wechat_articles_v3.py` - 增加等待时间
   - `scrape_wechat_articles_v4.py` - 基于录制流程优化
   - `scrape_wechat_articles_v5.py` - 完整抓取+翻页支持
   - `scrape_wechat_articles_v6.py` - 使用录制的工作流

3. ✅ 发现问题并纠正方向
   - 问题: Python RPA 脚本方式不稳定（cookies 过期、session 管理复杂）
   - 用户建议: 使用 Puppeteer/Playwright MCP 而不是 Python 脚本
   - 原因: MCP 是 Claude Code 的正确架构，更稳定可靠

### Phase 2: MCP 配置（已完成）
4. ✅ 发现 Playwright MCP 已存在
   - 位置: `/Users/dj/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/playwright/`
   - 命令: `npx @playwright/mcp@latest`

5. ✅ 创建项目级 MCP 配置
   - 文件: `/Users/dj/Desktop/小静的skills/_global_config/.mcp.json`
   - 配置内容:
     ```json
     {
       "mcpServers": {
         "playwright": {
           "command": "npx",
           "args": ["@playwright/mcp@latest"]
         }
       }
     }
     ```

6. ✅ 更新全局 settings.json
   - 添加: `"enableAllProjectMcpServers": true`
   - 位置: `/Users/dj/.claude/settings.json`
   - 作用: 自动启用所有项目目录下的 `.mcp.json` 中定义的 MCP 服务器

7. ✅ 创建全局 MCP 配置（符号链接方式）
   - 源文件: `/Users/dj/Desktop/小静的skills/_global_config/.mcp.json`
   - 符号链接: `~/.mcp.json` → 源文件
   - 作用: **在任何目录下都可以使用 Playwright MCP**
   - 优势:
     - 集中管理：所有配置都在 `小静的skills` 文件夹下
     - 可迁移性：换电脑时只需迁移文件夹，重新创建符号链接
     - 一致性：与 skills、hooks 的管理方式保持一致

---

## 🔄 下一步操作（重启后继续）

### Step 1: 启用 Playwright MCP
**重启 Claude Code 后**，系统会检测到新的 `.mcp.json` 文件并提示：
```
检测到新的 MCP 服务器: playwright
是否启用？
```
**操作**: 选择"启用"或"批准"

### Step 2: 验证 MCP 工具可用
重启后，告诉 Claude:
```
"继续微信文章抓取项目，验证 Playwright MCP 是否可用"
```

Claude 会检查可用的 MCP 工具，应该包括：
- `playwright_navigate` - 导航到 URL
- `playwright_click` - 点击元素
- `playwright_screenshot` - 截图
- `playwright_evaluate` - 执行 JavaScript
- 等等...

### Step 3: 使用 MCP 抓取文章
**不再需要 Python 脚本**，直接使用 MCP 工具：

1. **导航到微信公众号后台**
   ```
   playwright_navigate("https://mp.weixin.qq.com/")
   ```

2. **等待登录**（手动扫码）

3. **导航到发表记录**
   - 点击"内容管理"
   - 点击"发表记录"

4. **提取文章列表**
   - 使用 `playwright_evaluate` 执行 JavaScript 提取数据
   - 或使用 `playwright_click` + `playwright_screenshot` 逐步操作

5. **翻页抓取**
   - 点击"下一页"
   - 重复提取

6. **保存数据**
   - 保存为 JSON: `/Users/dj/Desktop/小静的skills/_global_config/wechat_articles_data.json`

### Step 4: 同步到飞书（后续）
- 读取 JSON 数据
- 匹配飞书表格中的文章（按标题）
- 更新字段: 发布时间、合集、曝光量、互动量、发布状态

---

## 📁 关键文件位置

### 已录制的工作流
- `/Users/dj/Desktop/小静的skills/_global_config/recorded_full_workflow.py`
  - 包含完整的操作流程和选择器

### MCP 配置
- `/Users/dj/Desktop/小静的skills/_global_config/.mcp.json`
  - Playwright MCP 服务器配置

### 输出文件
- `/Users/dj/Desktop/小静的skills/_global_config/wechat_articles_data.json`
  - 抓取的文章数据（待生成）

### 历史脚本（参考用）
- `scrape_wechat_articles_v3.py` - v6.py
- `recorded_article_scraping.py`

---

## 🔑 关键选择器（从录制中提取）

根据 `recorded_full_workflow.py`，关键选择器：

```python
# 导航
page.get_by_text("内容管理").click()
page.get_by_role("link", name="发表记录").click()

# 文章链接（示例）
page.get_by_role("link", name="立春赏花图鉴：把春天最早的消息带给你 🌸")

# 翻页
page.get_by_role("link", name="下一页").click()
page.get_by_role("link", name="上一页").click()

# 筛选
page.get_by_role("link", name="原创", exact=True).click()
page.get_by_role("link", name="合集").click()
```

---

## 💡 重要提醒

### 为什么使用 MCP 而不是 Python 脚本？

**Python RPA 方式的问题**:
- ❌ Cookies 频繁过期
- ❌ Session 管理复杂
- ❌ 需要手动处理登录状态
- ❌ 每次运行都是独立的进程

**MCP 方式的优势**:
- ✅ Claude 直接控制浏览器
- ✅ Session 持久化更好
- ✅ 可以实时交互和调试
- ✅ 符合 Claude Code 的架构设计

### 用户的关键反馈
> "你现在这种操作属于 rpa 的方式吗 如果用脚本的方式反复尝试不成功你是不是可以先使用那个puppeterMCP来试一下"

> "你就应该把这些在trae一种安装的mcp给它变成全局可用的而不是让我去打开trae来配合你"

---

## 🚀 重启后的第一句话

重启 Claude Code 后，直接说：

```
"继续微信文章抓取项目"
```

Claude 会：
1. 读取这个进度文档
2. 验证 Playwright MCP 是否已启用
3. 继续从 Step 2 开始执行

---

## 📊 数据结构（预期）

抓取的 JSON 数据格式：

```json
[
  {
    "title": "文章标题",
    "url": "https://mp.weixin.qq.com/s/...",
    "publish_date": "2026-02-01",
    "collection": "合集名称",
    "views": 1234,
    "interactions": 56,
    "status": "已发布",
    "extracted_at": "2026-02-05T15:42:00"
  }
]
```

---

**状态**: ⏸️ 等待重启后继续
**下一步**: 启用 Playwright MCP → 验证工具 → 开始抓取
