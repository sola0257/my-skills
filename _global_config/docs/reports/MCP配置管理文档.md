# MCP 配置管理文档

**更新时间**: 2026-02-05
**配置文件**: `/Users/dj/Desktop/小静的skills/_global_config/.mcp.json`
**符号链接**: `~/.mcp.json` → 配置文件

---

## 📋 已配置的 MCP 服务器

### 1. Playwright MCP
**类型**: 命令行工具
**用途**: 浏览器自动化、网页抓取
**配置**:
```json
{
  "command": "npx",
  "args": ["@playwright/mcp@latest"]
}
```

**使用场景**:
- 微信文章抓取
- 自动化发布
- 网页数据采集

---

### 2. Supabase MCP
**类型**: HTTP 服务
**用途**: 数据库存储、数据管理
**配置**:
```json
{
  "type": "http",
  "url": "https://mcp.supabase.com/mcp"
}
```

**使用场景**:
- 商品库存储
- 粉丝数记录
- 已发布内容管理
- 选题库管理

---

### 3. GitHub MCP
**类型**: HTTP 服务（需要 Token）
**用途**: 代码版本管理、协作
**配置**:
```json
{
  "type": "http",
  "url": "https://api.githubcopilot.com/mcp/",
  "headers": {
    "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
  }
}
```

**环境变量**: 需要设置 `GITHUB_PERSONAL_ACCESS_TOKEN`

**使用场景**:
- Skills 代码管理
- 知识库版本控制
- 规范文档管理

---

## 🔌 飞书集成（API 方式，非 MCP）

**重要说明**: 飞书目前通过 **API 直接访问**，不是 MCP 方式。

### 配置信息
- **App ID**: cli_a9c9443f9278dbd6
- **App Secret**: Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4
- **配置文件**: `_global_config/feishu-config.md`

### 已建立的表格
1. **内容记录** - 记录已发布内容
2. **粉丝数记录** - 跟踪粉丝增长
3. **商品库** - 管理商品信息
4. **选题清单** - 管理选题规划

### Python 脚本
- `check_feishu_tables.py` - 检查表格结构
- `optimize_feishu_tables.py` - 优化表格
- `populate_content_records.py` - 导入内容记录

### 使用方式
在 Skills 的脚本中直接调用飞书 API：
```python
import requests

# 获取 access_token
# 调用飞书 API
# 读取/写入表格数据
```

**详细文档**: 参考 `feishu-setup-report.md`

---

## 🔧 其他可用的 MCP（未配置）

在 `/Users/dj/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/` 目录下还有以下 MCP 可用：

- **asana**: 项目管理
- **context7**: 上下文管理
- **firebase**: Firebase 服务
- **gitlab**: GitLab 版本管理
- **greptile**: 代码搜索
- **laravel-boost**: Laravel 开发
- **linear**: 项目管理
- **serena**: 服务管理
- **slack**: Slack 集成
- **stripe**: 支付集成

**如需启用**: 参考对应目录下的 `.mcp.json` 文件，添加到全局配置中。

---

## 📊 MCP 使用优先级（根据 Skills 需求）

### 必装（已配置）
1. ✅ **Supabase** - 数据存储核心
2. ✅ **Playwright** - 自动化核心
3. ✅ **GitHub** - 版本管理核心

### 推荐安装（待配置）
4. ⏳ **WebResearch** - 内容研究（需要查找配置）
5. ⏳ **Fetch** - 数据抓取（需要查找配置）
6. ⏳ **Google Drive** - 文件管理（需要查找配置）

### 可选安装
7. Slack - 团队协作
8. Firebase - 应用开发
9. Linear - 项目管理

---

## 🔄 配置管理方式

### 统一管理架构
```
源文件: /Users/dj/Desktop/小静的skills/_global_config/.mcp.json
符号链接: ~/.mcp.json → 源文件
```

### 优势
1. **集中管理**: 所有 MCP 配置在一个文件中
2. **可迁移**: 换电脑时只需迁移 skills 文件夹
3. **一致性**: 与 Skills、Hooks 使用相同的管理方式
4. **版本控制**: 可以纳入 Git 管理

---

## 🚀 启用新的 MCP

### 步骤
1. 编辑配置文件:
   ```bash
   vim /Users/dj/Desktop/小静的skills/_global_config/.mcp.json
   ```

2. 添加新的 MCP 配置（参考已有格式）

3. 重启 Claude Code 使配置生效

4. 验证 MCP 是否可用

---

## 📝 环境变量配置

某些 MCP 需要环境变量（如 GitHub Token）。配置方式：

### 方法1: 在 settings.json 中配置
```json
{
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
  }
}
```

### 方法2: 在 shell 配置文件中设置
```bash
# ~/.zshrc 或 ~/.bashrc
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token_here"
```

---

## 🔍 故障排查

### MCP 无法启用
1. 检查配置文件语法是否正确
2. 检查符号链接是否有效: `ls -la ~/.mcp.json`
3. 重启 Claude Code
4. 查看 Claude Code 日志

### MCP 工具不可用
1. 检查环境变量是否设置
2. 检查网络连接（HTTP 类型的 MCP）
3. 检查命令是否可执行（命令行类型的 MCP）

---

## 📚 参考文档

- Skills 与 MCP 搭配使用清单: `/Users/dj/Desktop/Skills与MCP搭配使用清单.md`
- 近期行动清单: `/Users/dj/Desktop/近期行动清单-系统优化与工具整合.md`

---

**最后更新**: 2026-02-05
**维护者**: Claude Code
