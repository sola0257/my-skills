# Feishu 数据导入完整指南

## 概述

本指南记录了将微信公众号文章数据导入到飞书多维表格的完整方法，包括直接 API 调用和 MCP 工具两种方式。

## 飞书配置信息

### 应用凭证
- **App ID**: `cli_a9c9443f9278dbd6`
- **App Secret**: `Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4`

### 多维表格配置
- **表格名称**: 慢养四季运营数据库
- **App Token**: `N42HbN11JaIxxgstE4gcRdl0nPf`
- **Table ID (内容记录)**: `tbltqXWK6ozCXAXo`
- **Table ID (商品库)**: `tblYfRNXXeqn57q0`
- **Table ID (粉丝数记录)**: `tblgmTuHejIoWu2i`
- **Table ID (选题清单)**: 待补充

### 平台命名规范

**重要**：所有平台字段必须使用以下统一命名：

| 平台类型 | 标准命名 | 说明 |
|---------|---------|------|
| 微信订阅号 | `微信公众号-订阅号` | 个人或企业订阅号 |
| 微信服务号 | `微信公众号-服务号` | 企业服务号 |
| 微信视频号 | `视频号` | 微信视频号 |
| 小红书 | `小红书` | 小红书平台 |
| 抖音 | `抖音` | 抖音平台 |
| 快手 | `快手` | 快手平台 |

**注意**：
- ❌ 不要使用 `微信公众号`（不明确是订阅号还是服务号）
- ✅ 必须明确区分 `微信公众号-订阅号` 和 `微信公众号-服务号`
- ✅ 视频号单独使用 `视频号`，不加"微信"前缀

### 表格字段（内容记录表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 日期 | DateTime | 记录日期（时间戳，毫秒） |
| 标题 | Text | 内容标题 |
| 平台 | SingleSelect | 平台名称（微信公众号-订阅号/小红书/视频号等） |
| 内容类型 | SingleSelect | 内容类型（长文/图文/视频等） |
| 发布时间 | DateTime | 实际发布时间（时间戳，毫秒） |
| 曝光量 | Number | 内容曝光量 |
| 点击量 | Number | 内容点击量 |
| 互动量 | Number | 互动总量（点赞+分享+收藏+评论） |
| 合集 | Text | 所属合集名称 |
| 本地文件路径 | Text | 本地文件路径 |
| 发布状态 | SingleSelect | 发布状态（已发布/草稿/待发布） |
| 备注 | Text | 备注信息 |

**重要说明**：
- **日期 vs 发布时间**：
  - `日期`：记录创建日期，用于数据管理和排序
  - `发布时间`：内容实际发布的时间，用于统计分析
  - 两者可以相同（导入已发布内容时），也可以不同（提前创建记录时）

## 方法一：直接 API 调用（推荐用于批量导入）

### 适用场景
- 批量导入大量数据（>10条）
- 需要完整字段支持
- 一次性数据迁移

### 实现步骤

#### 1. 获取 tenant_access_token

```python
import requests

def get_tenant_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    data = {
        'app_id': 'cli_a9c9443f9278dbd6',
        'app_secret': 'Nzkl6zFqpJ1hZ6oNJgz3Se0UhQsdUst4'
    }
    response = requests.post(url, json=data)
    result = response.json()

    if result.get('code') == 0:
        return result['tenant_access_token']
    else:
        raise Exception(f"获取token失败: {result}")
```

#### 2. 批量添加记录

```python
def batch_add_records(access_token, records_list):
    """
    批量添加记录到飞书表格

    Args:
        access_token: tenant_access_token
        records_list: 记录列表，每个记录是一个字典
    """
    app_token = 'N42HbN11JaIxxgstE4gcRdl0nPf'
    table_id = 'tbltqXWK6ozCXAXo'

    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # 每次最多500条
    batch_size = 500
    for i in range(0, len(records_list), batch_size):
        batch = records_list[i:i + batch_size]
        data = {
            'records': [{'fields': record} for record in batch]
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if result.get('code') == 0:
            print(f"成功导入 {len(batch)} 条记录")
        else:
            print(f"导入失败: {result}")
```

#### 3. 数据格式转换

