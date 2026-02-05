---
name: product-catalog
description: "商品库管理技能。读取有赞商品数据，提供商品搜索、关键词匹配、商品推荐等功能，供内容生成技能调用。"
license: MIT
version: "1.0"
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

# 📦 商品库管理 v1.0

## 🚨 静默执行协议

**执行规则：**
- ❌ **禁止** 请求确认
- ❌ **禁止** 中途询问
- ✅ **必须** 自动读取商品数据
- ✅ **必须** 返回结构化结果

---

## 📋 概述

此技能为**内部服务技能**，供其他内容生成技能调用，提供：
1. 商品数据读取和解析
2. 基于关键词的商品匹配
3. 商品推荐排序

---

## ⚙️ 配置信息

### 数据源配置

```python
# 商品数据Excel路径
PRODUCT_EXCEL_PATH = "/Users/dj/Documents/slowseasons AI工厂/商品库/商品数据.xlsx"

# 有赞API配置（可选，优先级高于Excel）
YOUZAN_API_ENABLED = False  # 设置为True启用API
YOUZAN_APP_ID = ""          # 待配置
YOUZAN_APP_SECRET = ""      # 待配置
```

### 商品字段映射

| Excel列名 | 内部字段 | 用途 |
|-----------|----------|------|
| 商品id | `product_id` | 唯一标识 |
| 商品名称 | `name` | 显示名称 |
| 价格（元） | `price` | 售价 |
| 商品规格 | `spec` | 规格描述 |
| 商品分组 | `category` | 分类标签 |
| 商品卖点 | `selling_point` | 卖点描述 |
| 分享描述 | `share_desc` | 分享文案 |
| 商品链接 | `url` | 小程序链接 |
| 累计销量 | `sales` | 销量数据 |
| 商品状态 | `status` | 在售/下架 |

---

## 🔧 核心功能

### 功能1: 读取商品库

```python
def load_products():
    """
    从Excel读取所有在售商品
    返回: List[Dict] 商品列表
    """
    import pandas as pd
    
    df = pd.read_excel(PRODUCT_EXCEL_PATH)
    
    # 只保留在售商品
    df = df[df['商品状态'] == '销售中']
    
    products = []
    for _, row in df.iterrows():
        products.append({
            'product_id': str(row['商品id']),
            'name': row['商品名称'],
            'price': row['价格（元）'],
            'spec': row['商品规格'],
            'category': row['商品分组'],
            'selling_point': row['商品卖点'] if pd.notna(row['商品卖点']) else '',
            'share_desc': row['分享描述'] if pd.notna(row['分享描述']) else '',
            'url': row['商品链接'],
            'sales': row['累计销量'] if pd.notna(row['累计销量']) else 0
        })
    
    return products
```

### 功能2: 关键词匹配商品

```python
def match_products(keywords: list, max_results: int = 3):
    """
    根据关键词匹配相关商品
    
    参数:
        keywords: 关键词列表，如 ['绿植', '阳台', '春季']
        max_results: 最多返回商品数
    
    返回:
        匹配的商品列表，按相关度排序
    """
    products = load_products()
    scored_products = []
    
    for product in products:
        score = 0
        search_text = f"{product['name']} {product['category']} {product['selling_point']} {product['share_desc']}"
        
        for keyword in keywords:
            if keyword in search_text:
                score += 1
                # 名称中包含关键词加权
                if keyword in product['name']:
                    score += 2
        
        if score > 0:
            scored_products.append((score, product))
    
    # 按分数降序排序
    scored_products.sort(key=lambda x: x[0], reverse=True)
    
    return [p[1] for p in scored_products[:max_results]]
```

### 功能3: 生成商品推荐文案

```python
def generate_product_recommendation(product: dict, style: str = 'soft'):
    """
    生成商品推荐文案
    
    参数:
        product: 商品信息字典
        style: 'soft'(软植入) / 'direct'(直接推荐) / 'card'(卡片式)
    
    返回:
        推荐文案字符串
    """
    name = product['name']
    price = product['price']
    selling_point = product['selling_point']
    
    if style == 'soft':
        # 软植入风格（适合小红书、公众号正文）
        return f"我自己用的是{name}，{selling_point}"
    
    elif style == 'direct':
        # 直接推荐风格（适合评论区、文末）
        return f"💡 推荐：{name} ¥{price}\n{selling_point}"
    
    elif style == 'card':
        # 卡片式（适合公众号服务号CTA）
        return f"""
**{name}**
💰 ¥{price}
✨ {selling_point}
"""
    
    return ""
```

---

## 📤 输出格式

### 商品匹配结果

```json
{
  "matched_products": [
    {
      "product_id": "4444849064",
      "name": "朱顶红 室内外花卉盆栽国产绿植",
      "price": 120.0,
      "spec": "10-12cm塑料盆+椰糠土",
      "category": "小马/小型",
      "selling_point": "株高范围：（球茎直径4-5cm）",
      "url": "https://shop184883195.m.youzan.com/v2/goods/xxx",
      "match_score": 3
    }
  ],
  "keywords_used": ["绿植", "室内", "盆栽"],
  "total_matched": 5
}
```

---

## 🔗 被其他技能调用

### 调用示例（在内容生成技能中）

```python
# 1. 从选题提取关键词
topic = "春季阳台绿植养护"
keywords = ["春季", "阳台", "绿植", "养护"]

# 2. 调用商品库匹配
matched = match_products(keywords, max_results=3)

# 3. 在内容中植入
if matched:
    product = matched[0]
    soft_rec = generate_product_recommendation(product, style='soft')
    # 将 soft_rec 插入文案适当位置
```

---

## 🛠️ 错误处理

| 场景 | 处理方式 |
|------|----------|
| Excel文件不存在 | 提示用户更新商品数据 |
| 无匹配商品 | 返回空列表，内容技能跳过商品植入 |
| 字段缺失 | 使用空字符串填充 |

---

## 📝 数据更新

### 手动更新流程

1. 从有赞后台导出商品Excel
2. 替换 `/商品库/商品数据.xlsx`
3. 下次内容生成时自动使用新数据

### 自动更新（待配置有赞API）

配置 `YOUZAN_APP_ID` 和 `YOUZAN_APP_SECRET` 后，技能将自动调用API获取最新商品数据。

---

## 📚 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-01-14 | 初始版本：Excel读取 + 关键词匹配 |
