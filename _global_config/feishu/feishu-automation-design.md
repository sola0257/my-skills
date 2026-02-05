# 飞书运营数据库自动化流程设计

**版本**: v1.0
**日期**: 2026-02-05
**目标**: 实现内容发布后自动同步到飞书，并定期抓取账号数据用于复盘

---

## 一、整体架构

```
内容发布 → 本地记录 → 飞书同步 → 数据抓取 → 复盘分析
   ↓          ↓          ↓          ↓          ↓
 Skill    文件系统    飞书API   Puppeteer   飞书表格
```

---

## 二、自动化流程设计

### 流程 A：内容发布时自动同步（实时）

**触发时机**: 每次内容发布成功后

**执行步骤**:
1. content-generator 生成内容并保存到本地
2. 推送到平台（微信/小红书/视频号等）
3. **新增**: 自动调用飞书同步函数
4. 将内容元数据写入飞书"内容记录"表

**需要修改的 Skills**:
- `wechat-content-generator`
- `xiaohongshu-content-generator`
- `video-script-generator`

**实现方式**:
```python
# 在每个 content-generator 的推送成功后添加
def sync_to_feishu(content_metadata):
    """同步内容记录到飞书"""
    # 1. 获取飞书 access token
    # 2. 构建记录数据
    # 3. 调用飞书 API 添加记录
    pass
```

---

### 流程 B：定期抓取账号数据（每日）

**触发时机**: 每天晚上 23:00 自动执行

**执行步骤**:
1. 使用 Puppeteer MCP 登录各平台后台
2. 抓取已发布内容的数据（曝光量、点击量、互动量等）
3. 更新飞书"内容记录"表的对应字段
4. 计算"数据表现"（公式字段）
5. 标记"是否爆文"

**需要抓取的数据**:

| 平台 | 数据来源 | 抓取字段 |
|------|---------|---------|
| 微信公众号 | 公众号后台 | 阅读数、在看数、分享数、收藏数 |
| 小红书 | 创作者中心 | 曝光量、点击量、点赞数、收藏数、评论数 |
| 视频号 | 视频号助手 | 播放量、点赞数、评论数、转发数 |
| 快手 | 创作者中心 | 播放量、点赞数、评论数、分享数 |
| 抖音 | 创作者服务中心 | 播放量、点赞数、评论数、分享数 |

**实现方式**:
```python
# 创建新的 skill: feishu-data-sync
def scrape_account_data(platform):
    """使用 Puppeteer 抓取账号数据"""
    # 1. 启动 Puppeteer
    # 2. 登录平台后台
    # 3. 遍历已发布内容
    # 4. 抓取数据
    # 5. 更新飞书表格
    pass
```

---

### 流程 C：手动批量同步（按需）

**触发时机**: 用户手动执行

**使用场景**:
- 初次设置时批量导入历史数据
- 数据丢失后重新同步
- 切换数据源后重新导入

**执行命令**:
```bash
python3 reset_and_populate_feishu.py
```

---

## 三、技术实现方案

### 3.1 飞书 API 封装

创建统一的飞书 API 工具类：

**文件位置**: `/Users/dj/Desktop/小静的skills/_global_config/feishu_api.py`

**核心功能**:
```python
class FeishuAPI:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None

    def get_access_token(self):
        """获取访问令牌"""
        pass

    def add_content_record(self, record_data):
        """添加内容记录"""
        pass

    def update_content_record(self, record_id, update_data):
        """更新内容记录"""
        pass

    def get_record_by_title(self, title):
        """根据标题查找记录"""
        pass
```

### 3.2 Puppeteer MCP 集成

**使用场景**:
1. 登录各平台后台
2. 抓取内容数据
3. 截图保存（用于复盘）

**示例代码**:
```python
# 使用 Puppeteer MCP 抓取微信公众号数据
async def scrape_wechat_data():
    # 1. 启动浏览器
    browser = await puppeteer.launch()
    page = await browser.newPage()

    # 2. 登录公众号后台
    await page.goto('https://mp.weixin.qq.com/')
    # ... 登录逻辑

    # 3. 进入图文分析页面
    await page.goto('https://mp.weixin.qq.com/cgi-bin/appmsgpublish')

    # 4. 抓取数据
    articles = await page.evaluate('''() => {
        // 提取文章列表和数据
        return Array.from(document.querySelectorAll('.article-item')).map(item => ({
            title: item.querySelector('.title').textContent,
            read_count: item.querySelector('.read-count').textContent,
            like_count: item.querySelector('.like-count').textContent,
        }))
    }''')

    # 5. 更新飞书
    for article in articles:
        update_feishu_record(article)
```

### 3.3 Skills 集成

**修改点 1: wechat-content-generator**

