---
name: product-pipeline
description: "商品优化流水线。输入商品Excel和图片，自动完成SKU精简、卖点提炼、图片处理，输出优化后的Excel和图片。"
license: MIT
version: "2.0"
---


## ⚠️ 恢复执行重要提醒

**当用户说"继续Step X"、"继续执行"、"下一步"时**：

本 Skill 的所有步骤都可能需要用户输入或确认。
在恢复执行任何步骤前，请遵循全局"恢复执行强制规则"（~/.claude/CLAUDE.md）：

1. ✅ 先读取该步骤的完整描述
2. ✅ 检查是否需要提问或确认
3. ✅ 确认所有输入参数
4. ✅ 有疑问先问用户

**禁止直接开始执行，禁止假设已知上下文。**

---

# 🚀 商品优化流水线 v2.0

## 🚨 静默执行协议

**执行规则：**
- ❌ **禁止** 请求确认（Do not ask for confirmation to proceed）
- ❌ **禁止** 中途询问
- ✅ **必须** 一次性完成全部处理（Generate the full output in one go）
- ✅ **必须** 使用默认值处理缺失数据（If data is missing, use the defined defaults）
- ✅ **必须** 自动执行图片处理脚本

---

## 📋 概述

此技能是**端到端自动化流水线**，一次性完成：

1. **商品分析**：读取Excel，评估每个商品
2. **SKU精简**：自动精简到3-5个核心SKU
3. **卖点提炼**：自动生成符合品牌调性的卖点
4. **图片处理**：调用Python脚本批量处理图片
5. **输出结果**：生成优化后的Excel和处理后的图片

**无需人工介入，批量处理100+商品。**

---

## ⚙️ 触发条件

**语义触发词**：
- "处理这批商品" + Excel路径
- "优化商品上架"
- "批量处理1688商品"
- "商品流水线处理"

**输入要求**：
- 商品Excel文件路径（必填）
- 商品图片文件夹路径（可选，用于图片处理）

---

## 📥 输入格式

### 商品Excel格式

| 列名 | 说明 | 必填 |
|-----|------|------|
| 商品名称 | 原始商品名 | ✅ |
| SKU列表 | 多个SKU，换行或逗号分隔 | ✅ |
| 价格区间 | 如 "19-159" 或具体价格列表 | ✅ |
| 销量 | 总销量或SKU销量 | 建议 |
| 原始描述 | 1688采集的描述 | 可选 |
| 图片链接 | 主图URL | 可选 |

---

## 🔄 自动化处理流程

### Step 1: 读取商品数据

```python
import pandas as pd
df = pd.read_excel(input_path)
```

### Step 2: 对每个商品执行优化

```
for 商品 in 商品列表:
    1. 分析SKU → 应用精简规则 → 保留TOP3
    2. 分析原始描述 → 提炼卖点 → 生成3个核心卖点
    3. 优化标题 → 去除冗余词 → 保留15字以内
    4. 标记图片处理需求
```

### Step 3: SKU精简规则（自动执行）

```python
def select_top_skus(skus, prices, sales=None, max_count=3):
    """
    自动精简SKU
    规则：
    1. 有销量数据 → 按销量排序取TOP3
    2. 无销量数据 → 按价格取低/中/高各1个
    3. 去除价格极端值（超出中位数±50%）
    """
    # 计算价格中位数
    median_price = statistics.median(prices)
    
    # 过滤极端价格
    valid_skus = [
        sku for sku, price in zip(skus, prices)
        if median_price * 0.5 <= price <= median_price * 1.5
    ]
    
    # 按销量或价格排序
    if sales:
        sorted_skus = sorted(zip(valid_skus, sales), key=lambda x: x[1], reverse=True)
    else:
        sorted_skus = sorted(zip(valid_skus, prices), key=lambda x: x[1])
    
    # 返回TOP N
    return [sku for sku, _ in sorted_skus[:max_count]]
```

### Step 4: 卖点提炼（自动执行）

**品牌调性关键词库**：
- 🌿 自然、治愈、慢养、陪伴、生长
- 🏠 家居、氛围、角落、光线、窗台
- 💚 绿意、清新、透气、呼吸、生命力
- 🎨 质感、手作、温润、素雅、克制

