# Skills 可视化管理平台 - 架构设计文档

**项目名称**: Xiaohongshu Content Platform (小红书内容管理平台)
**版本**: v1.0.0
**设计日期**: 2026-02-06
**状态**: 架构设计阶段

---

## 一、项目概述

### 1.1 项目目标

为 xiaohongshu-content-generator skill 创建一个轻量级的 Web 可视化管理平台，让用户通过浏览器界面完成小红书内容的创建、管理和发布，无需使用命令行。

### 1.2 核心价值

- **降低使用门槛**: 从命令行操作转为可视化界面
- **提升效率**: 批量操作、模板管理、历史记录
- **数据可视化**: 飞书多维表格展示内容数据和统计
- **移动友好**: PWA 支持，像原生 App 一样使用
- **模块化设计**: 每个功能独立使用，灵活组合
- **智能通知**: 推送通知，及时了解内容状态
- **可扩展**: 未来可整合其他平台的 skills

### 1.3 用户场景

**主要用户**: 你（小静）
**使用场景**:
1. 每周规划内容选题
2. 生成小红书笔记（文案+配图）
3. 预览和编辑生成的内容
4. 推送到小红书草稿箱
5. 查看历史内容和数据统计
6. 发现热门选题

---

## 二、技术架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                      用户界面层                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Web 前端    │  │  移动端适配  │  │  飞书多维表  │  │
│  │  (Vue.js)    │  │  (响应式)    │  │  (数据展示)  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      API 网关层                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  FastAPI Backend (Python)                        │  │
│  │  - 路由管理                                       │  │
│  │  - 权限验证                                       │  │
│  │  - 请求日志                                       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      业务逻辑层                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Skill 调用  │  │  内容管理    │  │  数据分析    │  │
│  │  模块        │  │  模块        │  │  模块        │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      数据存储层                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  飞书多维表  │  │  本地文件    │  │  Redis缓存   │  │
│  │  (主存储)    │  │  (临时存储)  │  │  (会话)      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      外部服务层                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ xiaohongshu  │  │  Web Search  │  │  Image Gen   │  │
│  │  -mcp        │  │  API         │  │  API         │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.2 技术栈选择

#### 前端技术栈
- **框架**: Vue 3 + Vite
- **UI 组件**: Element Plus (轻量、美观、移动友好)
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP 客户端**: Axios
- **样式**: Tailwind CSS (响应式设计)

**选择理由**:
- Vue 3 学习曲线平缓，适合快速开发
- Element Plus 提供丰富的组件，减少开发时间
- Tailwind CSS 便于响应式设计，支持移动端

#### 后端技术栈
- **部署平台**: Vercel Serverless Functions
- **框架**: FastAPI (Python) 或 Next.js API Routes
- **运行时**: Python 3.9+ (Vercel 支持)
- **数据验证**: Pydantic
- **任务处理**: 分步执行（避免 10 秒超时）
- **日志**: Vercel 内置日志系统

**选择理由**:
- Vercel 100% 免费（Hobby Plan）
- 无需管理服务器，自动扩展
- Python 与现有 skills 无缝集成
- 分步执行策略解决超时限制

#### 数据存储
- **主存储**: 飞书多维表格 API
- **图片存储**: Vercel Blob Storage (免费 1GB)
- **临时数据**: Vercel KV (Redis 兼容，免费额度)
- **会话**: JWT Token (无状态)

**选择理由**:
- 飞书多维表格可视化强，便于数据分析
- Vercel Blob 存储生成的图片（免费 1GB）
- Vercel KV 提供快速缓存（免费额度足够）
- JWT 无状态会话，适合 Serverless

---

## 三、功能模块设计

### 3.1 核心功能模块

#### 模块1: 内容创建
**功能**:
- 选题输入（手动输入或热门推荐）
- 调用 xiaohongshu-content-generator skill
- **分步执行策略**（解决 Vercel 10 秒超时）
- 实时显示生成进度（自动化，无需手动确认）
- 预览生成的文案和配图

**分步执行流程**:
```
用户点击"生成内容"
  ↓
Step 1: 生成文案 (3秒)
  ↓
Step 2-13: 逐张生成图片 (每张 5秒)
  ↓
前端自动轮询，显示进度条
  ↓
完成后显示结果
```