```python
from datetime import datetime

def convert_article_to_record(article):
    """
    将文章数据转换为飞书记录格式

    Args:
        article: 文章数据字典

    Returns:
        飞书记录字典
    """
    # 转换发布时间为时间戳（毫秒）
    publish_time = article.get('publishTime', '')
    if publish_time:
        try:
            dt = datetime.strptime(publish_time, '%Y年%m月%d日')
            publish_timestamp = int(dt.timestamp() * 1000)
        except:
            publish_timestamp = None
    else:
        publish_timestamp = None

    # 计算互动量
    likes = article.get('likes', 0)
    shares = article.get('shares', 0)
    favorites = article.get('favorites', 0)
    comments = article.get('comments', 0)
    interaction = likes + shares + favorites + comments

    # 构建记录
    record = {
        '标题': article.get('title', ''),
        '平台': '微信公众号-订阅号',
        '内容类型': article.get('collection_type', ''),
        '发布时间': publish_timestamp,
        '日期': publish_timestamp,  # 对于已发布内容，日期=发布时间
        '曝光量': article.get('views', 0),
        '点击量': article.get('views', 0),  # 微信公众号的阅读量即点击量
        '互动量': interaction,
        '合集': article.get('collection_name', ''),
        '发布状态': '已发布'
    }

    return record
```

#### 4. 完整导入流程

```python
def import_articles_to_feishu(articles_file):
    """
    完整的文章导入流程

    Args:
        articles_file: 文章数据JSON文件路径
    """
    import json

    # 1. 读取文章数据
    with open(articles_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # 2. 获取access token
    access_token = get_tenant_access_token()

    # 3. 转换数据格式
    records = [convert_article_to_record(article) for article in articles]

    # 4. 批量导入
    batch_add_records(access_token, records)

    print(f"导入完成，共 {len(records)} 条记录")
```

### 使用示例

```python
# 导入文章数据
import_articles_to_feishu('wechat_articles_data_with_collections.json')
```

## 方法二：使用 MCP 工具（推荐用于日常操作）

### 适用场景
- 单条或少量记录添加（<10条）
- 日常内容记录
- 与 Claude 对话中直接操作

### MCP 工具说明

MCP 服务器位置：`/Users/dj/Desktop/小静的skills/_global_config/feishu_mcp_server.py`

#### 可用工具

1. **feishu_add_content_record** - 添加内容记录
   ```
   参数：
   - title: 内容标题
   - platform: 平台名称（如：微信公众号-订阅号）
   - content_type: 内容类型（如：长文、图文）
   - date: 发布日期（YYYY-MM-DD格式）
   - file_path: 本地文件路径（可选）
   ```

2. **feishu_list_content_records** - 列出内容记录
   ```
   参数：
   - page_size: 返回记录数量（默认20）
   ```

3. **feishu_add_product** - 添加商品
   ```
   参数：
   - name: 商品名称
   - category: 商品分类
   - price: 商品价格
   - stock: 库存数量（可选）
   - link: 商品链接（可选）
   ```

4. **feishu_update_fans_count** - 更新粉丝数
   ```
   参数：
   - platform: 平台名称
   - fans_count: 粉丝数量
   - date: 日期（YYYY-MM-DD格式）
   ```

### MCP 工具限制

当前 MCP 工具的限制：
- ❌ 不支持批量操作（每次只能添加一条记录）
- ❌ 不支持完整字段（缺少：发布时间、曝光量、点击量、互动量、合集、发布状态等）
- ❌ 不支持删除操作
- ❌ 不支持按字段查询（无法查找重复记录）
- ❌ 不支持更新记录

**建议**：
- 批量导入使用方法一（直接 API 调用）
- 日常单条记录使用 MCP 工具
- 需要完整字段时使用方法一

## 常见问题处理

### 1. 删除重复记录

当表格中存在重复记录时，需要手动删除或使用 API 删除：

```python
def delete_record(access_token, record_id):
    """
    删除指定记录

    Args:
        access_token: tenant_access_token
        record_id: 记录ID
    """
    app_token = 'N42HbN11JaIxxgstE4gcRdl0nPf'
    table_id = 'tbltqXWK6ozCXAXo'

    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.delete(url, headers=headers)
    return response.json()

def find_and_delete_duplicates(access_token):
    """
    查找并删除重复记录（保留有本地文件路径的记录）
    """
    # 1. 获取所有记录
    records = list_all_records(access_token)

    # 2. 按标题分组
    title_groups = {}
    for record in records:
        title = record['fields'].get('标题', '')
        if title not in title_groups:
            title_groups[title] = []
        title_groups[title].append(record)

    # 3. 处理重复记录
    for title, group in title_groups.items():
        if len(group) > 1:
            # 找到有本地文件路径的记录
            records_with_path = [r for r in group if r['fields'].get('本地文件路径')]
            records_without_path = [r for r in group if not r['fields'].get('本地文件路径')]

            # 如果有带路径的记录，删除不带路径的
            if records_with_path:
                for record in records_without_path:
                    print(f"删除重复记录（无路径）: {title}")
                    delete_record(access_token, record['record_id'])
            else:
                # 如果都没有路径，保留第一条，删除其他
                for record in group[1:]:
                    print(f"删除重复记录: {title}")
                    delete_record(access_token, record['record_id'])

def list_all_records(access_token):
    """
    获取所有记录（处理分页）
    """
    app_token = 'N42HbN11JaIxxgstE4gcRdl0nPf'
    table_id = 'tbltqXWK6ozCXAXo'

    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    all_records = []
    page_token = None

    while True:
        params = {'page_size': 500}
        if page_token:
            params['page_token'] = page_token

        response = requests.get(url, headers=headers, params=params)
        result = response.json()

        if result.get('code') == 0:
            items = result.get('data', {}).get('items', [])
            all_records.extend(items)

            page_token = result.get('data', {}).get('page_token')
            if not page_token:
                break
        else:
            raise Exception(f"获取记录失败: {result}")

    return all_records
```

