# Illustration Converter - 系列生成功能更新

## 更新日期
2026-01-31

## 更新内容

### 1. 新增功能：4张系列插画生成

**功能描述**：
- 每次生成同一种风格时，自动生成4张不同构图的插画，形成系列
- 4种构图策略：
  1. **全景**：完整植物+环境，建立氛围和背景
  2. **中景**：聚焦主体，展示整体形态和关键特征
  3. **特写**：叶片/花瓣纹理的极致细节
  4. **意境**：大量留白，强调情绪和诗意

**实现位置**：
- 文件：`scripts/generate_illustration.py`
- 方法：`generate_series()`
- 调用方式：
  ```python
  generator = IllustrationGenerator()
  paths = generator.generate_series(
      style_code="watercolor_oriental",
      subject="多肉植物",
      details="圆润饱满的叶片",
      mood="治愈、温柔"
  )
  ```

### 2. 新增功能：小红书标题和话题标签生成

**功能描述**：
- 为插画系列生成吸引人的小红书标题（<20字符，诗意化）
- 生成10个话题标签（3-4个大流量标签 + 6-7个长尾标签）
- 自动分类标签策略（流量池标签 vs 精准搜索标签）

**实现位置**：
- 文件：`scripts/generate_title_tags.py`
- 类：`TitleTagGenerator`
- 调用方式：
  ```python
  generator = TitleTagGenerator()
  result = generator.generate_title_and_tags(
      style_name="水彩",
      subject="多肉植物",
      aesthetic="东方"
  )
  # 返回：{"title": "...", "tags": [...], "tag_strategy": {...}}
  ```

**标题策略**：
- 严格限制20字符以内
- 诗意化、情感化、留白感
- 避免营销化、感叹号、夸张词汇
- 公式：时间+主题+情绪 / 风格+主题+意境 / 动作+主题+感受

**标签策略**：
- **大流量标签**（3-4个）：#插画 #手绘 #水彩 #植物
  - 目的：进入流量池，获得初始曝光
  - 特点：搜索量大（>10万），竞争激烈

- **长尾标签**（6-7个）：#水彩植物插画 #东方美学插画 #多肉养护日记
  - 目的：精准搜索，吸引目标用户
  - 特点：搜索量适中（1000-10万），竞争较小，转化率高

### 3. 新增文档：小红书策略指南

**文件位置**：
- `knowledge/xiaohongshu-strategy.md`

**内容包括**：
- 标题策略（长度要求、风格要求、标题公式）
- 话题标签策略（大流量标签 vs 长尾标签）
- 标签组合策略（风格主导型、主题主导型、教程型）
- 完整示例（东方水彩、彩铅步骤图、国画意境）
- 优化建议和避免的错误

---

## 工作流更新

### 原工作流（7步）
1. 图片分析/文本描述
2. 交互式确认风格
3. 生成插画（单张）
4. 满意度评分
5. 案例库管理
6. 持续优化
7. 输出结果

### 新工作流（8步）
1. 图片分析/文本描述
2. 交互式确认风格
3. **生成4张系列插画**（新增）
4. **生成小红书标题和标签**（新增）
5. 满意度评分
6. 案例库管理
7. 持续优化
8. 输出结果

---

## 技术实现

### 系列生成策略

**构图差异化**：
```python
compositions = [
    {
        "name": "全景",
        "prompt_addition": "Wide composition showing the complete plant with surrounding environment..."
    },
    {
        "name": "中景",
        "prompt_addition": "Medium shot focusing on the main subject..."
    },
    {
        "name": "特写",
        "prompt_addition": "Extreme close-up of leaf/petal texture..."
    },
    {
        "name": "意境",
        "prompt_addition": "Atmospheric composition with generous white space..."
    }
]
```

**视觉一致性保证**：
- 所有4张图片使用相同的 `style_code`
- 通过 `STYLE_MODEL_MAPPING` 确保使用相同模型
- 只改变构图描述，不改变风格参数

### 标题生成策略

**API调用**：
- 模型：`gemini-3-pro-preview`
- Temperature：0.8（提高创意性）
- 输出格式：JSON（包含标题、标签、标签策略）

**质量控制**：
- 自动检查标题长度（>20字符则截断）
- 自动检查标签数量（>10个则截断）
- 提供备用结果（API失败时使用）

---

## 使用示例

### 示例1：生成东方水彩系列

```python
from scripts.generate_illustration import IllustrationGenerator
from scripts.generate_title_tags import TitleTagGenerator

# 1. 生成4张系列插画
ill_gen = IllustrationGenerator()
image_paths = ill_gen.generate_series(
    style_code="watercolor_oriental",
    subject="多肉植物桃蛋",
    details="圆润饱满的叶片，表面有白霜，粉色渐变",
    mood="治愈、温柔"
)

# 2. 生成标题和标签
tag_gen = TitleTagGenerator()
title_tags = tag_gen.generate_title_and_tags(
    style_name="水彩",
    subject="多肉植物",
    aesthetic="东方"
)

# 3. 输出结果
print(f"标题: {title_tags['title']}")
print(f"标签: {' '.join(title_tags['tags'])}")
print(f"图片: {len(image_paths)} 张")
```