**API 端点**:
```
POST /api/content/generate-text      # Step 1: 生成文案
POST /api/content/generate-image     # Step 2-13: 生成单张图片
GET  /api/content/preview/{content_id}
```

#### 模块2: 内容管理
**功能**:
- 内容列表（分页、搜索、筛选）
- 内容编辑（文案、配图）
- 内容删除
- 批量操作

**API 端点**:
```
GET    /api/content/list
GET    /api/content/{content_id}
PUT    /api/content/{content_id}
DELETE /api/content/{content_id}
POST   /api/content/batch
```

#### 模块3: 内容发布
**功能**:
- 推送到小红书草稿箱（通过 xiaohongshu-mcp）
- 发布状态追踪
- 发布历史记录

**API 端点**:
```
POST /api/publish/xiaohongshu
GET  /api/publish/status/{publish_id}
GET  /api/publish/history
```

#### 模块4: 热门选题
**功能**:
- 网络搜索热门话题
- 选题推荐（基于历史数据）
- 选题收藏

**API 端点**:
```
GET  /api/topics/trending
POST /api/topics/search
POST /api/topics/favorite
```

#### 模块5: 数据统计
**功能**:
- 内容数量统计
- 发布频率分析
- 选题分布
- 飞书多维表格同步

**API 端点**:
```
GET /api/stats/overview
GET /api/stats/content
GET /api/stats/publish
```

### 3.2 辅助功能模块

#### 模块6: 用户管理
**功能**:
- 简单的登录认证（单用户）
- 会话管理

**API 端点**:
```
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/status
```

#### 模块7: 系统设置
**功能**:
- 飞书配置
- xiaohongshu-mcp 配置
- 图片生成 API 配置

**API 端点**:
```
GET /api/settings
PUT /api/settings
```

#### 模块8: 手动创建内容（新增）
**功能**:
- 手动输入标题和文案
- 上传图片（从本地/手机相册）
- 保存为可推送的内容
- 支持导入外部内容

**API 端点**:
```
POST /api/content/manual-create
POST /api/content/upload-images
```

**使用场景**:
- 在其他地方准备好的内容，想用平台推送
- 不需要 AI 生成，只需要推送功能
- 导入历史内容到平台

### 3.3 PWA 功能模块（新增）

#### 模块9: PWA 支持
**功能**:
- 添加到主屏幕
- 离线查看历史内容
- 全屏体验（无浏览器地址栏）
- 快速启动

**技术实现**:
- Service Worker（缓存策略）
- Web App Manifest（应用配置）
- 离线数据存储（IndexedDB）

**配置文件** (`manifest.json`):
```json
{
  "name": "小红书内容管理平台",
  "short_name": "小红书",
  "description": "AI 驱动的小红书内容生成和管理平台",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#ff2442",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

#### 模块10: 推送通知
**功能**:
- 内容生成完成通知
- 推送成功/失败通知
- 定时提醒（可选）
- 自定义通知设置

**技术实现**:
- Web Push API
- Push Notification Service
- 用户授权管理

**API 端点**:
```
POST /api/notifications/subscribe    # 订阅通知
POST /api/notifications/unsubscribe  # 取消订阅
POST /api/notifications/send         # 发送通知（后端调用）
GET  /api/notifications/settings     # 通知设置
```

**通知类型**:
```javascript
// 1. 内容生成完成
{
  title: "内容生成完成",
  body: "您的内容《多肉植物养护技巧》已生成完成",
  icon: "/icon-192.png",
  badge: "/badge-72.png",
  data: {
    type: "content_generated",
    content_id: "content_789"
  }
}

// 2. 推送成功
{
  title: "推送成功",
  body: "内容已成功推送到小红书草稿箱",
  icon: "/icon-192.png"
}