在 `scripts/wechat_publish.py` 的推送成功后添加：

```python
# 推送成功后
if result['success']:
    # 原有逻辑...

    # 新增：同步到飞书
    from feishu_api import FeishuAPI
    feishu = FeishuAPI(APP_ID, APP_SECRET)
    feishu.add_content_record({
        "日期": int(datetime.now().timestamp() * 1000),
        "标题": title,
        "平台": "微信公众号-订阅号",
        "内容类型": "长文",
        "本地文件路径": output_dir,
    })
```

**修改点 2: xiaohongshu-content-generator**

类似的，在发布成功后添加飞书同步逻辑。

---

## 四、定时任务设置

### 方案 A: 使用 cron（推荐）

**设置步骤**:
```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天 23:00 执行）
0 23 * * * cd /Users/dj/Desktop/小静的skills/_global_config && python3 scrape_and_sync.py >> /tmp/feishu_sync.log 2>&1
```

### 方案 B: 使用 launchd（macOS 原生）

创建 plist 文件：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.feishu.datasync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/dj/Desktop/小静的skills/_global_config/scrape_and_sync.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>23</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

---

## 五、数据字段映射

### 内容记录表字段

| 字段名 | 类型 | 数据来源 | 更新时机 |
|--------|------|---------|---------|
| 日期 | Date | 发布时间 | 发布时 |
| 发布时间 | Date | 推送结果 | 发布时 |
| 标题 | Text | 文案 | 发布时 |
| 平台 | Select | 固定值 | 发布时 |
| 内容类型 | Select | 固定值 | 发布时 |
| 本地文件路径 | Text | 保存路径 | 发布时 |
| 曝光量 | Number | Puppeteer 抓取 | 每日更新 |
| 点击量 | Number | Puppeteer 抓取 | 每日更新 |
| 互动量 | Number | Puppeteer 抓取 | 每日更新 |
| 转化量 | Number | Puppeteer 抓取 | 每日更新 |
| 数据表现 | Formula | 自动计算 | 实时 |
| 是否爆文 | Checkbox | 自动判断 | 每日更新 |
| 复盘说明 | Text | 手动填写 | 按需 |

### 爆文判断标准

```python
def is_viral_content(platform, metrics):
    """判断是否为爆文"""
    standards = {
        "微信公众号-订阅号": {
            "阅读数": 1000,  # 起号期标准
            "在看数": 50,
        },
        "小红书": {
            "曝光量": 10000,
            "点赞数": 100,
        },
        # ... 其他平台
    }

    # 判断逻辑
    return metrics['read_count'] >= standards[platform]['阅读数']
```

---

## 六、实施计划

### Phase 1: 基础设施（本周）
- [x] 创建飞书表格结构
- [x] 实现基础 API 封装
- [x] 实现批量导入脚本
- [ ] 创建 `feishu_api.py` 工具类

### Phase 2: 实时同步（下周）
- [ ] 修改 `wechat-content-generator`
- [ ] 修改 `xiaohongshu-content-generator`
- [ ] 修改 `video-script-generator`
- [ ] 测试实时同步功能

### Phase 3: 数据抓取（下下周）
- [ ] 研究 Puppeteer MCP 使用方法
- [ ] 实现微信公众号数据抓取
- [ ] 实现小红书数据抓取
- [ ] 实现其他平台数据抓取
- [ ] 设置定时任务

### Phase 4: 优化与监控（持续）
- [ ] 添加错误处理和重试机制
- [ ] 添加日志记录
- [ ] 添加数据验证
- [ ] 创建监控面板

---

## 七、注意事项

### 7.1 数据安全
- 飞书 API 凭证不要提交到 Git
- Puppeteer 登录凭证加密存储
- 定期备份飞书数据

### 7.2 性能优化
- 批量操作使用批量 API
- 避免频繁调用 API（使用缓存）
- Puppeteer 使用无头模式

### 7.3 错误处理
- API 调用失败时重试 3 次
- 记录所有错误到日志文件
- 关键错误发送通知

---

## 八、下一步行动

**今天可以做的 3 件事**:

1. **创建 feishu_api.py 工具类** (30分钟)
   - 封装所有飞书 API 调用
   - 提供统一的接口给其他 Skills 使用

2. **修改 wechat-content-generator** (1小时)
   - 在推送成功后添加飞书同步逻辑
   - 测试是否能正常写入

3. **研究 Puppeteer MCP 文档** (1小时)
   - 了解如何使用 Puppeteer MCP
   - 编写一个简单的测试脚本抓取微信公众号数据

**本周可以完成**:
- Phase 1 的所有任务
- Phase 2 的部分任务（至少完成微信公众号的实时同步）

---

**文档版本**: v1.0
**最后更新**: 2026-02-05