**预期输出**：
```
标题: 水彩下的多肉时光
标签: #插画 #手绘 #水彩 #多肉 #水彩植物插画 #东方美学插画 #多肉养护日记 #治愈系植物 #手绘日常 #水彩技法分享
图片: 4 张
  - 1_全景_watercolor_oriental_20260131_143022.png
  - 2_中景_watercolor_oriental_20260131_143045.png
  - 3_特写_watercolor_oriental_20260131_143108.png
  - 4_意境_watercolor_oriental_20260131_143131.png
```

---

## 文件清单

### 新增文件
- ✅ `scripts/generate_title_tags.py` - 标题和标签生成脚本
- ✅ `knowledge/xiaohongshu-strategy.md` - 小红书策略指南

### 修改文件
- ✅ `scripts/generate_illustration.py` - 新增 `generate_series()` 方法
- ✅ `SKILL.md` - 更新工作流（Step 4-5）

### 现有文件（未修改）
- `knowledge/style-prompt-templates.md` - 风格提示词模板
- `knowledge/style-model-mapping.md` - 风格-模型映射表
- `scripts/case_manager.py` - 案例库管理器
- `knowledge/cases/` - 案例库目录

---

## 下一步计划

### 待测试
- [ ] 测试4张系列插画生成（不同风格）
- [ ] 测试标题和标签生成（不同主题）
- [ ] 验证视觉一致性（同一风格的4张图）
- [ ] 验证标题长度控制（<20字符）
- [ ] 验证标签数量控制（10个）

### 待优化
- [ ] 添加标题A/B测试功能
- [ ] 添加标签热度分析功能
- [ ] 添加系列图片排版建议
- [ ] 添加小红书发布时间建议

### 待集成
- [ ] 将系列生成集成到 SKILL.md 主工作流
- [ ] 更新 README.md 和 USAGE.md
- [ ] 创建完整的端到端测试用例

---

## 技术细节

### API配置
- **端点**：`https://yunwu.ai/v1`
- **认证**：环境变量 `YUNWU_API_KEY`
- **图片生成模型**：`gemini-3-pro-image-preview`
- **文本生成模型**：`gemini-3-pro-preview`

### 输出格式
- **图片格式**：PNG
- **图片尺寸**：1080x1440像素（3:4竖版）
- **命名规则**：`序号_构图_风格_时间戳.png`
- **标题格式**：纯文本，<20字符
- **标签格式**：`#标签1 #标签2 ...`（空格分隔）

### 错误处理
- 图片生成失败：自动重试3次
- 标题生成失败：使用备用模板
- 标签生成失败：使用默认标签组合
- API超时：30秒超时限制

---

## 总结

本次更新实现了用户请求的核心功能：
1. ✅ 每次生成同一种风格时，生成4张形成系列
2. ✅ 为系列生成小红书标题（<20字符，诗意化）
3. ✅ 为系列生成话题标签（10个，混合策略）

所有功能已实现并准备测试。

---

## v1.1 - 全风格步骤图支持 (2026-01-31)

### 新增功能

**1. 所有风格都支持步骤图生成** ✅
- 不再限制只有彩铅可以生成步骤图
- 每种风格都有专门定制的5步绘画过程

**2. 各风格步骤图定义**：

| 风格 | 步骤 |
|------|------|
| **水彩（东方）** | 草稿 → 第一层水彩 → 叠加层次 → 细节刻画 → 完成 |
| **水彩（西方）** | 草稿 → 第一层水彩 → 叠加层次 → 细节刻画 → 完成 |
| **国画（东方）** | 构图 → 墨稿 → 淡彩 → 浓彩点睛 → 完成 |
| **彩铅（东方）** | 线稿 → 铺底色 → 深化色彩 → 细节刻画 → 完成 |
| **彩铅（西方）** | 线稿 → 铺底色 → 深化色彩 → 细节刻画 → 完成 |
| **油画（东方）** | 底稿 → 底色 → 中间色 → 高光与细节 → 完成 |
| **油画（西方）** | 底稿 → 底色 → 中间色 → 高光 → 完成 |
| **彩绘（东方）** | 线稿 → 平涂底色 → 叠加色彩 → 装饰细节 → 完成 |
| **彩绘（西方）** | 线稿 → 平涂底色 → 叠加色彩 → 装饰细节 → 完成 |

**3. 技术实现**：
- 新增 `generate_style_steps()` 通用方法
- 为每种风格定义专门的步骤描述
- 保留 `generate_pencil_steps()` 向后兼容

**4. 国画步骤图特别说明**：
- 国画不只是水墨，包含彩色
- 步骤包括：墨稿 + 淡彩 + 浓彩点睛
- 体现了国画"色墨结合"的特点

### 更新内容

**SKILL.md**：
- 更新 Step 1.2：所有风格都询问是否需要步骤图
- 添加各风格步骤图说明
- 简化执行逻辑（不再需要条件判断）

**generate_illustration.py**：
- 新增 `generate_style_steps()` 方法（250+ 行代码）
- 定义 9 种风格的步骤图配置
- 每种风格 5 个步骤，共 45 个步骤定义

### 用户反馈驱动

本次更新源于用户的两个重要反馈：
1. "为什么只有彩铅可以生成步骤图？"
2. "国画也不光是墨啊，国画也有颜色在里面的"

这些反馈帮助我们：
- 扩展了功能范围
- 更准确地理解了各种绘画风格
- 提升了 Skill 的专业性和完整性

---

**版本**: v1.1
**更新日期**: 2026-01-31
**向后兼容**: ✅ 是