// 3. 定时提醒
{
  title: "内容提醒",
  body: "今天还没有发布内容，要生成一篇吗？",
  icon: "/icon-192.png"
}
```

#### 模块11: 快捷操作
**功能**:
- 长按图标显示快捷菜单
- 快速生成内容
- 快速查看历史
- 快速推送最新内容

**技术实现**:
- PWA Shortcuts API
- 在 manifest.json 中配置

**配置示例**:
```json
{
  "shortcuts": [
    {
      "name": "快速生成内容",
      "short_name": "生成",
      "description": "快速生成一篇小红书内容",
      "url": "/create?quick=true",
      "icons": [{ "src": "/icons/create.png", "sizes": "96x96" }]
    },
    {
      "name": "查看历史内容",
      "short_name": "历史",
      "description": "查看所有历史内容",
      "url": "/history",
      "icons": [{ "src": "/icons/history.png", "sizes": "96x96" }]
    },
    {
      "name": "推送最新内容",
      "short_name": "推送",
      "description": "推送最新生成的内容到小红书",
      "url": "/publish/latest",
      "icons": [{ "src": "/icons/publish.png", "sizes": "96x96" }]
    }
  ]
}
```

---

## 四、数据模型设计

### 4.1 飞书多维表格结构

#### 表1: 内容表 (contents)
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | 文本 | 唯一标识 |
| title | 文本 | 标题 |
| content | 多行文本 | 正文内容 |
| topic | 文本 | 选题 |
| status | 单选 | 状态（草稿/已发布/已删除） |
| created_at | 日期 | 创建时间 |
| published_at | 日期 | 发布时间 |
| images | 附件 | 配图文件 |
| tags | 多选 | 标签 |

#### 表2: 发布记录表 (publish_history)
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | 文本 | 唯一标识 |
| content_id | 关联 | 关联内容表 |
| platform | 单选 | 平台（小红书） |
| status | 单选 | 状态（成功/失败） |
| published_at | 日期 | 发布时间 |
| error_message | 文本 | 错误信息 |

#### 表3: 选题库 (topics)
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | 文本 | 唯一标识 |
| topic | 文本 | 选题内容 |
| source | 单选 | 来源（手动/热门/推荐） |
| used_count | 数字 | 使用次数 |
| created_at | 日期 | 创建时间 |
| is_favorite | 复选框 | 是否收藏 |

### 4.2 本地文件存储结构

```
/data/
├── images/              # 生成的配图
│   ├── {content_id}/
│   │   ├── 01_封面.png
│   │   ├── 02_配图1.png
│   │   └── ...
├── temp/                # 临时文件
└── exports/             # 导出文件
```

---

## 五、接口设计

### 5.1 RESTful API 规范

**基础 URL**: `http://localhost:8000/api`

**通用响应格式**:
```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

**错误响应格式**:
```json
{
  "code": 400,
  "message": "error message",
  "detail": "detailed error info"
}
```

### 5.2 核心 API 示例

#### 生成文案（Step 1）
```
POST /api/content/generate-text

Request:
{
  "topic": "多肉植物养护技巧",
  "style": "信任型",
  "include_product": false
}

Response:
{
  "code": 200,
  "message": "文案生成成功",
  "data": {
    "content_id": "content_789",
    "title": "多肉植物养护的5个关键技巧",
    "content": "...",
    "image_prompts": [
      "prompt for image 1",
      "prompt for image 2",
      ...
    ]
  }
}
```

#### 生成单张图片（Step 2-13）
```
POST /api/content/generate-image

Request:
{
  "content_id": "content_789",
  "image_index": 0,
  "prompt": "prompt for image 1"
}

