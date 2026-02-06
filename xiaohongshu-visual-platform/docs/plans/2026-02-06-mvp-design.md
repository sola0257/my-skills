# MVP 设计文档 - 小红书内容管理平台

**日期**: 2026-02-06
**版本**: v1.0.0
**状态**: 设计完成，准备实施

---

## 一、设计决策

### 1.1 开发策略

**选择**: 本地开发，稍后部署

**理由**:
- 开发速度快，调试方便
- 不依赖网络和外部服务
- 可以快速验证功能
- 后续可以轻松迁移到 Vercel

### 1.2 开发顺序

**选择**: 前端优先，使用 Mock 数据

**理由**:
- 可以快速看到 UI 效果
- 用户体验更直观
- 可以先确定交互流程
- 后端可以根据前端需求调整

### 1.3 前端架构

**选择**: 单页应用 + 组件化

**技术栈**:
- Vue 3 + Composition API
- Vite（开发服务器和构建工具）
- Tailwind CSS（样式）
- Vue Router（路由）

**理由**:
- 组件复用性强
- 代码结构清晰
- 易于维护和扩展
- 符合 Vue 3 最佳实践

### 1.4 内容生成策略

**选择**: 调用现有的 xiaohongshu-content-generator skill

**理由**:
- 内容质量有保证
- 包含完整的质量检查流程
- 可以直接使用现有的知识库和案例
- 真正可用的 MVP，不只是原型

**已知限制**:
- WebSearch 功能调用失败
- 自动回退到本地知识库
- 本地知识库内容不够丰富（植物广度和深度都不够）
- MVP 阶段暂时接受这个限制

---

## 二、项目结构

```
xiaohongshu-visual-platform/
├── frontend/                    # Vue 3 前端
│   ├── src/
│   │   ├── views/              # 页面组件
│   │   │   ├── Home.vue        # 首页（导航）
│   │   │   ├── ContentCreate.vue  # 内容创建页面
│   │   │   ├── ContentList.vue    # 内容列表页面
│   │   │   └── ContentDetail.vue  # 内容详情页面
│   │   │
│   │   ├── components/         # 可复用组件
│   │   │   ├── TopicInput.vue     # 选题输入组件
│   │   │   ├── ProgressModal.vue  # 进度条弹窗组件
│   │   │   ├── ResultPreview.vue  # 结果预览组件
│   │   │   └── ImageGallery.vue   # 图片画廊组件
│   │   │
│   │   ├── api/                # API 调用封装
│   │   │   └── content.js      # 内容相关 API
│   │   │
│   │   ├── router/             # 路由配置
│   │   │   └── index.js
│   │   │
│   │   ├── App.vue             # 根组件
│   │   └── main.js             # 入口文件
│   │
│   ├── package.json
│   └── vite.config.js
│
├── backend/                     # Python 后端脚本
│   └── generate_content.py     # 内容生成脚本
│
├── data/                        # 数据存储目录
│   ├── contents/               # 内容元数据（JSON）
│   └── images/                 # 图片文件
│
└── docs/
    └── plans/
        └── 2026-02-06-mvp-design.md  # 本文档
```

---

## 三、数据流设计

### 3.1 用户交互流程

```
用户输入选题
  ↓
点击"生成内容"按钮
  ↓
显示进度弹窗
  ↓
后端生成文案（3秒）
  ↓
后端生成12张图片（串行，每张间隔3秒）
  ↓
显示结果（文案 + 12张图片）
  ↓
用户可以：
  - 保存结果
  - 编辑内容
  - 重新生成失败的图片
  - 放弃
```

### 3.2 状态管理

**MVP 阶段不使用 Pinia**，使用组件内部状态：
- `ref` - 响应式数据
- `reactive` - 响应式对象
- `computed` - 计算属性

**父子组件通信**:
- Props（父 → 子）
- Emits（子 → 父）

---

## 四、图片生成策略

### 4.1 延迟控制

**策略**: 串行生成，每张图片间隔 3 秒

```javascript
async function generateImages(prompts) {
  const images = [];
  const DELAY_BETWEEN_IMAGES = 3000; // 3秒

  for (let i = 0; i < prompts.length; i++) {
    const image = await generateSingleImage(prompts[i]);
    images.push(image);

    updateProgress(10 + (i + 1) * 7.5);

    if (i < prompts.length - 1) {
      await sleep(DELAY_BETWEEN_IMAGES);
    }
  }

  return images;
}
```

**理由**:
- 避免 API 速率限制
- 避免并发请求过多导致失败
- 降低服务器压力

### 4.2 错误处理

**重试机制**: 失败自动重试 3 次，使用指数退避

```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(1000 * Math.pow(2, i)); // 1s, 2s, 4s
    }
  }
}
```

**容错机制**: 单张失败不影响整体流程

