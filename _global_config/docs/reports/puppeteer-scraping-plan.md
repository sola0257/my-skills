# Puppeteer MCP 抓取方案

**版本**: v1.0
**日期**: 2026-02-05
**目标**: 从微信公众号后台抓取真实发布的内容数据

---

## 一、Puppeteer MCP 基础

### 1.1 什么是 Puppeteer MCP

Puppeteer MCP 是一个 Model Context Protocol 服务器，允许 Claude 通过 Puppeteer 控制浏览器，执行以下操作：
- 打开网页
- 点击元素
- 填写表单
- 执行 JavaScript
- 截图
- 抓取数据

### 1.2 安装和配置

Puppeteer MCP 已经安装在您的系统中（根据之前的对话）。

---

## 二、微信公众号后台抓取方案

### 2.1 目标数据

从公众号后台抓取以下数据：

| 字段 | 数据来源 | 优先级 |
|------|---------|--------|
| 标题 | 已发布文章列表 | P0 |
| 发布时间 | 已发布文章列表 | P0 |
| 内容类型 | 文章详情（图文/长文） | P0 |
| 合集 | 文章详情 | P1 |
| 阅读数 | 数据统计 | P1 |
| 在看数 | 数据统计 | P1 |
| 分享数 | 数据统计 | P2 |
| 收藏数 | 数据统计 | P2 |

### 2.2 抓取流程

```
1. 登录公众号后台
   ↓
2. 进入"已发表"页面
   ↓
3. 获取文章列表
   ↓
4. 遍历每篇文章
   ↓
5. 获取文章详情和数据
   ↓
6. 更新飞书表格
```

### 2.3 关键 URL

- 登录页面: `https://mp.weixin.qq.com/`
- 已发表列表: `https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list`
- 数据统计: `https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_list`

---

## 三、技术实现

### 3.1 登录方案

**方案 A: 扫码登录（推荐）**
```python
# 1. 打开登录页面
# 2. 等待二维码出现
# 3. 截图保存二维码
# 4. 提示用户扫码
# 5. 等待登录成功
# 6. 保存 cookies
```

**优点**: 安全，不需要存储密码
**缺点**: 需要手动扫码

**方案 B: Cookie 复用**
```python
# 1. 首次手动登录并保存 cookies
# 2. 后续使用保存的 cookies
# 3. Cookie 过期时重新登录
```

**优点**: 自动化程度高
**缺点**: 需要定期更新 cookies

### 3.2 数据抓取代码示例

```python
import asyncio
from pyppeteer import launch

async def scrape_wechat_articles():
    """抓取微信公众号已发布文章"""

    # 1. 启动浏览器
    browser = await launch(
        headless=False,  # 显示浏览器窗口
        args=['--no-sandbox']
    )
    page = await browser.newPage()

    # 2. 加载 cookies（如果有）
    cookies = load_cookies()
    if cookies:
        await page.setCookie(*cookies)

    # 3. 访问已发表页面
    await page.goto('https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list')

    # 4. 等待页面加载
    await page.waitForSelector('.appmsg-list')

    # 5. 提取文章列表
    articles = await page.evaluate('''() => {
        const items = document.querySelectorAll('.appmsg-list-item');
        return Array.from(items).map(item => ({
            title: item.querySelector('.title').textContent.trim(),
            publish_time: item.querySelector('.time').textContent.trim(),
            url: item.querySelector('a').href,
        }));
    }''')

    # 6. 遍历文章获取详细数据
    for article in articles:
        # 访问文章详情页
        await page.goto(article['url'])

        # 提取合集信息
        collection = await page.evaluate('''() => {
            const elem = document.querySelector('.collection-name');
            return elem ? elem.textContent.trim() : null;
        }''')

        article['collection'] = collection

        # 获取数据统计
        stats = await get_article_stats(page, article['url'])
        article.update(stats)

    # 7. 关闭浏览器
    await browser.close()

    return articles

async def get_article_stats(page, article_url):
    """获取文章数据统计"""
    # 进入数据统计页面
    await page.goto('https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_list')

    # 搜索文章
    await page.type('#search_input', article_url)
    await page.click('#search_btn')

    # 等待结果
    await page.waitForSelector('.table_item')

    # 提取数据
    stats = await page.evaluate('''() => {
        const row = document.querySelector('.table_item');
        return {
            read_count: row.querySelector('.read_count').textContent.trim(),
            like_count: row.querySelector('.like_count').textContent.trim(),
            share_count: row.querySelector('.share_count').textContent.trim(),
        };
    }''')

    return stats
```