Response:
{
  "code": 200,
  "message": "图片生成成功",
  "data": {
    "image_url": "https://blob.vercel-storage.com/...",
    "image_index": 0
  }
}
```

#### 前端自动化调用示例
```javascript
// 用户只需点击一次"生成内容"
async function generateContent(topic) {
  // Step 1: 生成文案
  updateProgress('正在生成文案...', 0);
  const textRes = await fetch('/api/content/generate-text', {
    method: 'POST',
    body: JSON.stringify({ topic })
  });
  const textData = await textRes.json();

  // Step 2-13: 自动生成12张图片
  const images = [];
  for (let i = 0; i < 12; i++) {
    updateProgress(`正在生成图片 ${i+1}/12...`, 10 + (i * 7));
    const imgRes = await fetch('/api/content/generate-image', {
      method: 'POST',
      body: JSON.stringify({
        content_id: textData.data.content_id,
        image_index: i,
        prompt: textData.data.image_prompts[i]
      })
    });
    const imgData = await imgRes.json();
    images.push(imgData.data.image_url);
  }

  updateProgress('全部完成！', 100);
  displayResult({ text: textData.data, images });
}
```

---

## 六、部署架构（Vercel 全栈方案）

### 6.1 为什么选择 Vercel

**核心优势**:
- ✅ **100% 免费**: Hobby Plan 永久免费
- ✅ **零运维**: 无需管理服务器
- ✅ **自动扩展**: 流量增加自动扩容
- ✅ **全球 CDN**: 访问速度快
- ✅ **HTTPS 自动**: 自动配置 SSL 证书
- ✅ **与现有工具链兼容**: 已使用 Vercel 部署静态网站

**免费额度**:
- Serverless Functions: 100GB-Hrs/月
- Bandwidth: 100GB/月
- Blob Storage: 1GB 存储
- KV Database: 256MB 存储
- 对于单用户使用，完全足够

### 6.2 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    Cloudflare DNS                        │
│              (你的阿里云域名解析)                         │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Vercel Platform                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Frontend (Vue 3 + Vite)                         │  │
│  │  - 静态资源托管                                   │  │
│  │  - 自动构建部署                                   │  │
│  │  - 全球 CDN 加速                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                            ↓                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Serverless Functions (Python)                   │  │
│  │  - /api/content/generate-text                    │  │
│  │  - /api/content/generate-image                   │  │
│  │  - /api/content/list                             │  │
│  │  - /api/publish/xiaohongshu                      │  │
│  │  - 每个函数独立运行，10秒超时                     │  │
│  └──────────────────────────────────────────────────┘  │
│                            ↓                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Vercel Storage                                  │  │
│  │  - Blob Storage (图片存储, 1GB)                  │  │
│  │  - KV Database (缓存, 256MB)                     │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    外部服务                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  飞书多维表  │  │ xiaohongshu  │  │  Image Gen   │  │
│  │  (主存储)    │  │  -mcp        │  │  API         │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 6.3 项目结构

```
xiaohongshu-visual-platform/
├── frontend/                    # Vue 3 前端
│   ├── src/
│   │   ├── components/         # 组件
│   │   ├── views/              # 页面
│   │   ├── api/                # API 调用
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
├── api/                         # Vercel Serverless Functions
│   ├── content/
│   │   ├── generate-text.py    # 生成文案
│   │   └── generate-image.py   # 生成单张图片
│   ├── publish/
│   │   └── xiaohongshu.py      # 推送到小红书
│   └── utils/
│       ├── feishu.py           # 飞书 API 封装
│       └── skill_caller.py     # Skill 调用封装
│
├── vercel.json                  # Vercel 配置
└── requirements.txt             # Python 依赖
```

### 6.4 Vercel 配置文件

**vercel.json**:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "frontend/dist"
      }
    },
    {
      "src": "api/**/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ],
  "env": {
    "FEISHU_APP_ID": "@feishu_app_id",
    "FEISHU_APP_SECRET": "@feishu_app_secret",
    "IMAGE_API_KEY": "@image_api_key"
  }
}
```

### 6.5 部署流程

#### 开发环境
```bash
# 前端开发
cd frontend
npm install
npm run dev          # http://localhost:5173

# 后端开发（使用 Vercel CLI）
vercel dev           # 本地模拟 Vercel 环境
```

#### 生产部署
```bash
# 方式1: 通过 Git 自动部署（推荐）
git push origin main
# Vercel 自动检测并部署

# 方式2: 手动部署
vercel --prod
```

#### 域名配置
```
1. 在 Vercel 项目设置中添加自定义域名
2. 在 Cloudflare DNS 中添加 CNAME 记录
   - 类型: CNAME
   - 名称: xiaohongshu (或其他子域名)
   - 目标: cname.vercel-dns.com
3. 等待 DNS 生效（通常几分钟）
```

### 6.6 环境变量配置

在 Vercel 项目设置中配置以下环境变量：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `FEISHU_APP_ID` | 飞书应用 ID | cli_xxx |
| `FEISHU_APP_SECRET` | 飞书应用密钥 | xxx |
| `IMAGE_API_KEY` | 图片生成 API Key | sk-xxx |
| `XIAOHONGSHU_MCP_URL` | 小红书 MCP 地址 | http://... |

### 6.7 解决 10 秒超时的策略

**问题**: Vercel Serverless Functions 有 10 秒超时限制

**解决方案**: 分步执行 + 前端自动轮询

**实现细节**:

