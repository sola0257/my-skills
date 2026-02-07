# Skill Output Format Documentation

## 概述

本文档定义了 `xiaohongshu-content-generator` skill 与平台之间的输出格式契约。

**重要**：修改 skill 时，请确保输出格式与本文档保持一致，否则需要同步更新平台代码。

## 当前版本：v1

### 输出格式

```json
{
    "title": "string",      // 必需：内容标题
    "content": "string",    // 必需：正文内容
    "images": []            // 必需：图片列表（数组）
}
```

### 字段说明

#### `title` (string, 必需)
- **类型**：字符串
- **说明**：生成的内容标题
- **示例**：`"多肉植物养护指南"`

#### `content` (string, 必需)
- **类型**：字符串
- **说明**：正文内容，可以包含换行符
- **示例**：`"多肉植物是一种非常适合新手的植物...\n\n养护要点：\n1. 光照充足\n2. 控制浇水"`

#### `images` (array, 必需)
- **类型**：数组
- **说明**：图片列表，支持两种格式：
  - **简单格式**：字符串数组（URL 或文件路径）
  - **对象格式**：包含 `url` 和 `prompt` 的对象数组

**简单格式示例**：
```json
{
    "images": [
        "https://example.com/image1.jpg",
        "/path/to/image2.png",
        "data:image/png;base64,iVBORw0KG..."
    ]
}
```

**对象格式示例**：
```json
{
    "images": [
        {
            "url": "https://example.com/image1.jpg",
            "prompt": "多肉植物特写"
        },
        {
            "url": "/path/to/image2.png",
            "prompt": "养护工具展示"
        }
    ]
}
```

## 版本兼容性

### 如何安全地修改 Skill

✅ **可以自由修改（无需更新平台代码）**：
- 修改生成逻辑、提示词
- 调整内容质量标准
- 更新知识库
- 修改图片生成算法
- 调整 `title` 和 `content` 的具体内容

⚠️ **需要同步更新平台代码**：
- 修改字段名称（如 `title` → `main_title`）
- 修改字段类型（如 `images` 从数组改为对象）
- 添加新的必需字段
- 删除现有字段

### 如果需要修改输出格式

1. **更新 `skill_caller.py`**：
   - 添加新版本的验证函数
   - 更新 `REQUIRED_FIELDS_V2` 常量
   - 在 `validate_skill_output()` 中添加 v2 分支

2. **更新 `app.py`**：
   - 如果字段名称改变，更新数据映射逻辑

3. **更新本文档**：
   - 添加 v2 格式说明
   - 标记 v1 为已弃用（如果适用）

## 错误处理

### 格式验证失败

如果 skill 输出格式不符合预期，平台会抛出详细的错误信息：

```
Skill output format validation failed: Skill output missing required fields: images. Expected format: ['title', 'content', 'images']
This usually means the skill's output format has changed.
Please check the skill output or update the platform code.
```

### 调试步骤

1. 检查 skill 的输出是否包含所有必需字段
2. 检查字段类型是否正确
3. 如果是有意的格式变更，按照上述步骤更新平台代码

## 示例

### 完整的有效输出

```json
{
    "title": "多肉植物养护全攻略",
    "content": "多肉植物以其可爱的外形和易养护的特点，成为了许多人的首选...\n\n## 养护要点\n\n1. **光照**：每天至少4小时直射光\n2. **浇水**：见干见湿，宁干勿湿\n3. **土壤**：疏松透气的颗粒土",
    "images": [
        {
            "url": "https://example.com/succulent1.jpg",
            "prompt": "多肉植物特写，展示叶片质感"
        },
        {
            "url": "https://example.com/succulent2.jpg",
            "prompt": "养护工具展示"
        }
    ]
}
```

## 版本历史

### v1 (当前版本)
- 初始版本
- 支持 `title`, `content`, `images` 三个字段
- `images` 支持简单格式和对象格式

---

**最后更新**：2026-02-06
**维护者**：Xiaohongshu Visual Platform Team