### 3.3 与飞书集成

```python
def sync_to_feishu(articles):
    """将抓取的数据同步到飞书"""
    from feishu_api import FeishuAPI

    feishu = FeishuAPI(APP_ID, APP_SECRET)

    for article in articles:
        # 根据标题查找现有记录
        record = feishu.get_record_by_title(article['title'])

        if record:
            # 更新现有记录
            feishu.update_content_record(record['record_id'], {
                "发布时间": article['publish_time'],
                "合集": article['collection'],
                "曝光量": article['read_count'],
                "互动量": article['like_count'],
                "发布状态": "已发布",
            })
        else:
            # 创建新记录
            feishu.add_content_record({
                "标题": article['title'],
                "发布时间": article['publish_time'],
                "合集": article['collection'],
                "平台": "微信公众号-订阅号",
                "发布状态": "已发布",
            })
```

---

## 四、实施步骤

### Phase 1: 基础验证（今天）

**目标**: 验证 Puppeteer MCP 能否正常工作

**步骤**:
1. 创建测试脚本 `test_puppeteer.py`
2. 测试打开微信公众号登录页
3. 测试扫码登录
4. 测试保存 cookies
5. 测试访问已发表页面

**预期结果**: 能够成功登录并访问后台

### Phase 2: 数据抓取（明天）

**目标**: 实现文章列表抓取

**步骤**:
1. 编写文章列表抓取逻辑
2. 测试提取标题、发布时间
3. 测试提取合集信息
4. 验证数据准确性

**预期结果**: 能够获取所有已发布文章的基本信息

### Phase 3: 数据统计（后天）

**目标**: 抓取文章数据统计

**步骤**:
1. 研究数据统计页面结构
2. 编写数据抓取逻辑
3. 测试阅读数、在看数等指标
4. 处理数据格式转换

**预期结果**: 能够获取文章的完整数据

### Phase 4: 飞书集成（本周末）

**目标**: 将抓取的数据同步到飞书

**步骤**:
1. 实现数据匹配逻辑（根据标题）
2. 实现数据更新逻辑
3. 处理新文章和已有文章
4. 测试完整流程

**预期结果**: 自动化数据同步完成

### Phase 5: 定时任务（下周）

**目标**: 设置每日自动抓取

**步骤**:
1. 优化脚本性能
2. 添加错误处理
3. 设置 cron 定时任务
4. 添加日志和监控

**预期结果**: 每天自动更新数据

---

## 五、注意事项

### 5.1 反爬虫对策

- 使用真实的浏览器环境（Puppeteer）
- 添加随机延迟（1-3秒）
- 模拟人类操作（滚动、移动鼠标）
- 使用已登录的 cookies

### 5.2 数据准确性

- 以平台数据为准，不以本地文件为准
- 定期验证数据一致性
- 记录抓取时间戳

### 5.3 安全性

- Cookies 加密存储
- 不在代码中硬编码密码
- 定期更新 cookies

---

## 六、测试脚本

创建 `test_puppeteer_mcp.py` 进行基础测试：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Puppeteer MCP 基础测试
测试是否能够正常使用 Puppeteer 控制浏览器
"""

import asyncio
from pyppeteer import launch

async def test_basic():
    """基础测试：打开网页并截图"""
    print("🚀 启动浏览器...")
    browser = await launch(
        headless=False,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )

    page = await browser.newPage()

    print("📄 访问微信公众号登录页...")
    await page.goto('https://mp.weixin.qq.com/')

    print("📸 截图...")
    await page.screenshot({'path': 'wechat_login.png'})

    print("✅ 测试完成！请查看 wechat_login.png")

    # 等待用户查看
    await asyncio.sleep(5)

    await browser.close()

if __name__ == "__main__":
    asyncio.run(test_basic())
```

---

## 七、下一步行动

**今天立即可以做的**:

1. **安装依赖** (5分钟)
   ```bash
   pip3 install pyppeteer
   ```

2. **运行测试脚本** (10分钟)
   ```bash
   python3 test_puppeteer_mcp.py
   ```

3. **验证登录流程** (15分钟)
   - 手动扫码登录
   - 保存 cookies
   - 测试 cookies 复用

**预期成果**: 今天结束时，能够通过 Puppeteer 自动登录微信公众号后台

---

**文档版本**: v1.0
**最后更新**: 2026-02-05