1. **后端**: 将长任务拆分为多个短任务
   ```python
   # api/content/generate-text.py
   def handler(request):
       # 只生成文案，3秒内完成
       text = generate_text(topic)
       return {
           "content_id": content_id,
           "text": text,
           "image_prompts": [...]
       }

   # api/content/generate-image.py
   def handler(request):
       # 只生成单张图片，5秒内完成
       image = generate_single_image(prompt)
       return {
           "image_url": image_url
       }
   ```

2. **前端**: 自动串行调用
   ```javascript
   async function generateContent(topic) {
     // Step 1: 生成文案
     const text = await generateText(topic);

     // Step 2-13: 自动生成12张图片
     for (let i = 0; i < 12; i++) {
       updateProgress(`生成图片 ${i+1}/12`);
       await generateImage(text.image_prompts[i]);
     }
   }
   ```

3. **用户体验**: 只需点击一次，自动完成所有步骤

### 6.8 成本估算

**完全免费**（基于 Vercel Hobby Plan）:

| 资源 | 免费额度 | 预估使用 | 是否足够 |
|------|---------|---------|---------|
| Serverless 执行时间 | 100 GB-Hrs/月 | ~5 GB-Hrs/月 | ✅ 足够 |
| 带宽 | 100 GB/月 | ~10 GB/月 | ✅ 足够 |
| Blob 存储 | 1 GB | ~500 MB | ✅ 足够 |
| KV 数据库 | 256 MB | ~50 MB | ✅ 足够 |

**使用场景假设**:
- 每天生成 3 篇内容
- 每篇 12 张图片（每张 100KB）
- 每月约 90 篇内容，1080 张图片
- 总存储: ~108 MB（远低于 1GB 限制）

### 6.9 监控与日志

**Vercel 内置监控**:
- 访问 Vercel Dashboard 查看:
  - 函数执行时间
  - 错误率
  - 带宽使用
  - 存储使用

**日志查看**:
```bash
# 实时查看日志
vercel logs --follow

# 查看特定函数的日志
vercel logs --function=api/content/generate-text
```

### 6.10 备份策略

**数据备份**:
- 飞书多维表格: 定期导出为 Excel
- Vercel Blob 图片: 定期下载到本地
- 代码: Git 仓库自动备份

**备份脚本**:
```bash
# 每周自动备份飞书数据
# 可以使用 GitHub Actions 定时执行
```

---

## 七、用户体验流程（重点说明）

### 7.1 内容生成流程（一键自动化）

**用户操作**: 只需点击一次"生成内容"按钮

**系统自动执行**:

```
┌─────────────────────────────────────────────────────────┐
│  用户输入选题 + 点击"生成内容"                           │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  前端显示进度条（自动更新，无需用户操作）                │
│                                                          │
│  ✓ 正在生成文案... (0%)                                  │
│  ✓ 文案生成完成 (10%)                                    │
│  ✓ 正在生成图片 1/12... (17%)                            │
│  ✓ 正在生成图片 2/12... (24%)                            │
│  ...                                                     │
│  ✓ 正在生成图片 12/12... (100%)                          │
│  ✓ 全部完成！                                            │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  显示完整结果（文案 + 12张图片）                         │
│  - 可预览                                                │
│  - 可编辑                                                │
│  - 可推送到小红书                                        │
└─────────────────────────────────────────────────────────┘
```

**关键点**:
- ✅ 用户只需点击一次
- ✅ 无需手动确认每一步
- ✅ 进度条实时显示当前状态
- ✅ 整个过程约 1-2 分钟
- ✅ 类似于上传多个文件的体验

### 7.2 前端实现示例

```javascript
// 用户点击"生成内容"按钮触发
async function handleGenerateContent() {
  const topic = document.getElementById('topic').value;

  // 显示进度条
  showProgressModal();

  try {
    // Step 1: 生成文案（自动）
    updateProgress('正在生成文案...', 0);
    const textResponse = await fetch('/api/content/generate-text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic })
    });
    const textData = await textResponse.json();
    updateProgress('文案生成完成', 10);

    // Step 2-13: 生成12张图片（自动循环）
    const images = [];
    for (let i = 0; i < 12; i++) {
      updateProgress(`正在生成图片 ${i+1}/12...`, 10 + (i * 7.5));

      const imageResponse = await fetch('/api/content/generate-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content_id: textData.content_id,
          image_index: i,
          prompt: textData.image_prompts[i]
        })
      });

      const imageData = await imageResponse.json();
      images.push(imageData.image_url);
    }

    // 完成
    updateProgress('全部完成！', 100);

    // 显示结果
    displayResult({
      content_id: textData.content_id,
      title: textData.title,
      content: textData.content,
      images: images
    });

  } catch (error) {
    showError('生成失败，请重试');
    console.error(error);
  } finally {
    // 3秒后自动关闭进度条
    setTimeout(() => hideProgressModal(), 3000);
  }
}
```

