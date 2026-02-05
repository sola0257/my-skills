# 飞书 MCP 服务器设置指南

**创建日期**: 2026-02-05
**版本**: v1.0

## 概述

飞书 MCP (Model Context Protocol) 服务器允许 Claude Code 直接调用飞书 API，实现内容记录、商品管理、粉丝数跟踪等功能。

## 已完成的配置

### 1. MCP 服务器文件

**位置**: `/Users/dj/Desktop/小静的skills/_global_config/feishu_mcp_server.py`

**功能**:
- 飞书 API 认证和令牌管理
- 添加内容记录
- 列出内容记录
- 添加商品
- 更新粉丝数

### 2. MCP 配置文件

**位置**: `/Users/dj/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/feishu/.mcp.json`

**配置内容**:
```json
{
  "feishu": {
    "command": "python3",
    "args": [
      "/Users/dj/Desktop/小静的skills/_global_config/feishu_mcp_server.py"
    ],
    "env": {
      "FEISHU_APP_ID": "cli_a9c9443f9278dbd6",
      "FEISHU_APP_SECRET": "Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4"
    }
  }
}
```

## 安装步骤

### Step 1: 安装 MCP Python SDK

```bash
pip3 install mcp
```

### Step 2: 验证安装

```bash
python3 -c "import mcp; print('MCP installed successfully')"
```

### Step 3: 测试 MCP 服务器

```bash
python3 /Users/dj/Desktop/小静的skills/_global_config/feishu_mcp_server.py
```

如果没有错误，说明服务器可以正常启动。

### Step 4: 重启 Claude Code

重启 Claude Code 以加载新的 MCP 服务器。

## 可用的 MCP 工具

### 1. feishu_add_content_record

添加内容记录到飞书。

**参数**:
- `title` (必需): 内容标题
- `platform` (必需): 平台名称 (如: 微信公众号-订阅号, 小红书)
- `content_type` (必需): 内容类型 (如: 长文, 图文)
- `date` (必需): 发布日期 (YYYY-MM-DD)
- `file_path` (可选): 本地文件路径

**示例**:
```python
# 在 Claude Code 中调用
mcp__feishu__feishu_add_content_record({
    "title": "春季养花指南",
    "platform": "微信公众号-订阅号",
    "content_type": "长文",
    "date": "2026-02-05",
    "file_path": "/Users/dj/Desktop/content/..."
})
```

### 2. feishu_list_content_records

列出最近的内容记录。

**参数**:
- `page_size` (可选): 返回记录数 (默认: 20)

**示例**:
```python
mcp__feishu__feishu_list_content_records({
    "page_size": 10
})
```

### 3. feishu_add_product

添加商品到商品库。

**参数**:
- `name` (必需): 商品名称
- `category` (必需): 商品分类
- `price` (必需): 商品价格
- `stock` (可选): 库存数量
- `link` (可选): 商品链接

**示例**:
```python
mcp__feishu__feishu_add_product({
    "name": "多肉植物组合",
    "category": "多肉",
    "price": 39.9,
    "stock": 100,
    "link": "https://..."
})
```

### 4. feishu_update_fans_count

更新平台粉丝数。

**参数**:
- `platform` (必需): 平台名称
- `fans_count` (必需): 当前粉丝数
- `date` (必需): 日期 (YYYY-MM-DD)

**示例**:
```python
mcp__feishu__feishu_update_fans_count({
    "platform": "小红书",
    "fans_count": 520,
    "date": "2026-02-05"
})
```

## 集成到 Skills

### 在 wechat-content-generator 中使用

在 `scripts/wechat_publish.py` 的推送成功后添加:

```python
# 推送成功后，调用飞书 MCP 添加记录
# Claude Code 会自动调用 MCP 工具
```

在 SKILL.md 中添加步骤:

```markdown
### Step X: 同步到飞书

使用 MCP 工具将内容记录同步到飞书:
- 调用 feishu_add_content_record
- 传入标题、平台、内容类型、日期等信息
```

## 故障排除

### 问题 1: MCP 包未安装

**错误**: `ModuleNotFoundError: No module named 'mcp'`

**解决**:
```bash
pip3 install mcp
```

### 问题 2: 飞书 API 认证失败

**错误**: `Failed to get access token`

**解决**:
- 检查 APP_ID 和 APP_SECRET 是否正确
- 确认飞书应用权限已开启

### 问题 3: MCP 服务器未加载

**解决**:
1. 检查 `.mcp.json` 文件是否存在
2. 重启 Claude Code
3. 运行 `/mcp` 命令查看已连接的 MCP 服务器

## 下一步

1. **测试 MCP 工具**: 在 Claude Code 中测试每个工具
2. **集成到 Skills**: 修改 content-generator Skills 以使用 MCP
3. **添加更多工具**: 根据需要添加更多飞书操作 (如查询、更新、删除等)
4. **错误处理**: 完善错误处理和重试逻辑

## 技术细节

### MCP 协议

MCP (Model Context Protocol) 是一个标准协议，允许 AI 模型通过工具调用与外部服务交互。

**工作流程**:
1. Claude Code 启动时加载 MCP 配置
2. 启动 MCP 服务器进程
3. Claude 通过 stdio 与 MCP 服务器通信
4. MCP 服务器调用飞书 API
5. 返回结果给 Claude

### 飞书 API

**认证**: 使用 tenant_access_token
**端点**: `https://open.feishu.cn/open-api/`
**文档**: https://open.feishu.cn/document/

## 参考资料

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [飞书开放平台文档](https://open.feishu.cn/document/)
- [Claude Code MCP 指南](https://docs.anthropic.com/claude/docs/mcp)

---

**最后更新**: 2026-02-05
**维护者**: Claude Code
