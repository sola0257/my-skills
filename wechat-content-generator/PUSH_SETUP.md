# 微信公众号推送配置指南 v3.0

## 📋 概述

本文档说明如何配置微信公众号推送功能，使内容能够自动推送到草稿箱。

**v3.0 更新 (2026-01-30)**：
- 图片处理策略优化：封面用图床 + 正文用 Base64
- 减少外部依赖，提高推送可靠性

---

## 🔑 API配置

### 1. 微信公众号API（微绿流量宝）

**获取方式：**
1. 访问：https://wx.limyai.com
2. 注册账号并获取API Key
3. 分别获取订阅号和服务号的API Key

**配置环境变量：**

```bash
# 订阅号API Key
export WECHAT_SUBSCRIPTION_API_KEY="your_subscription_api_key_here"

# 服务号API Key
export WECHAT_SERVICE_API_KEY="your_service_api_key_here"
```

### 2. ImgBB图床API

**获取方式：**
1. 访问：https://api.imgbb.com
2. 注册账号并获取API Key

**配置环境变量：**

```bash
export IMGBB_API_KEY="your_imgbb_api_key_here"
```

---

## 🛠️ 使用方法

### 方法1：通过Skill自动推送

当使用 `/wechat-content-generator` 生成内容时，会自动推送到草稿箱。

```bash
/wechat-content-generator 主题="春节花园改造" 格式="订阅号长文"
```

### 方法2：手动推送现有文档

如果已经有Markdown文档，可以手动推送：

```bash
# 推送到订阅号
python /Users/dj/Desktop/小静的skills/wechat-content-generator/scripts/wechat_publish.py \
  "/path/to/your/article.md" subscription

# 推送到服务号
python /Users/dj/Desktop/小静的skills/wechat-content-generator/scripts/wechat_publish.py \
  "/path/to/your/article.md" service
```

---

## 📝 推送流程（v3.0 优化）

1. **读取Markdown文件**
   - 提取标题、正文、图片引用

2. **处理图片（智能策略）**
   - **封面图**：上传到 ImgBB 图床（避免 API 字段限制）
   - **正文图片**：
     * 文件 ≤ 2MB：转换为 Base64 直接嵌入
     * 文件 > 2MB：上传到图床

3. **转换为HTML**
   - Markdown转换为微信兼容的HTML
   - 图片已处理为 URL 或 Base64

4. **推送到草稿箱**
   - 调用微信API
   - 创建草稿

5. **保存推送结果**
   - 保存Media ID
   - 保存推送时间和状态

### 图片处理策略说明

| 图片类型 | 处理方式 | 原因 |
|---------|---------|------|
| 封面图 | 图床（imgbb） | API 数据库字段有长度限制 |
| 正文图片（≤2MB） | Base64 嵌入 | 减少外部依赖，提高可靠性 |
| 正文图片（>2MB） | 图床（imgbb） | 避免文档过大 |

**优势**：
- ✅ 正文图片自包含，无需依赖图床
- ✅ 减少网络请求，提高推送速度
- ✅ 智能降级，处理各种场景

---

## ✅ 验证推送成功

推送成功后会显示：

```
✅ 推送成功！
📋 Media ID: xxxxx
🔗 草稿箱链接: https://mp.weixin.qq.com/cgi-bin/appmsg?action=list&type=10
📁 结果已保存: /path/to/推送结果.json
```

同时会在文章目录下生成 `推送结果.json` 文件：

```json
{
  "status": "success",
  "result": {
    "errcode": 0,
    "errmsg": "ok",
    "media_id": "xxxxx"
  },
  "push_time": "2026-01-25T16:00:00",
  "account_type": "subscription"
}
```

---

## ❌ 常见问题

### 1. API Key未配置

**错误信息：**
```
❌ subscription API Key未配置
```

**解决方法：**
- 检查环境变量是否正确设置
- 确认API Key是否有效

### 2. 图片上传失败

**错误信息：**
```
❌ 图片上传失败: xxx
```

**解决方法：**
- 检查ImgBB API Key是否正确
- 检查图片文件是否存在
- 检查网络连接

### 3. 推送失败

**错误信息：**
```
❌ 推送失败: xxx
```

**解决方法：**
- 检查微信API Key是否正确
- 检查API额度是否用完
- 查看 `推送结果.json` 中的详细错误信息

---

## 🔧 环境变量设置

### macOS/Linux

**临时设置（当前终端会话）：**
```bash
export WECHAT_SUBSCRIPTION_API_KEY="your_key"
export WECHAT_SERVICE_API_KEY="your_key"
export IMGBB_API_KEY="your_key"
```

**永久设置（添加到 ~/.zshrc 或 ~/.bashrc）：**
```bash
echo 'export WECHAT_SUBSCRIPTION_API_KEY="your_key"' >> ~/.zshrc
echo 'export WECHAT_SERVICE_API_KEY="your_key"' >> ~/.zshrc
echo 'export IMGBB_API_KEY="your_key"' >> ~/.zshrc
source ~/.zshrc
```

### Windows

**临时设置（当前命令行会话）：**
```cmd
set WECHAT_SUBSCRIPTION_API_KEY=your_key
set WECHAT_SERVICE_API_KEY=your_key
set IMGBB_API_KEY=your_key
```

**永久设置（系统环境变量）：**
1. 右键"此电脑" → 属性 → 高级系统设置
2. 环境变量 → 新建
3. 添加上述三个变量

---

## 📚 相关文档

- [微绿流量宝API文档](https://wx.limyai.com/docs)
- [ImgBB API文档](https://api.imgbb.com)
- [微信公众号开发文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)

---

## 🔄 版本历史

- **v3.0 (2026-01-30)**：
  - 图片处理策略优化：封面用图床 + 正文用 Base64
  - 新增智能降级机制（>2MB 自动用图床）
  - 减少外部依赖，提高推送可靠性

- **v1.0 (2026-01-25)**：
  - 创建推送脚本
  - 支持订阅号和服务号
  - 支持图片上传到图床
  - 支持Markdown转HTML
  - 支持推送结果验证