### 7.3 与其他常见场景对比

| 场景 | 用户操作次数 | 等待时间 | 体验 |
|------|-------------|---------|------|
| **上传多个文件** | 1次（选择文件+点击上传） | 根据文件大小 | 进度条显示 |
| **批量下载图片** | 1次（点击下载） | 根据图片数量 | 进度条显示 |
| **我们的平台** | 1次（点击生成） | 1-2分钟 | 进度条显示 |
| **传统方式（需手动确认）** | 13次（每步都要点） | 1-2分钟 | 体验差 ❌ |

### 7.4 错误处理

**如果某一步失败**:
```
正在生成图片 5/12...
❌ 图片 5 生成失败
↓
自动重试（最多3次）
↓
如果仍然失败：
  - 跳过该图片
  - 继续生成剩余图片
  - 最后提示用户："已生成 11/12 张图片，图片 5 生成失败"
```

**网络中断**:
```
检测到网络中断
↓
暂停生成
↓
显示提示："网络连接中断，请检查网络后重试"
↓
用户可以选择：
  - 重新开始
  - 从中断处继续（如果已保存进度）
```

### 7.5 移动端体验

**手机访问时**:
- 响应式布局，自动适配屏幕
- 进度条占据屏幕中央
- 可以锁屏，后台继续生成
- 生成完成后发送通知（如果允许）

---

## 八、安全设计

### 7.1 认证与授权

- **认证方式**: JWT Token
- **会话管理**: Redis 存储
- **密码加密**: bcrypt

### 7.2 API 安全

- **CORS 配置**: 限制允许的域名
- **速率限制**: 防止 API 滥用
- **输入验证**: Pydantic 模型验证
- **SQL 注入防护**: 使用 ORM/参数化查询

### 7.3 数据安全

- **敏感信息加密**: API Key、Token 等
- **HTTPS**: 生产环境强制使用
- **备份策略**: 飞书数据定期导出备份

---

## 八、性能优化（Serverless 优化策略）

### 8.1 前端优化

- **代码分割**: 路由懒加载，减少首屏加载时间
- **资源压缩**: Vite 自动 Gzip/Brotli 压缩
- **CDN 加速**: Vercel 全球 CDN 自动加速
- **图片优化**:
  - 使用 WebP 格式
  - 懒加载（Intersection Observer）
  - 响应式图片（srcset）
- **缓存策略**:
  - 静态资源长期缓存（1年）
  - HTML 短期缓存（5分钟）

### 8.2 后端优化（Serverless 特有）

- **冷启动优化**:
  - 减少依赖包大小
  - 使用轻量级库
  - 预热关键函数（定时调用）
- **函数拆分**:
  - 每个函数只做一件事
  - 避免单个函数超时
  - 独立部署，独立扩展
- **缓存策略**:
  - Vercel KV 缓存热点数据
  - 飞书 API 响应缓存（5分钟）
  - 图片 prompt 缓存（避免重复生成）
- **并发控制**:
  - 前端控制并发请求数（最多 3 个）
  - 避免同时生成多张图片导致超时

### 8.3 移动端优化

- **响应式设计**: Tailwind CSS 断点适配
- **触摸优化**:
  - 按钮最小 44x44px
  - 增加点击区域
  - 防止误触
- **加载优化**:
  - 骨架屏（Skeleton）
  - 进度条（实时反馈）
  - 乐观更新（Optimistic UI）
- **网络优化**:
  - 请求合并
  - 失败重试（指数退避）
  - 离线提示

### 8.4 成本优化

- **图片存储优化**:
  - 定期清理过期图片
  - 压缩图片质量（80%）
  - 使用 WebP 格式（减少 30% 体积）
- **函数执行优化**:
  - 避免不必要的 API 调用
  - 批量操作合并请求
  - 使用缓存减少重复计算
