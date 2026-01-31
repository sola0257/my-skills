# 风格-模型映射表 v1.0

> **核心目的**：保证同一风格的视觉一致性，避免模型自动切换导致的不稳定

---

## 🎯 设计原则

### 1. 固定映射原则
- 每个风格固定使用一个模型
- **禁止** AI 根据情况自动选择模型
- **禁止** 同一风格使用不同模型

### 2. 测试验证原则
- 每个风格在上线前必须测试
- 对比不同模型的生成效果
- 选择视觉效果最好的模型作为固定选择

### 3. 中文支持优先
- 需要中文文字的风格必须使用 Gemini
- 彩铅步骤图强制使用 Gemini

---

## 📊 当前映射表（v1.0）

| 风格代码 | 用户友好名称 | 固定模型 | 原因 | 测试状态 |
|---------|-------------|---------|------|---------|
| `watercolor_oriental` | 清新水彩（东方） | `gemini-3-pro-image-preview` | 细腻晕染、留白控制好 | ✅ 已测试 |
| `watercolor_western` | 清新水彩（西方） | `gemini-3-pro-image-preview` | 植物插画细节好 | ✅ 已测试 |
| `ink_oriental` | 水墨国画（东方） | `gemini-3-pro-image-preview` | 水墨韵味、支持题款 | ⏳ 待测试 |
| `ink_western` | 水墨国画（西方） | `gemini-3-pro-image-preview` | 现代水墨效果 | ⏳ 待测试 |
| `pencil_oriental` | 细腻彩铅（东方） | `gemini-3-pro-image-preview` | 笔触细腻、纸张质感 | ⏳ 待测试 |
| `pencil_western` | 细腻彩铅（西方） | `gemini-3-pro-image-preview` | 写实风格、光影好 | ⏳ 待测试 |
| `pencil_steps` | 细腻彩铅（步骤图） | `gemini-3-pro-image-preview` | **强制**（中文标注） | ⏳ 待测试 |
| `oil_oriental` | 质感油画（东方） | `gemini-3-pro-image-preview` | 含蓄笔触、意境感 | ⏳ 待测试 |
| `oil_western` | 质感油画（西方） | `gemini-3-pro-image-preview` | 古典油画质感 | ⏳ 待测试 |
| `gouache_oriental` | 装饰彩绘（东方） | `gemini-3-pro-image-preview` | 平涂效果、装饰性 | ⏳ 待测试 |
| `gouache_western` | 装饰彩绘（西方） | `gemini-3-pro-image-preview` | 现代插画风格 | ⏳ 待测试 |

---

## 🔧 使用方法

### 在代码中强制使用

```python
# ❌ 错误做法：让 AI 自动选择
def select_model(style):
    if "需要艺术感":
        return "dall-e-3"
    else:
        return "gemini-3-pro-image-preview"

# ✅ 正确做法：使用固定映射表
STYLE_MODEL_MAPPING = {
    "watercolor_oriental": "gemini-3-pro-image-preview",
    "watercolor_western": "gemini-3-pro-image-preview",
    "ink_oriental": "gemini-3-pro-image-preview",
    "ink_western": "gemini-3-pro-image-preview",
    "pencil_oriental": "gemini-3-pro-image-preview",
    "pencil_western": "gemini-3-pro-image-preview",
    "pencil_steps": "gemini-3-pro-image-preview",  # 强制
    "oil_oriental": "gemini-3-pro-image-preview",
    "oil_western": "gemini-3-pro-image-preview",
    "gouache_oriental": "gemini-3-pro-image-preview",
    "gouache_western": "gemini-3-pro-image-preview",
}

def get_model_for_style(style_code):
    """获取风格对应的固定模型"""
    model = STYLE_MODEL_MAPPING.get(style_code)
    if not model:
        raise ValueError(f"未知风格代码: {style_code}")
    return model
```

---

## 🧪 测试计划

### 测试方法

对每个风格进行以下测试：

1. **Gemini 测试**
   - 生成5张同风格图片
   - 评估：视觉一致性、细节质量、色彩准确性

2. **DALL-E 3 测试**（可选）
   - 生成5张同风格图片
   - 对比 Gemini 的效果

3. **选择标准**
   - 视觉一致性 > 艺术感 > 细节质量
   - 如果需要中文，必须选 Gemini

### 测试记录模板

```markdown
## 风格：清新水彩（东方）

### Gemini 测试结果
- 视觉一致性：⭐⭐⭐⭐⭐
- 细节质量：⭐⭐⭐⭐
- 色彩准确性：⭐⭐⭐⭐⭐
- 留白控制：⭐⭐⭐⭐⭐
- 综合评分：4.75/5

### DALL-E 3 测试结果
- 视觉一致性：⭐⭐⭐
- 细节质量：⭐⭐⭐⭐⭐
- 色彩准确性：⭐⭐⭐⭐
- 留白控制：⭐⭐⭐
- 综合评分：3.75/5

### 最终选择：Gemini
**原因**：视觉一致性更好，留白控制更符合东方美感
```

---

## 📝 更新记录

### 如何更新映射表

1. **测试新模型**
   - 生成至少10张测试图
   - 对比现有模型的效果

2. **评估标准**
   - 视觉一致性是否提升？
   - 是否有明显优势？
   - 是否有副作用？

3. **更新流程**
   - 更新本文档的映射表
   - 更新 `scripts/generate_illustration.py` 中的配置
   - 记录更新原因和测试结果

### 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-01-31 | 初始版本，全部使用 Gemini（待测试验证） |

---

## ⚠️ 重要提醒

### 为什么需要固定映射？

**问题案例**：
```
用户生成"水墨国画"风格
第1次：AI 选择 Gemini → 淡雅水墨效果
第2次：AI 选择 DALL-E 3 → 浓重油画效果
结果：同一风格，视觉感受完全不同 ❌
```

**解决方案**：
```
用户生成"水墨国画"风格
第1次：固定使用 Gemini → 淡雅水墨效果
第2次：固定使用 Gemini → 淡雅水墨效果
结果：同一风格，视觉感受一致 ✅
```

### 执行规范

- ✅ 必须使用 `STYLE_MODEL_MAPPING` 字典
- ✅ 必须在代码中硬编码映射关系
- ❌ 禁止使用 if-else 逻辑判断
- ❌ 禁止让 AI 根据 prompt 内容选择模型
- ❌ 禁止用户自定义模型选择

---

**最后更新**：2026-01-31