```javascript
async function generateImages(prompts) {
  const images = [];
  const failedImages = []; // 记录失败的图片序号

  for (let i = 0; i < prompts.length; i++) {
    try {
      const image = await retryWithBackoff(
        () => generateSingleImage(prompts[i]),
        3
      );

      if (image) {
        images.push(image);
      } else {
        images.push(null);  // 占位
        failedImages.push(i + 1);
      }
    } catch (error) {
      images.push(null);
      failedImages.push(i + 1);
    }
  }

  return { images, failedImages };
}
```

### 4.3 单独重新生成失败图片

**UI 展示**:
```
配图 (11/12 张成功)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[图1] [图2] [图3] [图4]
[❌失败] [图6] [图7] [图8]  ← 图5显示失败状态
[图9] [图10] [图11] [图12]

点击失败的图片可以单独重新生成
```

**交互**:
- 点击失败的图片 → 单独重新生成
- 点击"重新生成所有失败图片" → 批量重新生成
- 重新生成时仍然遵循延迟控制（3秒间隔）

---

## 五、数据存储方案

### 5.1 存储结构

```
/data/
├── contents/                    # 内容数据目录
│   ├── content_001.json        # 内容元数据
│   ├── content_002.json
│   └── ...
│
└── images/                      # 图片文件目录
    ├── content_001/            # 每个内容对应一个图片目录
    │   ├── 01_封面.png
    │   ├── 02_配图1.png
    │   ├── ...
    │   └── 12_配图11.png
    └── content_002/
        └── ...
```

### 5.2 数据模型

**content_001.json**:
```json
{
  "id": "content_001",
  "topic": "多肉植物养护技巧",
  "title": "多肉植物养护的5个关键技巧",
  "content": "正文内容...",
  "images": [
    "/data/images/content_001/01_封面.png",
    "/data/images/content_001/02_配图1.png",
    ...
  ],
  "status": "draft",  // draft, published
  "createdAt": "2026-02-06T15:30:00Z",
  "updatedAt": "2026-02-06T15:35:00Z"
}
```

### 5.3 保存策略

- **文案和元数据**: 保存在 JSON 文件中（轻量、易于查询）
- **图片文件**: 保存在对应的目录中（独立管理、易于替换）
- **关联方式**: JSON 中存储图片的相对路径

**优点**:
- 数据结构清晰
- 图片可以单独管理（替换、删除）
- JSON 文件小，加载快
- 易于迁移到飞书或 Vercel

---

## 六、后端实现

### 6.1 技术选择

**方案**: 简单的本地 Python 脚本

**理由**:
- 可以直接调用 xiaohongshu-content-generator skill
- 实现简单，易于调试
- 后续可以迁移到 Vercel Serverless Functions

### 6.2 实现示例

```python
# backend/generate_content.py
import sys
import json
from pathlib import Path

def generate_content(topic):
    # 调用 xiaohongshu-content-generator skill
    # 这里可以直接调用 Claude API 或使用现有的 skill

    result = {
        "id": "content_001",
        "topic": topic,
        "title": "生成的标题",
        "content": "生成的正文",
        "images": []  # 图片路径列表
    }

    return result

if __name__ == "__main__":
    topic = sys.argv[1]
    result = generate_content(topic)
    print(json.dumps(result, ensure_ascii=False))
```

### 6.3 前端调用

```javascript
// 使用 Node.js 的 child_process 调用 Python 脚本
const { exec } = require('child_process');

async function generateContent(topic) {
  return new Promise((resolve, reject) => {
    exec(`python backend/generate_content.py "${topic}"`,
      (error, stdout, stderr) => {
        if (error) reject(error);
        resolve(JSON.parse(stdout));
      }
    );
  });
}
```

---

## 七、MVP 范围

### 7.1 包含的功能

- ✅ 前端 UI 和交互
- ✅ 内容生成功能（文案 + 12张图片）
- ✅ 进度显示
- ✅ 错误处理和重试
- ✅ 单独重新生成失败图片
- ✅ 本地数据存储
- ✅ 内容列表查看
- ✅ 内容详情查看

### 7.2 不包含的功能（完整版本再实现）

- ❌ 飞书多维表格集成
- ❌ 部署到 Vercel
- ❌ 推送到小红书草稿箱
- ❌ 热门选题推荐
- ❌ 数据统计和分析
- ❌ PWA 功能
- ❌ 推送通知

---

## 八、下一步

1. **创建详细的实现计划** - 使用 `superpowers:writing-plans`
2. **开始实现** - 按照计划逐步实现
3. **测试和验证** - 确保功能正常工作
4. **迭代优化** - 根据使用反馈改进

---

**文档版本**: v1.0.0
**最后更新**: 2026-02-06
**维护者**: Claude Code