- **带宽优化**:
  - 启用 Brotli 压缩
  - 图片懒加载
  - 分页加载（每页 20 条）

---

## 九、监控与日志

### 9.1 日志系统

- **应用日志**: structlog 结构化日志
- **访问日志**: Nginx access log
- **错误日志**: 异常追踪和告警

### 9.2 监控指标

- **系统监控**: CPU、内存、磁盘
- **应用监控**: API 响应时间、错误率
- **业务监控**: 内容生成成功率、发布成功率

---

## 十一、开发计划（基于 Vercel 部署）

### 11.1 MVP (最小可行产品) - 2周

**Week 1: 基础框架 + 核心功能**
- [ ] Day 1-2: 搭建项目框架
  - 创建 Vue 3 + Vite 前端项目
  - 配置 Vercel 项目
  - 创建基础 Serverless Functions
- [ ] Day 3-4: 实现内容生成功能
  - 实现文案生成 API (`/api/content/generate-text`)
  - 实现图片生成 API (`/api/content/generate-image`)
  - 前端进度条组件
- [ ] Day 5-7: 内容管理功能
  - 内容列表页面
  - 内容预览页面
  - 基础编辑功能

**Week 2: 数据存储 + 发布功能**
- [ ] Day 8-10: 飞书集成
  - 飞书 API 封装
  - 数据同步到飞书多维表格
  - 飞书数据读取和展示
- [ ] Day 11-12: 小红书发布
  - xiaohongshu-mcp 集成
  - 推送到草稿箱功能
  - 发布状态追踪
- [ ] Day 13-14: UI 优化 + 测试
  - 移动端适配
  - 基础 UI 美化
  - 功能测试和 Bug 修复

### 11.2 完整版本 - 4周

**Week 3: 高级功能**
- [ ] Day 15-17: 热门选题功能
  - Web Search 集成
  - 选题推荐算法
  - 选题收藏功能
- [ ] Day 18-19: 数据统计
  - 内容数量统计
  - 发布频率分析
  - 数据可视化图表
- [ ] Day 20-21: 批量操作
  - 批量生成内容
  - 批量推送
  - 批量删除

**Week 4: 优化 + 部署**
- [ ] Day 22-24: 性能优化
  - 冷启动优化
  - 缓存策略实施
  - 图片压缩优化
- [ ] Day 25-26: 部署到生产
  - 配置自定义域名
  - 环境变量配置
  - HTTPS 配置
- [ ] Day 27-28: 测试 + 文档
  - 完整功能测试
  - 编写使用文档
  - 性能测试

### 11.3 技术栈学习路径（如果需要）

**前端（Vue 3）**:
- 如果不熟悉 Vue 3: 1-2 天学习基础
- 推荐资源: Vue 3 官方文档 + Element Plus 文档

**Vercel 部署**:
- 如果不熟悉 Vercel: 半天学习基础
- 推荐资源: Vercel 官方文档 + 示例项目

**Python Serverless**:
- 如果不熟悉 Serverless: 1 天学习基础
- 推荐资源: Vercel Python 文档 + FastAPI 文档

### 11.4 里程碑

| 里程碑 | 时间 | 交付物 |
|--------|------|--------|
| **M1: 项目启动** | Day 1 | 项目框架搭建完成 |
| **M2: 核心功能** | Day 7 | 可以生成内容（文案+图片） |
| **M3: MVP 完成** | Day 14 | 可以生成、管理、发布内容 |
| **M4: 功能完善** | Day 21 | 所有高级功能完成 |
| **M5: 上线** | Day 28 | 部署到生产环境，可正式使用 |

### 11.5 风险与应对

| 风险 | 可能性 | 影响 | 应对措施 |
|------|--------|------|---------|
| Vercel 超时问题 | 中 | 高 | 已有分步方案，可降低风险 |
| 飞书 API 限流 | 低 | 中 | 实施缓存策略 |
| 图片生成 API 不稳定 | 中 | 高 | 实施重试机制 + 错误处理 |
| 前端技术不熟悉 | 低 | 中 | 使用 Element Plus 降低难度 |
| 移动端适配问题 | 低 | 低 | 使用 Tailwind CSS 响应式 |

---

**文档版本**: v2.0.0 (Vercel 全栈方案)
**最后更新**: 2026-02-06
**维护者**: Claude Code