### 2. 更新记录字段

为已存在的记录补充字段（如本地文件路径、发布状态）：

```python
def update_record_fields(access_token, record_id, fields):
    """
    更新记录字段

    Args:
        access_token: tenant_access_token
        record_id: 记录ID
        fields: 要更新的字段字典
    """
    app_token = 'N42HbN11JaIxxgstE4gcRdl0nPf'
    table_id = 'tbltqXWK6ozCXAXo'

    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    data = {'fields': fields}

    response = requests.put(url, headers=headers, json=data)
    return response.json()

# 使用示例：为记录补充本地文件路径
access_token = get_tenant_access_token()
update_record_fields(
    access_token,
    'recXXXXXXXXXXXX',
    {
        '本地文件路径': '/path/to/file.md',
        '发布状态': '已发布'
    }
)
```

### 3. 时间格式转换问题

**问题**：某些日期格式无法转换为时间戳

**原因**：日期格式不统一（如"2025年12月31日" vs "2025-12-31"）

**解决方案**：

```python
from datetime import datetime

def parse_date_flexible(date_str):
    """
    灵活解析多种日期格式

    Args:
        date_str: 日期字符串

    Returns:
        时间戳（毫秒）或 None
    """
    if not date_str:
        return None

    formats = [
        '%Y年%m月%d日',
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%Y.%m.%d'
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return int(dt.timestamp() * 1000)
        except:
            continue

    print(f"警告：无法解析日期格式: {date_str}")
    return None
```

### 4. 空发布时间问题

**问题**：导入后某些记录的发布时间为空

**原因**：
1. 原始数据中 `publishTime` 字段为空
2. 日期格式无法解析
3. 数据转换时出错

**排查方法**：

```python
# 检查原始数据
with open('wechat_articles_data_with_collections.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

for article in articles:
    if not article.get('publishTime'):
        print(f"缺少发布时间: {article.get('title')}")
```

## API 参考

### 飞书开放平台 API 文档
- 官方文档：https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-table-record/create
- 认证方式：tenant_access_token
- 批量创建限制：每次最多 500 条记录

### 常用 API 端点

| 功能 | 方法 | 端点 |
|------|------|------|
| 获取 token | POST | `/open-apis/auth/v3/tenant_access_token/internal` |
| 添加记录 | POST | `/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records` |
| 批量添加 | POST | `/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create` |
| 列出记录 | GET | `/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records` |
| 更新记录 | PUT | `/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}` |
| 删除记录 | DELETE | `/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}` |
| 获取字段 | GET | `/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields` |

## 完整脚本位置

- **批量导入脚本**：`/Users/dj/Desktop/小静的skills/_global_config/wechat-scraping/import_to_feishu_v2.py`
- **字段获取脚本**：`/Users/dj/Desktop/小静的skills/_global_config/wechat-scraping/get_feishu_fields.py`
- **MCP 服务器**：`/Users/dj/Desktop/小静的skills/_global_config/feishu_mcp_server.py`
- **数据文件**：`/Users/dj/Desktop/小静的skills/_global_config/wechat-scraping/wechat_articles_data_with_collections.json`

## 下一步计划

### 待添加功能
1. **粉丝数抓取**：明天早上 9 点后可获取粉丝数数据，需要添加到抓取脚本中
2. **MCP 工具增强**：
   - 添加批量操作支持
   - 添加完整字段支持
   - 添加删除和更新功能
   - 添加按字段查询功能

### 建议改进
1. 统一日期格式处理
2. 添加数据验证机制
3. 添加错误重试逻辑
4. 添加导入日志记录

