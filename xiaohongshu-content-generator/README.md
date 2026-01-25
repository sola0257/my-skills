# 小红书内容生成器 - 文件结构说明

## 📁 目录结构

```
xiaohongshu-content-generator/
├── SKILL.md                          # 主配置文件（v3.1）
├── README.md                         # 本文件
├── knowledge/                        # 知识库
│   ├── xiaohongshu-copywriting-guide.md      # 文案创作手册
│   ├── image-prompt-guide.md                 # 配图 Prompt 模板
│   ├── flexible_prompt_system.md             # 分层 Prompt 系统（v3.1）
│   └── character_references/                 # 人物参考照片
│       ├── README.md
│       ├── IMGBB_CONFIG.md
│       ├── imgbb_urls.json
│       ├── primary_ref.jpg
│       ├── secondary_ref.jpg
│       ├── backup_01.jpg
│       └── backup_02.jpg
├── scripts/                          # 核心脚本（生产环境）
│   ├── deeprouter_mj_api.py                  # Midjourney API 封装
│   ├── hybrid_image_generator.py             # 混合生成器（MJ + Gemini）
│   └── generate_xhs_post.py                  # 完整内容生成主脚本
└── tests/                            # 测试文件（临时，不纳入版本控制）
    ├── test_*.py                             # 各种测试脚本
    └── test_*.png                            # 测试生成的图片
```

## 📝 文件说明

### 核心文件

**SKILL.md**
- Skill 主配置文件
- 包含完整的执行流程、API 配置、模板规则
- 当前版本：v3.1

### 知识库 (knowledge/)

**xiaohongshu-copywriting-guide.md**
- 小红书文案创作规则
- 标题、正文、标签的写作模板

**image-prompt-guide.md**
- 配图风格指南
- 不同选题类型的配图策略

**flexible_prompt_system.md** (v3.1 新增)
- 分层 Prompt 模板系统
- 支持5大选题类型：场景痛点、新手避坑、季节时令、送礼推荐、养护知识
- 灵活的内容填充机制

**character_references/**
- 人物参考照片及配置
- ImgBB 图床 URL 映射

### 核心脚本 (scripts/)

**deeprouter_mj_api.py**
- DeepRouter Midjourney API 完整封装
- 支持图片上传、任务提交、状态查询、图片下载
- 用于生成高质量场景图

**hybrid_image_generator.py** (v3.1 新增)
- 混合生成器：Midjourney + Gemini
- Midjourney 生成场景底图
- Gemini 添加中文文字叠加
- 解决封面"高颜值场景图 + 大字标题"需求

**generate_xhs_post.py**
- 完整的小红书内容生成主脚本
- 整合文案生成 + 配图生成
- 一键生成完整内容包

### 测试文件 (tests/)

⚠️ **注意：此目录仅用于开发测试，不纳入正式版本**

包含各种测试脚本和测试生成的图片，用于：
- API 功能测试
- Prompt 效果测试
- 参数调优测试

## 🔄 使用流程

### 方式1：直接调用 Skill

```bash
# 在 Claude Code 中
/xiaohongshu-content-generator 春日居家绿植装饰
```

### 方式2：使用脚本

```python
import sys
sys.path.append('/Users/dj/.claude/skills/xiaohongshu-content-generator/scripts')

from hybrid_image_generator import HybridImageGenerator

# 初始化
generator = HybridImageGenerator(
    mj_api_key="sk-TKd09OF2QjXLWbDAn76sVzlxvw8lSaUL4qYl7pR5FEYFbF8I",
    gemini_api_key="sk-UqMsXIWjukWom3cHPkbf5xBqYrnEJHz3J7cdQQNhkFg974X5"
)

# 生成封面
generator.generate_cover_with_text(
    scene_prompt="...",
    title_text="春日居家绿植装饰指南",
    output_dir="/path/to/output",
    topic_name="春日绿植"
)
```

## 📊 版本历史

- **v3.1** (2026-01-14)
  - 新增 Midjourney API 集成
  - 新增混合生成器（MJ + Gemini）
  - 新增分层 Prompt 系统
  - 优化文件结构

- **v3.0**
  - 新增商品库匹配
  - 新增商品软植入

- **v2.0**
  - 子文件夹输出结构
  - 标题字数限制
  - 地域标签

## 🔗 相关路径

- **Skill 目录**: `/Users/dj/.claude/skills/xiaohongshu-content-generator/`
- **输出目录**: `/Users/dj/Documents/slowseasons AI工厂/内容发布/发布记录/2026/小红书/`
- **商品库**: `/Users/dj/Documents/slowseasons AI工厂/商品库/商品数据.xlsx`