**卖点生成模板**：
```
基于商品品类 + 材质 + 特性，自动生成：
- 卖点1: [功能/特性] - 解决什么问题
- 卖点2: [材质/品质] - 为什么值得信赖
- 卖点3: [场景/情感] - 带来什么体验
```

### Step 5: 图片处理（调用脚本）

```bash
# 自动执行图片处理脚本
python scripts/image_processor.py \
    --input /path/to/images \
    --output /path/to/processed
```

---

## 📤 输出格式

### 1. 优化后的Excel

输出路径：`{原文件名}_optimized.xlsx`

| 列名 | 内容 |
|-----|------|
| 商品名称 | 优化后的标题（15字以内） |
| 原商品名称 | 保留原始名称 |
| 保留SKU | 精简后的3个SKU |
| 淘汰SKU | 被淘汰的SKU列表 |
| 卖点1 | 自动生成 |
| 卖点2 | 自动生成 |
| 卖点3 | 自动生成 |
| 分享描述 | 一句话描述 |
| 建议售价 | 基于保留SKU计算 |
| 处理状态 | 已处理/需人工检查 |

### 2. 处理后的图片

输出路径：`processed_images/`

```
processed_images/
├── 商品1_主图.jpg
├── 商品2_主图.jpg
└── ...
```

### 3. 处理报告（Markdown）

```markdown
# 商品优化报告

**处理时间**：2026-01-14 15:30
**商品总数**：50
**成功处理**：48
**需人工检查**：2

## 处理摘要

| 指标 | 数值 |
|-----|------|
| SKU精简数量 | 从 1200 → 150 |
| 平均保留SKU | 3个/商品 |
| 图片处理 | 48张 |

## 需人工检查的商品

1. **商品A** - 原因：SKU少于3个，无法精简
2. **商品B** - 原因：无价格信息
```

---

## 🖼️ 图片处理脚本

### 安装依赖

```bash
pip install rembg Pillow
```

### 使用方法

```bash
# 批量处理
python scripts/image_processor.py \
    --input ./原始图片 \
    --output ./处理后图片

# 单张处理
python scripts/image_processor.py \
    --input ./image.jpg \
    --output ./processed.jpg \
    --single
```

### 默认效果

- 自动抠图（使用Rembg）
- 合成莫兰迪渐变背景（米白→淡绿）
- 输出尺寸：800x800px
- 商品居中，占画面80%

---

## 🔧 使用示例

### 示例1：完整流水线

**输入**：
```
处理这批商品：
Excel路径：/Users/dj/Downloads/1688商品.xlsx
图片文件夹：/Users/dj/Downloads/商品图片/
```

**输出**：
- `/Users/dj/Downloads/1688商品_optimized.xlsx`
- `/Users/dj/Downloads/商品图片_processed/`
- 处理报告（控制台输出）

---

### 示例2：只优化文字信息

**输入**：
```
优化这个商品Excel：/Users/dj/Downloads/商品清单.xlsx
```

**输出**：
- 优化后的Excel
- 无图片处理

---

## 🛠️ 错误处理

| 场景 | 自动处理方式 |
|------|-------------|
| Excel格式不规范 | 尝试自动识别列名 |
| SKU数量<3 | 保留全部，标记"无需精简" |
| 无销量数据 | 按价格分布选择 |
| 图片处理失败 | 记录失败项，继续处理下一个 |
| 缺少必填字段 | 标记"需人工检查" |

---

## 📝 Anti-Patterns（禁止做的事）

### ❌ 错误示例

```
❌ "Excel中有50个商品，是否开始处理？"
❌ "商品A的SKU已精简，需要确认吗？"
❌ "图片处理完成，是否继续下一步？"
```

### ✅ 正确示例

```
✅ 直接读取Excel，批量处理所有商品
✅ 自动精简SKU，无需确认
✅ 一次性输出所有结果
```

---

## 🔗 依赖

- Python 3.8+
- pandas
- rembg
- Pillow

### 安装命令

```bash
pip install pandas rembg Pillow openpyxl
```

---

## 📚 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0 | 2026-01-14 | 全自动化流水线：SKU精简+卖点提炼+图片处理 |
| v1.0 | 2026-01-14 | 初版：分析+建议模式 |
